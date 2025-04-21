import requests
from bs4 import BeautifulSoup
import time
import os

# NADEEM LOGO
logo = r'''
███    ██  █████  ██████  ███████ ███████ ███    ███
████   ██ ██   ██ ██   ██ ██      ██      ████  ████
██ ██  ██ ███████ ██████  █████   █████   ██ ████ ██
██  ██ ██ ██   ██ ██   ██ ██      ██      ██  ██  ██
██   ████ ██   ██ ██   ██ ███████ ███████ ██      ██
'''

def show_logo():
    os.system('clear' if os.name != 'nt' else 'cls')
    for line in logo.splitlines():
        print(f"\033[1;32m{line}\033[0m")
        time.sleep(0.1)
    print("\n\033[1;36m     [×] Welcome to NADEEM'S TOKEN TOOLKIT\033[0m\n")

# Extract token from cookie
def get_token_from_cookie(cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile)',
        'Referer': 'https://business.facebook.com/',
        'Host': 'business.facebook.com',
        'Origin': 'https://business.facebook.com',
        'Connection': 'keep-alive',
    }

    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update({'cookie': cookie})

    print("[*] Checking cookie...")

    try:
        res = session.get('https://business.facebook.com/business_locations')
        if "checkpoint" in res.url or "login" in res.url:
            print("[!] Checkpoint detected! Waiting for manual approval...")
            return None

        token = None
        soup = BeautifulSoup(res.text, 'html.parser')
        for script in soup.find_all('script'):
            if 'EAAB' in script.text or 'EAAC' in script.text:
                start = script.text.find('EA')
                token = script.text[start:start+200].split('"')[0]
                break

        if token:
            print(f"\n\033[1;32m[✓] Token Extracted:\033[0m {token}\n")
            return token
        else:
            print("[×] Token not found in response.")
            return None
    except Exception as e:
        print(f"[×] Error during request: {str(e)}")
        return None

# Retry loop for checkpoint bypass
def retry_until_token(cookie, delay=5):
    while True:
        token = get_token_from_cookie(cookie)
        if token:
            with open("extracted_token.txt", "w") as f:
                f.write(token)
            print("[✓] Token saved to extracted_token.txt")
            break
        print(f"[!] Retrying in {delay} seconds...\n")
        time.sleep(delay)

# Main
if __name__ == '__main__':
    show_logo()
    user_cookie = input("\n[?] Enter your Facebook Cookie: ").strip()
    retry_until_token(user_cookie)
