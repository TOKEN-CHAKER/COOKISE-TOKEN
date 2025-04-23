from playwright.sync_api import sync_playwright
import time

def lock_nickname(c_user, xs, group_url, target_uid, nickname):
    cookies = [
        {"name": "c_user", "value": c_user, "domain": ".facebook.com", "path": "/"},
        {"name": "xs", "value": xs, "domain": ".facebook.com", "path": "/"},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        context.add_cookies(cookies)
        page = context.new_page()

        print("[*] Opening Messenger thread...")
        page.goto(group_url)
        time.sleep(10)

        print("[*] Opening group settings...")
        page.click("text=Chat Settings")
        time.sleep(2)

        print("[*] Searching for UID...")
        page.click("text=Nicknames")
        time.sleep(2)

        selector = f"[href*='{target_uid}']"
        page.click(selector)
        time.sleep(1)

        print(f"[*] Setting nickname: {nickname}")
        page.fill('input[placeholder="Enter nickname"]', nickname)
        page.click("text=Save")
        time.sleep(3)

        print("[+] Nickname locked successfully!")
        browser.close()

# === USER INPUT SECTION ===
c_user = input("Enter your c_user cookie: ").strip()
xs = input("Enter your xs cookie: ").strip()
group_url = input("Enter Messenger group URL (like https://www.messenger.com/t/12345678): ").strip()
target_uid = input("Enter UID of the user to lock nickname: ").strip()
nickname = input("Enter nickname to lock: ").strip()

lock_nickname(c_user, xs, group_url, target_uid, nickname)
