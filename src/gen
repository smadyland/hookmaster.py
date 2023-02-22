import requests
import json
import random
import string
import time

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
input("Press any key to exit")
