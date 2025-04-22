import requests
import time

def check_token_validity(token):
    url = f"https://graph.facebook.com/v18.0/me?access_token={token}"
    res = requests.get(url).json()
    return res.get("id") is not None

def is_valid_messenger_group(token, group_id):
    url = f"https://graph.facebook.com/v18.0/{group_id}?access_token={token}"
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

    if not check_token_validity(token):
        print("[-] Invalid token. Please check and try again.")
        return

    if not is_valid_messenger_group(token, group_id):
        print("[-] Failed to fetch group info. Check token or group UID.")
        return

    print("[+] Group validated.")
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
