import requests
import re
import time
import os

def show_logo():
    os.system('clear')
    print("""
\033[1;32m╔══════════════════════════════════════╗
║         𝗕𝗿𝗼𝗸𝗲𝗻 𝗡𝗮𝗱𝗲𝗲𝗺 𝗧𝗼𝗸𝗲𝗻 𝗧𝗼𝗼𝗹         ║
╠══════════════════════════════════════╣
║  FB Token Extractor | Termux Ready   ║
║     Status: CHECKPOINT SAFE          ║
╚══════════════════════════════════════╝
\033[0m""")

def extract_token_from_cookies(cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile)",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie,
    }

    try:
        response = requests.get(
            "https://business.facebook.com/business_locations", headers=headers
        )
        access_token = re.search(r"EAAG\w+", response.text)
        if access_token:
            token = access_token.group(0)
            print("\n\033[1;32m[✓] Successfully Token Generated:\033[0m\n", token)
            with open("token.txt", "w") as f:
                f.write(token)
            return True
        elif "checkpoint" in response.text.lower():
            print("\033[1;33m[!] Checkpoint Detected! Please Approve Manually...\033[0m")
            return False
        else:
            print("\033[1;31m[×] Invalid Cookies or Token Not Found.\033[0m")
            return False
    except Exception as e:
        print("\033[1;31m[!] Error:\033[0m", e)
        return False

def main():
    show_logo()
    cookie = input("\n\033[1;36m[Input] Paste Your Facebook Cookies:\033[0m\n> ").strip()

    while True:
        success = extract_token_from_cookies(cookie)
        if success:
            print("\033[1;32m[✓] Token Saved to token.txt\033[0m")
            break
        else:
            print("\033[1;34m[~] Retrying in 5 seconds...\033[0m")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupted by user. Exiting...\033[0m")
