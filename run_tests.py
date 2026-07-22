"""
Integration tests for CareerLens FastAPI backend.
"""

import sys
import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCareerLensAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Register a fresh user and retrieve authentication token."""
        # 1. Register test user
        register_payload = {
            "full_name": "Test User",
            "email": "testuser@example.com",
            "password": "Password123!",
            "university": "Test University",
            "major": "Computer Science",
            "skills": "Python, FastAPI",
            "interests": "AI, Cloud",
        }
        res = client.post("/api/auth/register", json=register_payload)
        if res.status_code == 400:  # already registered from prior run
            pass
        else:
            assert res.status_code == 201, res.text

        # 2. Login to get token
        login_res = client.post(
            "/api/auth/login",
            json={"email": "testuser@example.com", "password": "Password123!"},
        )
        assert login_res.status_code == 200, login_res.text
        token = login_res.json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {token}"}

    def test_01_root(self):
        res = client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")

    def test_02_get_profile(self):
        res = client.get("/api/students/me", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["email"], "testuser@example.com")

    def test_03_update_profile(self):
        updates = {"bio": "Updated bio for automated testing"}
        res = client.put("/api/students/me", json=updates, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["bio"], "Updated bio for automated testing")

    def test_04_list_and_search_opportunities(self):
        res = client.get("/api/opportunities/")
        self.assertEqual(res.status_code, 200)
        items = res.json()
        self.assertGreaterEqual(len(items), 1)

        # Search by query term
        search_res = client.get("/api/opportunities/?q=Software")
        self.assertEqual(search_res.status_code, 200)

    def test_05_create_and_manage_opportunity(self):
        opp_data = {
            "title": "Backend Development Intern",
            "description": "Building FastAPI services",
            "company": "Startup Inc",
            "location": "Remote",
            "opportunity_type": "internship",
            "category": "Backend",
            "skills_required": "Python, FastAPI",
        }
        create_res = client.post("/api/opportunities/", json=opp_data)
        self.assertEqual(create_res.status_code, 201)
        opp_id = create_res.json()["id"]

        # Fetch created opportunity
        get_res = client.get(f"/api/opportunities/{opp_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["title"], "Backend Development Intern")

        # Save opportunity
        save_res = client.post(f"/api/opportunities/{opp_id}/save", headers=self.headers)
        self.assertEqual(save_res.status_code, 201)

        # List saved opportunities
        saved_list = client.get("/api/opportunities/saved/me", headers=self.headers)
        self.assertEqual(saved_list.status_code, 200)
        self.assertTrue(any(item["opportunity_id"] == opp_id for item in saved_list.json()))

        # Unsave opportunity
        unsave_res = client.delete(f"/api/opportunities/{opp_id}/save", headers=self.headers)
        self.assertEqual(unsave_res.status_code, 204)

        # Delete opportunity
        del_res = client.delete(f"/api/opportunities/{opp_id}")
        self.assertEqual(del_res.status_code, 204)

    def test_06_recommendations(self):
        res = client.get("/api/recommendations/", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json(), list)

        refresh_res = client.post("/api/recommendations/refresh", headers=self.headers)
        self.assertEqual(refresh_res.status_code, 200)
        self.assertIn("count", refresh_res.json())

    def test_07_notifications(self):
        res = client.get("/api/notifications/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

        read_all_res = client.put("/api/notifications/read-all", headers=self.headers)
        self.assertEqual(read_all_res.status_code, 200)

    def test_08_dashboard(self):
        res = client.get("/api/dashboard/", headers=self.headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("total_opportunities", data)
        self.assertIn("saved_opportunities", data)
        self.assertIn("unread_notifications", data)


if __name__ == "__main__":
    unittest.main()
