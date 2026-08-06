import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def test_supabase_connection():
    if not SUPABASE_URL or not SUPABASE_KEY or SUPABASE_URL == "YOUR_SUPABASE_URL":
        print("[-] Supabase credentials not configured in .env")
        return False
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        # Request a table instead of root which requires a secret API key
        response = requests.get(f"{SUPABASE_URL}/rest/v1/Users?limit=1", headers=headers, timeout=5)
        if response.status_code in [200, 404, 400]:
            # 200 OK, 404 Not Found (table doesn't exist yet but auth is valid), 400 Bad Request
            print("[+] Successfully connected to Supabase!")
            return True
        else:
            print(f"[-] Failed to connect: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[-] Exception during connection: {e}")
        return False

if __name__ == "__main__":
    test_supabase_connection()
