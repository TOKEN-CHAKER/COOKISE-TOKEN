import requests
from bs4 import BeautifulSoup
import time

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

    print("Checking cookie...")

    try:
        res = session.get('https://business.facebook.com/business_locations')
        if "checkpoint" in res.url or "login" in res.url:
            print("Checkpoint detected! Waiting for manual approval...")
            return None

        token = None
        soup = BeautifulSoup(res.text, 'html.parser')
        for script in soup.find_all('script'):
            if 'EAAB' in script.text or 'EAAC' in script.text:
                start = script.text.find('EA')
                token = script.text[start:start+200].split('"')[0]
                break

        if token:
            print(f"[✓] Token Extracted: {token}")
            return token
        else:
            print("[×] Token not found in response.")
            return None
    except Exception as e:
        print("[×] Error during request:", str(e))
        return None

def retry_until_token(cookie, delay=5):
    while True:
        token = get_token_from_cookie(cookie)
        if token:
            break
        time.sleep(delay)

if __name__ == '__main__':
    user_cookie = input("Enter your Facebook Cookie: ").strip()
    retry_until_token(user_cookie)
