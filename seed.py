"""
Database seed script for CareerLens backend.
Populates SQLite database with sample students, opportunities, notifications, and saved items.
"""

import asyncio
from datetime import datetime, timedelta, timezone
from app.database.database import AsyncSessionLocal, engine, Base
from app.database.init_db import init_db
from app.models.student import Student
from app.models.opportunity import Opportunity, OpportunityType
from app.models.notification import Notification
from app.models.saved import SavedOpportunity
from app.utils.security import hash_password



async def seed():
    print("[INIT] Re-creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        print("[SEED] Seeding data...")



        # Create Sample Students
        student1 = Student(
            full_name="Alex Rivera",
            email="alex@example.com",
            hashed_password=hash_password("Password123!"),
            phone="+1 (555) 019-2834",
            university="Stanford University",
            major="Computer Science",
            skills="Python, FastAPI, Machine Learning, React, PostgreSQL",
            interests="Artificial Intelligence, Full Stack Web Development, Cloud Engineering",
            bio="Passionate CS senior looking for software engineering internships and AI research fellowships.",
        )
        student2 = Student(
            full_name="Maria Chen",
            email="maria@example.com",
            hashed_password=hash_password("Password123!"),
            phone="+1 (555) 014-9821",
            university="MIT",
            major="Data Science",
            skills="Python, SQL, R, Data Visualization, Deep Learning, PyTorch",
            interests="Data Science, Analytics, Computer Vision",
            bio="Data Science enthusiast passionate about predictive modeling and biomedical AI.",
        )

        session.add_all([student1, student2])
        await session.flush()  # populate student1.id and student2.id

        now = datetime.now(timezone.utc)

        # Create Sample Opportunities
        opp1 = Opportunity(
            title="Software Engineering Intern (Summer 2026)",
            description="Join our core engineering team to build scalable microservices and user-facing web features.",
            company="TechCorp Solutions",
            location="San Francisco, CA (Hybrid)",
            opportunity_type=OpportunityType.INTERNSHIP,
            category="Software Engineering",
            skills_required="Python, FastAPI, React, Docker, SQL",
            application_url="https://example.com/jobs/swe-intern",
            deadline=now + timedelta(days=30),
            source="TechCorp Careers",
        )
        opp2 = Opportunity(
            title="AI & Machine Learning Research Fellow",
            description="Prestigious 6-month fellowship researching generative AI models and LLM alignment.",
            company="OpenAI Frontiers",
            location="Remote",
            opportunity_type=OpportunityType.JOB,
            category="Machine Learning",
            skills_required="Python, PyTorch, Machine Learning, Deep Learning, Natural Language Processing",
            application_url="https://example.com/jobs/ai-fellow",
            deadline=now + timedelta(days=14),
            source="AI Research Portal",
        )
        opp3 = Opportunity(
            title="Women in STEM Excellence Scholarship 2026",
            description="$10,000 merit scholarship for undergraduate students pursuing degrees in Computer Science and Data Science.",
            company="Global STEM Foundation",
            location="Global",
            opportunity_type=OpportunityType.SCHOLARSHIP,
            category="Scholarships",
            skills_required="Computer Science, Data Science, Academic Excellence",
            application_url="https://example.com/scholarships/women-in-stem",
            deadline=now + timedelta(days=45),
            source="STEM Grants Hub",
        )
        opp4 = Opportunity(
            title="Full-Stack Web Development Hackathon",
            description="48-hour online hackathon with $25,000 in prizes for modern web and mobile apps.",
            company="DevGlobal Network",
            location="Online",
            opportunity_type=OpportunityType.COMPETITION,
            category="Hackathon",
            skills_required="React, Node.js, Python, UI/UX, Cloud",
            application_url="https://example.com/hackathons/devglobal2026",
            deadline=now + timedelta(days=7),
            source="Hackathon Central",
        )
        opp5 = Opportunity(
            title="Cloud Architecture & DevOps Masterclass Workshop",
            description="Hands-on intensive workshop covering Kubernetes, CI/CD pipelines, and AWS cloud deployment.",
            company="CloudScale Academy",
            location="New York, NY",
            opportunity_type=OpportunityType.WORKSHOP,
            category="DevOps",
            skills_required="Docker, Kubernetes, AWS, CI/CD, Linux",
            application_url="https://example.com/workshops/cloud-devops",
            deadline=now + timedelta(days=20),
            source="CloudScale Events",
        )

        session.add_all([opp1, opp2, opp3, opp4, opp5])
        await session.flush()

        # Seed Saved Opportunity
        saved_opp = SavedOpportunity(
            student_id=student1.id,
            opportunity_id=opp1.id,
        )
        session.add(saved_opp)

        # Seed Notifications
        notif1 = Notification(
            student_id=student1.id,
            title="New Opportunity Match",
            message='A new opportunity "Software Engineering Intern (Summer 2026)" matches your Python & FastAPI skills!',
            is_read=False,
            notification_type="new_match",
        )
        notif2 = Notification(
            student_id=student1.id,
            title="Deadline Approaching",
            message='The application deadline for "Full-Stack Web Development Hackathon" is in 7 days!',
            is_read=False,
            notification_type="deadline",
        )
        session.add_all([notif1, notif2])


        await session.commit()
        print("[SUCCESS] Database successfully seeded!")


if __name__ == "__main__":
    asyncio.run(seed())

