from flask import Flask, request
import requests, threading, time

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Broken Nadeem | Group Nickname Lock</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: monospace;
            text-align: center;
            padding-top: 50px;
        }
        input, button {
            padding: 10px;
            margin: 8px;
            background-color: #111;
            border: 1px solid #0f0;
            color: #0f0;
            border-radius: 5px;
        }
        button:hover {
            background-color: #0f0;
            color: #000;
        }
        #loading {
            margin-top: 20px;
            font-weight: bold;
            display: none;
        }
    </style>
</head>
<body>
    <h2>Group Nickname Lock - Broken Nadeem</h2>
    <form method="POST" onsubmit="startLoading()">
        <input name="access_token" placeholder="Enter Access Token" required><br>
        <input name="your_uid" placeholder="Enter Your UID" required><br>
        <input name="group_uid" placeholder="Enter Group UID" required><br>
        <input name="nickname" placeholder="Nickname to Lock" required><br>
        <button type="submit">Lock Nickname</button>
    </form>

    <div id="loading">
        <p>Worming started... Terminal logs will show live status</p>
    </div>

    <script>
        function startLoading() {
            document.getElementById("loading").style.display = "block";
        }
    </script>
</body>
</html>
"""

def set_nickname(access_token, group_uid, nickname):
    url = f"https://graph.facebook.com/v19.0/{group_uid}/nicknames"
    payload = {
        "nickname": nickname,
        "access_token": access_token
    }
    res = requests.post(url, data=payload)
    return res.json()

def monitor_nickname(access_token, group_uid, your_uid, nickname):
    print("[*] Monitoring started...")
    last_nick = ""
    while True:
        try:
            url = f"https://graph.facebook.com/v19.0/{group_uid}?fields=thread_nickname&access_token={access_token}"
            res = requests.get(url).json()

            current_uid = res.get("thread_nickname", {}).get("setting_actor", "")
            current_nick = res.get("thread_nickname", {}).get("nickname", "")

            if current_nick != nickname:
                print(f"[!] Nickname changed to '{current_nick}' by UID {current_uid}")
                if current_uid != your_uid:
                    print("[!] Unauthorized change detected. Re-locking nickname...")
                    set_nickname(access_token, group_uid, nickname)
                else:
                    print("[+] Change allowed by owner.")
            else:
                print("[+] Nickname still locked.")

        except Exception as e:
            print(f"[!] Error: {e}")
        time.sleep(5)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        your_uid = request.form['your_uid']
        group_uid = request.form['group_uid']
        nickname = request.form['nickname']

        threading.Thread(target=monitor_nickname, args=(access_token, group_uid, your_uid, nickname)).start()
        return "<h3 style='color:#0f0;'>Nickname lock worm started! Check terminal logs for updates.</h3>"

    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
