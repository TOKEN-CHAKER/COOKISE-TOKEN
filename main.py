import requests
import time
import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def slow_print(msg):
    for c in msg:
        print(c, end='', flush=True)
        time.sleep(0.02)
    print()

def get_group_name(convo_id, token):
    url = f'https://graph.facebook.com/v19.0/{convo_id}?fields=name&access_token={token}'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get('name')
    return None

def get_last_changer(convo_id, token):
    url = f'https://graph.facebook.com/v19.0/{convo_id}/messages?limit=5&access_token={token}'
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json().get('data', [])
        for msg in data:
            if 'changed the name' in msg.get('message', ''):
                return msg.get('from', {}).get('id')
    return None

def set_group_name(convo_id, token, name):
    url = f'https://graph.facebook.com/v19.0/{convo_id}'
    payload = {
        'name': name,
        'access_token': token
    }
    res = requests.post(url, data=payload)
    return res.status_code == 200

def lock_loop(convo_id, token, locked_name, allowed_uid):
    while True:
        current_name = get_group_name(convo_id, token)
        if current_name and current_name != locked_name:
            changer_uid = get_last_changer(convo_id, token)
            if changer_uid and changer_uid != allowed_uid:
                print(f"[!] Unauthorized name change by UID {changer_uid} — restoring...")
                set_group_name(convo_id, token, locked_name)
            else:
                print("[=] Name changed by authorized user, no action taken.")
        else:
            print("[=] Name is locked correctly.")
        time.sleep(10)

if __name__ == '__main__':
    clear()
    slow_print("    <<< Messenger Group Name Lock v2 - Authorized Edition >>>\n")

    token = input("[+] Enter your access token: ")
    allowed_uid = input("[+] Enter your UID (allowed to change name): ")
    convo_id = input("[+] Enter Messenger Group UID: ")
    locked_name = input("[+] Enter group name to lock: ")

    slow_print("\n[*] Activating smart lock system...")
    time.sleep(1)

    current_name = get_group_name(convo_id, token)
    if current_name:
        set_group_name(convo_id, token, locked_name)
        slow_print("\n[+] Name Lock Activated with Authorized Control!")
        print("[*] Monitoring name changes...\n")
        lock_loop(convo_id, token, locked_name, allowed_uid)
    else:
        print("[-] Failed to fetch group info. Check token or UID.")
