from flask import Flask, request
import requests, threading, time

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Broken Nadeem | Nickname Worm Locker</title>
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
        .worm {
            font-size: 20px;
            animation: blink 1s infinite;
            color: #0f0;
        }
        @keyframes blink {
            0%   {opacity: 1;}
            50%  {opacity: 0.2;}
            100% {opacity: 1;}
        }
    </style>
</head>
<body>
    <h2>Messenger Nickname Worm Locker</h2>
    <form method="POST" onsubmit="startLoading()">
        <input name="c_user" placeholder="c_user Cookie" required><br>
        <input name="xs" placeholder="xs Cookie" required><br>
        <input name="target_uid" placeholder="Target UID" required><br>
        <input name="nickname" placeholder="Nickname to Lock" required><br>
        <button type="submit">Lock Nickname</button>
    </form>

    <div id="loading">
        <div class="worm">Worming in progress... Broken Nadeem style</div>
        <div class="worm">[█████-----] Trying to lock...</div>
        <div class="worm">Terminal Logs: Check console</div>
    </div>

    <script>
        function startLoading() {
            document.getElementById("loading").style.display = "block";
        }
    </script>
</body>
</html>
"""

def worm_lock(c_user, xs, target_uid, nickname):
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

    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            res = requests.post("https://www.facebook.com/messaging/set_nickname/", headers=headers, data=data)
            if "error" not in res.text and "Successfully" in res.text or res.status_code == 200:
                print(f"[+] Nickname Locked Successfully in attempt {attempt + 1}")
                break
            else:
                print(f"[!] Attempt {attempt + 1} failed... retrying")
        except Exception as e:
            print(f"[!] Error at attempt {attempt + 1}: {e}")
        time.sleep(1)  # Safe delay

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        c_user = request.form['c_user']
        xs = request.form['xs']
        target_uid = request.form['target_uid']
        nickname = request.form['nickname']
        threading.Thread(target=worm_lock, args=(c_user, xs, target_uid, nickname)).start()
        return "<h3 style='color:#0f0;'>Nickname worming started! Check terminal logs for success.</h3>"
    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
