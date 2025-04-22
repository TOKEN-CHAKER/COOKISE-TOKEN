import requests
import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print("<<< Messenger Group Name Lock v2 - Authorized Edition >>>")
    print("        Coded & Modified by Broken Nadeem")
    print("-" * 60)

def validate_token(token):
    try:
        url = f"https://graph.facebook.com/me?access_token={token}"
        r = requests.get(url)
        data = r.json()
        if "id" in data:
            print(f"[+] Token valid for user: {data['name']} ({data['id']})")
            return data['id']
        else:
            print("[-] Invalid access token.")
            return None
    except Exception as e:
        print("[-] Token check failed:", e)
        return None

def lock_group_name(token, group_id, uid, lock_name):
    url = f"https://graph.facebook.com/{group_id}/participants/{uid}"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'nickname': lock_name}

    while True:
        r = requests.post(url, headers=headers, data=payload)
        if "error" not in r.text:
            print(f"[+] Group name successfully locked to: {lock_name}")
            break
        else:
            print("[-] Lock failed or no access to group. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    banner()
    token = input("[+] Enter your access token: ").strip()
    uid = input("[+] Enter your UID (allowed to change name): ").strip()
    group_id = input("[+] Enter Messenger Group UID: ").strip()
    lock_name = input("[+] Enter group name to lock: ").strip()

    print("\n[*] Activating smart lock system...")

    if validate_token(token):
        lock_group_name(token, group_id, uid, lock_name)
