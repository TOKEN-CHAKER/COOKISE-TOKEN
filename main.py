from flask import Flask, request
from playwright.sync_api import sync_playwright
import threading

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
            page.goto(group_url, timeout=60000)
            page.wait_for_timeout(10000)

            page.click("text=Chat Settings")
            page.wait_for_timeout(2000)

            page.click("text=Nicknames")
            page.wait_for_timeout(2000)

            page.click(f"[href*='{target_uid}']")
            page.wait_for_timeout(1000)

            page.fill('input[placeholder="Enter nickname"]', nickname)
            page.click("text=Save")
            page.wait_for_timeout(2000)

            print("[+] Nickname locked successfully!")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            browser.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        threading.Thread(target=lock_nickname, args=(
            data['c_user'], data['xs'], data['group_url'],
            data['target_uid'], data['nickname']
        )).start()
        return "<h2 style='color:#0f0;background:#111;padding:10px;'>Nickname lock started! Check logs in Termux.</h2>"
    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
