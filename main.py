from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

group_id = "61573436296849"
nickname_lock = True
name_lock = True

# === Load Token & Get Admin UID ===
def load_token():
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            return f.read().strip()
    return ""

def get_admin_uid(token):
    url = f"https://graph.facebook.com/me?access_token={token}"
    res = requests.get(url).json()
    return res.get("id", "")

AUTHORIZED_UID = get_admin_uid(load_token())

# === Lock Functions ===
def set_nickname(token):
    url = f"https://graph.facebook.com/v20.0/{group_id}/participants/me/nickname"
    payload = {"nickname": "Locked by Broken Nadeem", "access_token": token}
    return requests.post(url, data=payload).json()

def set_group_name(token, name="Locked Group by Broken Nadeem"):
    url = f"https://graph.facebook.com/v20.0/{group_id}"
    payload = {"name": name, "access_token": token}
    return requests.post(url, data=payload).json()

def process_command(cmd, token):
    global nickname_lock, name_lock
    if cmd == "start":
        nickname_lock = True
        name_lock = True
        return {"status": "success", "message": "Locker started"}
    elif cmd == "reset":
        nickname_lock = False
        name_lock = False
        return {"status": "reset", "message": "Locker stopped"}
    elif cmd == "name lock":
        res1 = set_nickname(token)
        res2 = set_group_name(token)
        return {"status": "locked", "nickname_result": res1, "groupname_result": res2}
    elif cmd == "info":
        return {"status": "info", "nickname_lock": nickname_lock, "name_lock": name_lock}
    else:
        return {"status": "error", "message": f"Unknown command: {cmd}"}

# === Web UI ===
html_ui = '''
<!DOCTYPE html>
<html>
<head>
    <title>Group Name Locker</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; margin-top: 40px; }
        input, button { margin: 8px; padding: 10px; background: #111; color: #0f0; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>Messenger Group Locker</h1>
    <input type="text" id="uid" placeholder="Your Facebook UID"><br>
    <input type="text" id="command" placeholder="Command (start, name lock, reset, info)"><br>
    <button onclick="sendCommand()">Execute</button>
    <pre id="output"></pre>
<script>
function sendCommand() {
    fetch("/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            uid: document.getElementById("uid").value,
            command: document.getElementById("command").value
        })
    }).then(res => res.json())
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
    uid = data.get("uid")
    cmd = data.get("command")
    token = load_token()

    if uid != AUTHORIZED_UID:
        return jsonify({"status": "error", "message": "Unauthorized user!"})

    result = process_command(cmd, token)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
