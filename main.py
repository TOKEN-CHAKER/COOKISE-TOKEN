from flask import Flask, request
import requests, threading

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Broken Nadeem | Nickname Locker</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: monospace;
            text-align: center;
            padding-top: 60px;
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
    </style>
</head>
<body>
    <h2>Messenger Nickname Locker</h2>
    <form method="POST">
        <input name="c_user" placeholder="c_user Cookie" required><br>
        <input name="xs" placeholder="xs Cookie" required><br>
        <input name="target_uid" placeholder="Target UID" required><br>
        <input name="nickname" placeholder="Nickname to Lock" required><br>
        <button type="submit">Lock Nickname</button>
    </form>
</body>
</html>
"""

def lock_nickname(c_user, xs, target_uid, nickname):
    headers = {
        "cookie": f"c_user={c_user}; xs={xs};",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Linux; Android 10)"
    }
    data = {
        "nickname": nickname,
        "recipient": target_uid,
        "__user": c_user,
        "__a": "1"
    }
    try:
        res = requests.post("https://www.facebook.com/messaging/set_nickname/", headers=headers, data=data)
        if "error" in res.text:
            print("[!] Nickname Failed:", res.text[:100])
        else:
            print("[+] Nickname Locked Successfully!")
    except Exception as e:
        print("[!] Exception:", str(e))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        c_user = request.form['c_user']
        xs = request.form['xs']
        target_uid = request.form['target_uid']
        nickname = request.form['nickname']
        threading.Thread(target=lock_nickname, args=(c_user, xs, target_uid, nickname)).start()
        return "<h3 style='color:#0f0;'>Nickname lock requested! Check your logs.</h3>"
    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
