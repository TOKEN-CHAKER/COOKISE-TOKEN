from flask import Flask, request, render_template_string import requests, threading, time

app = Flask(name)

ADMIN_UID = "61573436296849" GROUP_ID = "<YOUR_GROUP_ID>"  # Replace with your group ID ACCESS_TOKEN = "<YOUR_ACCESS_TOKEN>"  # Replace with your group access token

status = { "bot_active": False, "lock_active": False, "nickname": "", "target_uid": "", "cookies": {} }

HTML_TEMPLATE = """

<!DOCTYPE html><html>
<head>
    <title>Broken Nadeem | Animated Nickname Locker</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            padding: 40px;
        }
        h1, h3 {
            animation: glow 1s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #0f0; }
            to { text-shadow: 0 0 20px #0f0, 0 0 30px #0f0; }
        }
        .status {
            margin-top: 20px;
            font-size: 20px;
            color: cyan;
        }
    </style>
</head>
<body>
    <h1>Broken Nadeem Nickname Worm Locker</h1>
    <div class="status">
        <p>Bot Active: {{ bot_active }}</p>
        <p>Locking: {{ lock_active }}</p>
        <p>Target UID: {{ target_uid }}</p>
        <p>Nickname: {{ nickname }}</p>
    </div>
</body>
</html>
"""def set_nickname(): headers = { "cookie": f"c_user={status['cookies']['c_user']}; xs={status['cookies']['xs']};", "content-type": "application/x-www-form-urlencoded", "user-agent": "Mozilla/5.0 (Linux; Android 10)" } data = { "nickname": status['nickname'], "recipient": status['target_uid'], "__user": status['cookies']['c_user'], "__a": "1" } while status['lock_active']: try: res = requests.post("https://www.facebook.com/messaging/set_nickname/", headers=headers, data=data) if "error" not in res.text: print("[+] Nickname Locked Successfully") else: print("[-] Nickname lock attempt failed") except Exception as e: print(f"[!] Exception: {e}") time.sleep(2)

def command_listener(): print("[+] Command listener started") url = f"https://graph.facebook.com/{GROUP_ID}/feed?access_token={ACCESS_TOKEN}" last_checked = "" while True: try: res = requests.get(url).json() data = res.get("data", []) if data: latest = data[0] if latest['id'] != last_checked: last_checked = latest['id'] message = latest.get('message', '').lower() sender = latest.get('from', {}).get('id', '') if sender == ADMIN_UID: if "start" in message: status['bot_active'] = True print("[+] Bot started") elif "name lock" in message and status['bot_active']: status['lock_active'] = True print("[*] Nickname locking initiated") threading.Thread(target=set_nickname).start() elif "reset" in message: status['bot_active'] = False status['lock_active'] = False print("[!] System reset by admin") except Exception as e: print(f"[!] Listener error: {e}") time.sleep(5)

@app.route('/') def index(): return render_template_string(HTML_TEMPLATE, **status)

@app.route('/configure', methods=['POST']) def configure(): status['cookies'] = { 'c_user': request.form['c_user'], 'xs': request.form['xs'] } status['nickname'] = request.form['nickname'] status['target_uid'] = request.form['target_uid'] return "Configured!"

if name == 'main': threading.Thread(target=command_listener).start() app.run(host='0.0.0.0', port=5000)

