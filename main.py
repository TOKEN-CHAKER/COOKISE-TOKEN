import requests
import time
import sys

def log(text):
    for c in text + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)

def get_group_user_info(token, thread_id, uid):
    url = f"https://graph.facebook.com/v19.0/{thread_id}/participants"
    params = {
        "access_token": token
    }

    log("\n[+] Fetching group participants...")
    res = requests.get(url, params=params)

    if res.status_code != 200:
        log(f"[-] Failed to fetch participants: {res.json().get('error', {}).get('message', 'Unknown Error')}")
        return

    data = res.json().get("data", [])
    found = False

    for user in data:
        if user.get("id") == uid:
            found = True
            name = user.get("name", "Unknown")
            nickname = user.get("nickname", "No Nickname")
            log("\n[✓] User Found in Group!")
            log(f"    [•] Name     : {name}")
            log(f"    [•] Nickname : {nickname}")
            break

    if not found:
        log("\n[!] User not found in the group participants.")

def main():
    log("\n==== Facebook Group User Logger ====\n")
    token = input("[+] Enter Access Token: ").strip()
    thread_id = input("[+] Enter Messenger Thread ID (Group ID): ").strip()
    uid = input("[+] Enter Target User UID: ").strip()

    get_group_user_info(token, thread_id, uid)

if __name__ == "__main__":
    main()
