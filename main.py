import requests
import time
import os

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("<<< Messenger Group Name Lock v2 - Authorized Edition >>>")
    print("        Coded & Modified by Broken Nadeem")
    print("------------------------------------------------------------")

def validate_token(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    res = requests.get(url).json()
    if "id" in res:
        print(f"[+] Token valid for user: {res['name']} ({res['id']})")
        return res['id']
    else:
        print("[-] Invalid token.")
        return None

def lock_name_loop(token, thread_id, uid, lock_name):
    url = f"https://graph.facebook.com/v18.0/{thread_id}/participants/{uid}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'nickname': lock_name
    }

    while True:
        r = requests.post(url, headers=headers, data=data)
        res = r.json()

        if "error" not in res:
            print(f"[+] Group name locked to: {lock_name}")
            break
        else:
            print("[-] Failed to lock. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    banner()
    token = input("[+] Enter your access token: ").strip()
    uid = input("[+] Enter your UID (allowed to change name): ").strip()
    thread_id = input("[+] Enter Messenger Group UID: ").strip()
    lock_name = input("[+] Enter group name to lock: ").strip()

    print("\n[*] Activating smart lock system...")
    if validate_token(token):
        lock_name_loop(token, thread_id, uid, lock_name)
