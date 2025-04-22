import requests
import time

def check_token_validity(token):
    url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
    res = requests.get(url).json()
    return res.get("id"), res.get("name")

def has_group_access(token, group_id):
    url = f"https://graph.facebook.com/v18.0/{group_id}?fields=name,participants&access_token={token}"
    res = requests.get(url).json()
    return "id" in res

def change_group_name(token, group_id, new_name):
    url = f"https://graph.facebook.com/v18.0/{group_id}"
    payload = {
        "name": new_name,
        "access_token": token
    }
    res = requests.post(url, data=payload).json()
    return "success" in res and res["success"]

def lock_group_name():
    print("<<< Messenger Group Name Lock v2 - Authorized Edition >>>")
    token = input("[+] Enter your access token: ").strip()
    uid = input("[+] Enter your UID (allowed to change name): ").strip()
    group_id = input("[+] Enter Messenger Group UID: ").strip()
    new_name = input("[+] Enter group name to lock: ").strip()

    print("\n[*] Activating smart lock system...")
    time.sleep(1)

    user_id, user_name = check_token_validity(token)
    if not user_id:
        print("[-] Invalid token. Please check and try again.")
        return
    if user_id != uid:
        print(f"[-] UID does not match token owner. Your UID: {user_id}")
        return

    if not has_group_access(token, group_id):
        print("[-] Invalid Messenger Group UID or no access. Check again.")
        return

    print(f"[+] Token valid for user: {user_name} ({user_id})")
    time.sleep(0.5)
    print(f"[*] Locking group name to: {new_name} ...")
    time.sleep(1)

    success = change_group_name(token, group_id, new_name)
    if success:
        print(f"[+] Group name successfully locked as: {new_name}")
        print("[*] Smart Lock Activated by Broken Nadeem.")
    else:
        print("[-] Failed to change group name. Possible permission error.")

if __name__ == "__main__":
    lock_group_name()
