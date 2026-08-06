import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def test_resend_connection():
    if not RESEND_API_KEY or RESEND_API_KEY == "YOUR_RESEND_API_KEY":
        print("[-] Resend API key not configured in .env")
        return False
        
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # We test connectivity by listing domains or emails (or just hitting a lightweight endpoint)
    # Just checking auth validity with an invalid payload or a simple GET to domains
    try:
        response = requests.get("https://api.resend.com/domains", headers=headers, timeout=5)
        if response.status_code == 200:
            print("[+] Successfully connected to Resend API!")
            return True
        else:
            print(f"[-] Failed to connect: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[-] Exception during connection: {e}")
        return False

if __name__ == "__main__":
    test_resend_connection()
