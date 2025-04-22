from twilio.rest import Client
import time

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
    print("\n--- GLOBAL SMS SPAMMER BY BROKEN NADEEM ---\n")

    account_sid = input("Enter Your Twilio Account SID: ")
    auth_token = input("Enter Your Twilio Auth Token: ")
    from_number = input("Enter Your Twilio Phone Number (with +countrycode): ")
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

    client = Client(account_sid, auth_token)

    print("\nStarting to send messages...\n")
    for msg in messages:
        final_msg = msg.strip().replace("{name}", name).replace("{hater}", hater)
        send_sms(client, from_number, to_number, final_msg)
        time.sleep(delay)

if __name__ == "__main__":
    main()
