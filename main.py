import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
╔════════════════════════════════════════════╗
║         HATER MESSAGE SPAMMER TOOL        ║
║            By: Broken Nadeem              ║
╚════════════════════════════════════════════╝
""")

def send_message_simulation(phone, name, hater, delay, messages):
    count = 0
    for msg in messages:
        count += 1
        final_msg = msg.strip().replace("{name}", name).replace("{hater}", hater)
        print(f"[{count}] SENT to {phone}: {final_msg}")
        time.sleep(delay)

def main():
    clear()
    banner()

    phone = input("Enter Target Phone Number: ")
    name = input("Enter Your Name: ")
    hater = input("Enter Hater's Name: ")

    try:
        delay = float(input("Enter Delay Between Messages (in seconds): "))
    except ValueError:
        print("Invalid speed! Using default 1 second.")
        delay = 1.0

    file_path = input("Enter Path to Message File: ")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            messages = f.readlines()
            if not messages:
                print("\n[!] Message file is empty!")
                return
    except FileNotFoundError:
        print("\n[!] File not found!")
        return

    print(f"\n[+] Sending messages to {phone}...\n")
    send_message_simulation(phone, name, hater, delay, messages)

if __name__ == "__main__":
    main()
