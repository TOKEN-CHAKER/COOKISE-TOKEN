import requests
import re

BANNER = """
\033[1;32m
██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔═══╝ ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██║     ██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝

         Facebook Cookie Token Extractor
                Coded by Broken Nadeem
\033[0m
"""

def extract_token(cookie):
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/89.0 Safari/537.36"
    }
    try:
        response = requests.get("https://business.facebook.com/business_locations", headers=headers)
        token = re.search(r'EAAG\w+', response.text)
        if token:
            return token.group(0)
        else:
            return None
    except Exception as e:
        print(f"\033[1;31m[!] Error while requesting: {str(e)}\033[0m")
        return None

def main():
    print(BANNER)
    cookie = input("\033[1;36m[+] Paste your Facebook Cookie:\033[0m ").strip()
    print("\n\033[1;33m[*] Extracting token... Please wait...\033[0m\n")

    token = extract_token(cookie)

    if token:
        print(f"\033[1;32m[✓] Token Found:\033[0m {token}")
    else:
        print("\033[1;31m[✗] Token not found. Invalid or checkpointed cookie.\033[0m")

if __name__ == '__main__':
    main()
