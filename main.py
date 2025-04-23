from flask import Flask, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

# CONFIG
GROUP_ID = "9306787302780384"
ADMIN_UIDS = ["61573436296849"]
lock_active = False


def get_token():
    with open("token.txt", "r") as f:
        return f.read().strip()


def lock_group_name():
    global lock_active
    token = get_token()
    while lock_active:
        try:
            response = requests.post(
                f"https://graph.facebook.com/v20.0/{GROUP_ID}",
                data={
                    "access_token": token,
                    "name": "Locked by Broken Nadeem"
                }
            )
            print("Lock response:", response.text)
        except Exception as e:
            print("Error locking group name:", e)
        time.sleep(5)


@app.route("/", methods=["GET"])
def block_browser():
    return "Access Denied", 403


@app.route("/webhook", methods=["POST"])
def receive_command():
    global lock_active

    data = request.json
    try:
        messaging_event = data['entry'][0]['messaging'][0]
        sender_id = str(messaging_event['sender']['id'])
        message = messaging_event['message']['text'].strip().lower()
    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error", "message": "Invalid structure"})

    if sender_id not in ADMIN_UIDS:
        return jsonify({"status": "unauthorized"})

    if message == "start":
        return jsonify({"status": "success", "message": "Locker is ready"})

    elif message == "name lock":
        if not lock_active:
            lock_active = True
            threading.Thread(target=lock_group_name).start()
            return jsonify({"status": "started", "message": "Name lock initiated"})
        else:
            return jsonify({"status": "running", "message": "Name lock already active"})

    elif message == "reset":
        lock_active = False
        return jsonify({"status": "stopped", "message": "Locker reset"})

    return jsonify({"status": "ignored", "message": "Command not recognized"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
