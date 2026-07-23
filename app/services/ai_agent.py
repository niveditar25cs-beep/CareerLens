import os
import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from duckduckgo_search import AsyncDDGS
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.models.student import Student
from app.models.opportunity import Opportunity, OpportunityType, JobStatus

logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.warning("GEMINI_API_KEY is not set. AI Agent will fail if triggered.")


async def fetch_search_results(query: str, max_results: int = 15) -> str:
    """Fetch search results from DuckDuckGo."""
    try:
        async with AsyncDDGS() as ddgs:
            results = [r async for r in ddgs.atext(query, max_results=max_results)]
            
        # Format results for the LLM
        formatted = ""
        for i, r in enumerate(results):
            formatted += f"Result {i+1}:\n"
            formatted += f"Title: {r.get('title')}\n"
            formatted += f"URL: {r.get('href')}\n"
            formatted += f"Snippet: {r.get('body')}\n\n"
        return formatted
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return ""


def parse_llm_response(response_text: str) -> List[Dict[str, Any]]:
    """Parse the JSON list from the LLM response."""
    try:
        # Strip markdown json blocks if present
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "opportunities" in data:
            return data["opportunities"]
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response: {e}\nResponse: {response_text}")
        return []


async def run_opportunity_search_agent(student: Student, db: AsyncSession) -> List[Opportunity]:
    """
    Run the AI Agent for a specific student to find personalized opportunities.
    """
    # 1. Construct search query based on student profile
    skills = student.skills or "software engineering"
    department = student.major or "computer science"
    
    query = f"({skills} OR {department}) (internship OR job OR hackathon OR scholarship) active application site:internshala.com OR site:linkedin.com OR site:unstop.com"
    
    # 2. Fetch raw search results
    search_text = await fetch_search_results(query, max_results=20)
    
    if not search_text:
        return []

    # 3. Process with Gemini
    system_prompt = f"""
    Act as an Opportunity Search AI Agent for CareerLens. 
    Your task is to analyze the provided search results and extract valid opportunities.
    Filter opportunities based on the student's profile:
    - Department: {student.major}
    - Skills: {student.skills}
    - Year of Study: {student.graduation_year}
    - Interests: {student.interests}
    
    Remove duplicate or expired listings, prioritize relevant and active opportunities.
    
    Return ONLY a JSON list of objects. Do not include any other text.
    Each object must have exactly these keys:
    - "title": (string) The title of the opportunity
    - "company": (string) Organization name
    - "description": (string) Brief description
    - "eligibility": (string) Eligibility criteria
    - "location": (string) Location (or Remote)
    - "deadline": (string) Application deadline if available, else null
    - "application_url": (string) Application link (the href from the search result)
    - "source": (string) Source platform (e.g., LinkedIn, Internshala)
    - "opportunity_type": (string) Must be one of: internship, job, scholarship, competition, workshop, other
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
        response = model.generate_content(
            f"Here are the search results:\n{search_text}\n\nReturn the JSON list.",
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        parsed_opportunities = parse_llm_response(response.text)
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return []

    # 4. Save and deduplicate in database
    saved_opportunities = []
    
    for opp_data in parsed_opportunities:
        title = opp_data.get("title")
        company = opp_data.get("company")
        url = opp_data.get("application_url")
        
        if not title or not company:
            continue
            
        # Deduplication check
        existing_query = select(Opportunity).where(
            (Opportunity.original_url == url) |
            ((Opportunity.title == title) & (Opportunity.company == company))
        )
        existing = await db.execute(existing_query)
        if existing.scalars().first():
            continue
            
        # Map opportunity_type
        opp_type_str = str(opp_data.get("opportunity_type", "other")).lower()
        try:
            opp_type = OpportunityType(opp_type_str)
        except ValueError:
            opp_type = OpportunityType.OTHER

        new_opp = Opportunity(
            title=title,
            company=company,
            description=opp_data.get("description"),
            eligibility=opp_data.get("eligibility"),
            location=opp_data.get("location"),
            application_url=url,
            original_url=url, # Use same for uniqueness
            source=opp_data.get("source"),
            opportunity_type=opp_type,
            status=JobStatus.ACTIVE
        )
        db.add(new_opp)
        saved_opportunities.append(new_opp)
        
    if saved_opportunities:
        await db.commit()
        for opp in saved_opportunities:
            await db.refresh(opp)
            
    return saved_opportunities
