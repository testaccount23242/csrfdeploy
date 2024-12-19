# bot.py
import requests

# Bot configuration
BOT_USERNAME = "admin"
BOT_PASSWORD = "adminpass"
TARGET_URL = "http://127.0.0.1:5000"

session = requests.Session()

def bot_login():
    login_url = f"{TARGET_URL}/login"
    payload = {"username": BOT_USERNAME, "password": BOT_PASSWORD}
    response = session.post(login_url, data=payload)
    if response.status_code == 200:
        print("[Bot] Logged in successfully as admin.")
    else:
        print("[Bot] Failed to log in.")

def visit_payload(payload_url):
    print(f"[Bot] Visiting payload: {payload_url}")
    response = session.get(payload_url)
    if response.status_code == 200:
        print("[Bot] Payload executed.")
    else:
        print("[Bot] Failed to execute payload.")

def main():
    bot_login()
    payload_url = input("Enter payload URL: ")
    visit_payload(payload_url)

if __name__ == "__main__":
    main()
