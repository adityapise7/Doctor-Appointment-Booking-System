import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def seed():
    print("Seeding Departments...")
    depts = [
        {"name": "Cardiology", "description": "Heart care"},
        {"name": "Pediatrics", "description": "Child care"},
        {"name": "General Practice", "description": "General medicine"}
    ]
    resp = requests.post(f"{SUPABASE_URL}/rest/v1/departments", json=depts, headers=headers)
    if resp.status_code not in [201, 200]:
        print("Error seeding depts:", resp.text)
        return
    dept_records = resp.json()
    cardio_id = dept_records[0]["id"]
    
    print("Seeding Users (Doctor)...")
    users = [
        {"email": "doctor@aurahealth.com", "role": "Doctor"}
    ]
    resp = requests.post(f"{SUPABASE_URL}/rest/v1/users", json=users, headers=headers)
    if resp.status_code not in [201, 200]:
        print("Error seeding users:", resp.text)
        return
    user_records = resp.json()
    doc_user_id = user_records[0]["id"]
    
    print("Seeding Doctors...")
    docs = [
        {
            "user_id": doc_user_id,
            "department_id": cardio_id,
            "full_name": "Sarah Jenkins",
            "specialization": "Cardiologist",
            "working_hours": {
                "days": [1, 2, 3, 4, 5],
                "start_time": "09:00",
                "end_time": "17:00",
                "break": {"start": "12:00", "end": "13:00"},
                "slot_duration": 30
            }
        }
    ]
    resp = requests.post(f"{SUPABASE_URL}/rest/v1/doctors", json=docs, headers=headers)
    if resp.status_code not in [201, 200]:
        print("Error seeding doctors:", resp.text)
        return
    
    print("Seeding Complete!")

if __name__ == "__main__":
    seed()
