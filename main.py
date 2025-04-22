import requests
import time

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE'
CONVO_ID = 'YOUR_CONVERSATION_ID_HERE'
LOCKED_NAME = 'Aliya x Nadeem'  # jo naam lock karna hai

def get_group_name():
    url = f'https://graph.facebook.com/v19.0/{CONVO_ID}?fields=name&access_token={ACCESS_TOKEN}'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get('name')
    else:
        print("[-] Error fetching group name:", res.text)
        return None

def set_group_name(name):
    url = f'https://graph.facebook.com/v19.0/{CONVO_ID}'
    payload = {
        'name': name,
        'access_token': ACCESS_TOKEN
    }
    res = requests.post(url, data=payload)
    if res.status_code == 200:
        print(f"[+] Group name reset to: {name}")
    else:
        print("[-] Failed to set name:", res.text)

def lock_loop():
    while True:
        current_name = get_group_name()
        if current_name and current_name != LOCKED_NAME:
            print(f"[!] Name changed to '{current_name}' - resetting...")
            set_group_name(LOCKED_NAME)
        else:
            print("[=] Name is locked correctly.")
        time.sleep(10)  # Check every 10 seconds

if __name__ == '__main__':
    print("[*] Messenger Group Name Lock Started...")
    lock_loop()
