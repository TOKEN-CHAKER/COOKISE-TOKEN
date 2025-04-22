import requests
import time
import os

def check_token_validity(token):
    try:
        url = f"https://graph.facebook.com/me?access_token={token}"
        res = requests.get(url).json()
        return res.get("id")
    except:
        return None

def is_valid_messenger_group(token, group_id):
    try:
        url = f"https://graph.facebook.com/{group_id}?access_token={token}"
        res = requests.get(url).json()
        return res.get("id")
    except:
        return None

def change_group_name(token, group_id, new_name):
    try:
        url = f"https://graph.facebook.com/{group_id}"
        payload = {
            "name": new_name,
            "access_token": token
        }
        res = requests.post(url, data=payload).json()
        return res.get("success") == True
    except:
        return False

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def lock_group_name():
    clear()
    print("<<< Messenger Group Name Lock v2 - Authorized Edition >>>\n")

    token = input("[+] Enter your access token: ").strip()
    uid = input("[+] Enter your UID (allowed to change name): ").strip()
    group_id = input("[+] Enter Messenger Group UID: ").strip()
    new_name = input("[+] Enter group name to lock: ").strip()

    print("\n[*] Activating smart lock system...")
    time.sleep(1)

    user_id = check_token_validity(token)
    if not user_id:
        print("[-] Invalid access token. Please try again.")
        return
    
    if user_id != uid:
        print("[-] UID doesn't match the token owner. Access denied.")
        return

    if not is_valid_messenger_group(token, group_id):
        print("[-] Invalid Messenger Group UID or no access. Check again.")
        return

    print("[+] Token and Group validated.")
    time.sleep(0.5)

    print(f"[*] Locking group name to: {new_name}")
    time.sleep(1)

    if change_group_name(token, group_id, new_name):
        print(f"[+] Group name successfully locked as: {new_name}")
        print("[*] Smart Lock Activated by Broken Nadeem.")
    else:
        print("[-] Failed to lock group name. Maybe token has no permission.")

if __name__ == "__main__":
    lock_group_name()
