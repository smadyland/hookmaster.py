import dhooks
import requests
import json
import random
import string
import time
import os

def webhook_gen():
    def generate_random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    channel_id = input('Enter the webhooks channel ID: ')
    num_webhooks = int(input('Enter the number of webhooks to create (max 15): '))
    webhook_name = input('Enter the name for the webhooks (press enter for default): ')

    url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
    headers = {"Content-Type": "application/json", "Authorization": "Bot <YOUR_BOT_TOKEN>"}

    for i in range(num_webhooks):
        if webhook_name:
            name = webhook_name
        else:
            name = generate_random_string(8)
        payload = {"name": name}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"Failed to create webhook: {response.text}")
        else:
            response_json = response.json()
            webhook_id = response_json["id"]
            webhook_token = response_json["token"]

            webhook_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
            print(f"Successfully created webhook: {webhook_url}")

            with open("webhooks.txt", "a") as f:
                f.write(webhook_url + "\n")
                time.sleep(5)
    print("Wrote webhook URL to webhooks.txt successfully!")

def message_send():
with open('webhooks.txt', 'r') as f:
    webhook_links = [line.strip() for line in f.readlines()]

message = input("What would you like the webhooks to say?: ")
    messages_per_second = float(input("How many messages per second? (default = 1, 0 for instant): ") or 1)

    if messages_per_second == 0:
        while True:
            for link in webhook_links:
                hook = dhooks.Webhook(link)
                hook.send(message)
    else:
        delay = 1.0 / messages_per_second
        while True:
            for link in webhook_links:
                hook = dhooks.Webhook(link)
                hook.send(message)
            time.sleep(delay)

def run_script(num):
    if num == 1:
        webhook_gen()
    elif num == 2:
        message_send()
    elif num == 0:
        print("Exiting the program")
        time.sleep(0.4)
        exit()
    else:
        print("Invalid option")

while True:
    print("""
|              |                   |                         
|---.,---.,---.|__/ ,-.-.,---.,---.|--- ,---.,---. ,---.,   .
|   ||   ||   ||  \ | | |,---|`---.|    |---'|     |   ||   |
`   '`---'`---'`   `` ' '`---^`---'`---'`---'`    o|---'`---|
                                                   |    `---'
                                                   """)
    print("Enter 1 to execute the webhook generator")
    print("Enter 2 to execute the message flooder")
    print("Enter 0 to exit the program")

    user_input = int(input("Enter your selection: "))
    run_script(user_input)

    input("Press enter to go back to the option selections ")
    os.system('cls' if os.name == 'nt' else 'clear')