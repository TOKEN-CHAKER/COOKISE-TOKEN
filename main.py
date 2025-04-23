from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# === Group Settings ===
group_id = "YOUR_GROUP_THREAD_ID"  # <- Yahan apna Facebook group thread ID lagao
nickname_lock = True
name_lock = True

# === Admin UID Loader ===
def get_admin_uids():
    if not os.path.exists("admin_uids.txt"):
        return []
    with open("admin_uids.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

# === Lock Functions ===
def set_nickname(token):
    url = f"https://graph.facebook.com/v20.0/{group_id}/participants/me/nickname"
    payload = {
        "nickname": "Locked by Broken Nadeem",
        "access_token": token
    }
    return requests.post(url, data=payload).json()

def set_group_name(token, name="Locked Group by Broken Nadeem"):
    url = f"https://graph.facebook.com/v20.0/{group_id}"
    payload = {
        "name": name,
        "access_token": token
    }
    return requests.post(url, data=payload).json()

def process_command(cmd, token):
    global nickname_lock, name_lock
    if cmd == "start":
        nickname_lock = True
        name_lock = True
        return {"status": "success", "message": "Locker started"}
    elif cmd == "name lock":
        res1 = set_nickname(token)
        res2 = set_group_name(token)
        return {"status": "locked", "nickname_result": res1, "groupname_result": res2}
    elif cmd == "reset":
        nickname_lock = False
        name_lock = False
        return {"status": "reset", "message": "Locker reset"}
    else:
        return {"status": "error", "message": "Unknown command"}

# === Web UI ===
html_ui = '''
<!DOCTYPE html>
<html>
<head>
    <title>Locker Panel</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; margin-top: 50px; }
        input, button { margin: 10px; padding: 10px; background: #111; color: #0f0; border: 1px solid #0f0; }
        .glow { animation: glow 1s infinite alternate; }
        @keyframes glow {
            from { text-shadow: 0 0 5px #0f0; }
            to { text-shadow: 0 0 20px #0f0; }
        }
    </style>
</head>
<body>
    <div class="glow">
        <h1>Nickname & Group Locker</h1>
        <input type="text" id="token" placeholder="Access Token"><br>
        <input type="text" id="uid" placeholder="Your Facebook UID"><br>
        <input type="text" id="command" placeholder="Command (start, name lock, reset)"><br>
        <button onclick="sendCommand()">Execute</button>
        <pre id="output"></pre>
    </div>
<script>
function sendCommand() {
    fetch("/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            token: document.getElementById("token").value,
            uid: document.getElementById("uid").value,
            command: document.getElementById("command").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = JSON.stringify(data, null, 2);
    });
}
</script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(html_ui)

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    token = data.get("token")
    uid = data.get("uid")
    cmd = data.get("command")

    if uid not in get_admin_uids():
        return jsonify({"status": "error", "message": "Unauthorized user!"})

    result = process_command(cmd, token)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
