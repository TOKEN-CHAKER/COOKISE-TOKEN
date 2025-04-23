from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# === Admin UID Loader ===
def get_admin_uids():
    if not os.path.exists("admin_uids.txt"):
        return []
    with open("admin_uids.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# === Group Lock System ===
group_id = "YOUR_GROUP_THREAD_ID"  # <- Yahan apna group thread ID lagao
nickname_lock = True
name_lock = True

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
        return {"status": "success", "message": "Locker Started"}
    elif cmd == "name lock":
        res1 = set_nickname(token)
        res2 = set_group_name(token)
        return {"status": "locked", "nickname": res1, "name": res2}
    elif cmd == "reset":
        nickname_lock = False
        name_lock = False
        return {"status": "reset", "message": "Locks Removed"}
    else:
        return {"status": "error", "message": "Unknown command"}

# === HTML UI ===
html_ui = '''
<!DOCTYPE html>
<html>
<head>
  <title>Nickname Locker Tool</title>
  <style>
    body {
      background: #000;
      color: #00ffcc;
      font-family: monospace;
      padding-top: 60px;
      text-align: center;
    }
    input, button {
      background: #111;
      color: #00ffcc;
      padding: 10px;
      margin: 5px;
      border: 1px solid #00ffcc;
    }
    .container {
      animation: glow 2s infinite alternate;
    }
    @keyframes glow {
      from { text-shadow: 0 0 5px #00ffcc; }
      to { text-shadow: 0 0 15px #00ffcc, 0 0 25px #00ffcc; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Nickname & Group Name Locker</h1>
    <input type="text" id="token" placeholder="Access Token">
    <input type="text" id="uid" placeholder="Your Facebook UID">
    <input type="text" id="command" placeholder="Command (start, name lock, reset)">
    <button onclick="sendCommand()">Send Command</button>
    <pre id="response"></pre>
  </div>

  <script>
    function sendCommand() {
      fetch("/command", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          command: document.getElementById("command").value,
          token: document.getElementById("token").value,
          uid: document.getElementById("uid").value
        })
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("response").innerText = JSON.stringify(data, null, 2);
      });
    }
  </script>
</body>
</html>
'''

# === Flask Routes ===
@app.route("/")
def home():
    return render_template_string(html_ui)

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    cmd = data.get("command")
    token = data.get("token")
    uid = data.get("uid")

    if uid not in get_admin_uids():
        return jsonify({"status": "error", "message": "Unauthorized: Not an admin!"})

    result = process_command(cmd, token)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
