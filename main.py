import json
import os
from twilio.rest import Client
import time

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        config = {
            "sid": input("Enter Your Twilio Account SID: ").strip(),
            "token": input("Enter Your Twilio Auth Token: ").strip(),
            "twilio_number": input("Enter Your Twilio Phone Number (+countrycode): ").strip()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return config

def send_sms(client, from_number, to_number, body):
    try:
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"[SENT] To {to_number}: {body}")
    except Exception as e:
        print(f"[FAILED] {e}")

def main():
    print("\n--- GLOBAL SMS SENDER (CONFIG ENABLED) BY BROKEN NADEEM ---\n")

    config = load_config()
    sid = config["sid"]
    token = config["token"]
    from_number = config["twilio_number"]

    to_number = input("Enter Target Phone Number (with +countrycode): ")
    name = input("Enter Your Name: ")
    hater = input("Enter Hater's Name: ")

    try:
        delay = float(input("Enter Delay Between Messages (in seconds): "))
    except:
        delay = 1.0

    message_file = input("Enter Path to Message File: ")

    try:
        with open(message_file, "r", encoding="utf-8") as f:
            messages = f.readlines()
            if not messages:
                print("Message file is empty!")
                return
    except:
        print("File not found!")
        return

    client = Client(sid, token)

    print("\nStarting to send messages...\n")
    for msg in messages:
        final_msg = msg.strip().replace("{name}", name).replace("{hater}", hater)
        send_sms(client, from_number, to_number, final_msg)
        time.sleep(delay)

if __name__ == "__main__":
    main()
