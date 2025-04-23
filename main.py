from flask import Flask, request
from playwright.sync_api import sync_playwright
import threading, time

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Broken Nadeem | Nickname Locker</title>
</head>
<body style="background:#000;color:#00FF00;font-family:monospace;text-align:center;padding-top:40px;">
    <h2>Messenger Nickname Locker</h2>
    <form method="POST">
        <input name="c_user" placeholder="c_user Cookie" required><br><br>
        <input name="xs" placeholder="xs Cookie" required><br><br>
        <input name="group_url" placeholder="Messenger Group URL" required><br><br>
        <input name="target_uid" placeholder="Target UID" required><br><br>
        <input name="nickname" placeholder="Nickname to Lock" required><br><br>
        <button type="submit" style="padding: 10px 20px;">Lock Nickname</button>
    </form>
</body>
</html>
"""

def lock_nickname(c_user, xs, group_url, target_uid, nickname):
    cookies = [
        {"name": "c_user", "value": c_user, "domain": ".facebook.com", "path": "/"},
        {"name": "xs", "value": xs, "domain": ".facebook.com", "path": "/"},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()

        try:
            print("[*] Navigating to Messenger group...")
            page.goto(group_url)
            time.sleep(10)

            print("[*] Opening chat settings...")
            page.click("text=Chat Settings")
            time.sleep(2)

            print("[*] Opening Nicknames section...")
            page.click("text=Nicknames")
            time.sleep(2)

            print("[*] Selecting user...")
            page.click(f"[href*='{target_uid}']")
            time.sleep(1)

            print(f"[*] Locking nickname: {nickname}")
            page.fill('input[placeholder=\"Enter nickname\"]', nickname)
            page.click("text=Save")
            time.sleep(2)

            print("[+] Nickname locked successfully!")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            browser.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        c_user = request.form['c_user']
        xs = request.form['xs']
        group_url = request.form['group_url']
        target_uid = request.form['target_uid']
        nickname = request.form['nickname']
        threading.Thread(target=lock_nickname, args=(c_user, xs, group_url, target_uid, nickname)).start()
        return "<h2 style='color:#0f0;background:#111;padding:10px;'>Nickname lock started! Check Termux logs.</h2>"
    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
