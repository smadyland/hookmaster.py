import subprocess
import threading
import requests
import dhooks
import ctypes
import random
import string
import time
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

ctypes.windll.kernel32.SetConsoleTitleW("hookmaster.py")

def webhook_gen():
    def generate_random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    channel_id = input('enter the channel ID: ')
    num_webhooks = int(input('enter the number of webhooks to create (max 15 per channel): '))
    webhook_name = input('enter the name for the webhooks (press enter for random): ')
    proxy_url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&simplified=true'
    proxies = {'socks4': proxy_url}
    url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
    headers = {"Content-Type": "application/json", "Authorization": f"Bot " + TOKEN}

    for i in range(num_webhooks):
        if webhook_name:
            name = webhook_name
        else:
            name = generate_random_string(8)
        payload = {"name": name}
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        if response.status_code != 200:
            print(f"failed to create webhook: {response.text}")
        else:
            response_json = response.json()
            webhook_id = response_json["id"]
            webhook_token = response_json["token"]

            webhook_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
            print(f"successfully created webhook: {webhook_url}")

            with open("webhooks.txt", "a") as f:
                f.write(webhook_url + "\n")
    print("wrote webhook URL's to webhooks.txt successfully!")

def checker():
    with open("webhooks.txt", "r") as f:
        webhooks = f.read().splitlines()

    working_webhooks = []
    for webhook in webhooks:
        try:
            response = requests.get(webhook)
            if response.status_code >= 200 and response.status_code < 300:
                working_webhooks.append(webhook)
        except:
            pass

    num_checked = len(webhooks)
    num_deleted = len(webhooks) - len(working_webhooks)

    with open("webhooks.txt", "w") as f:
        f.write("\n".join(working_webhooks))
    print(f"successfully checked through {num_checked} webhook(s), and deleted {num_deleted} broken one(s)!")

def delete_webhooks():
    channel_id = input("enter the ID of the channel to delete webhooks from: ")
    url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
    headers = {"Authorization": f"Bot {TOKEN}"}
    response = requests.get(url, headers=headers)
    proxy_url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&simplified=true'
    proxies = {'socks4': proxy_url}

    if response.status_code != 200:
        print(f"failed to get webhooks: {response.text}")
        return
    webhooks = response.json()

    for webhook in webhooks:
        webhook_id = webhook["id"]
        webhook_url = f"https://discord.com/api/webhooks/{webhook_id}"
        response = requests.delete(webhook_url, headers=headers, proxies=proxies)
        if response.status_code != 204:
            print(f"failed to delete webhook {webhook_id}: {response.text}")
        else:
            print(f"deleted webhook {webhook_id}")

def pinger_flooder():
    with open('webhooks.txt', 'r') as f:
        webhook_links = [line.strip() for line in f.readlines()]

    message = "@everyone hookmaster winning"
    messages_per_second = float(input("how many messages per second? (default = 1, 0 for instant): ") or 1)

    def send_message(link):
        hook = dhooks.Webhook(link)
        hook.send(message)

    if messages_per_second == 0:
        while True:
            threads = []
            for link in webhook_links:
                t = threading.Thread(target=send_message, args=(link,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
    else:
        delay = 1.0 / messages_per_second
        while True:
            threads = []
            for link in webhook_links:
                t = threading.Thread(target=send_message, args=(link,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            time.sleep(delay)
            print("sending messages!")

def message_send():
    webhook_links = []
    with open('webhooks.txt', 'r') as f:
        webhook_links.extend([line.strip() for line in f.readlines()])

    message = input("what would you like the webhooks to say?: ")
    messages_per_second = float(input("how many messages per second? (default = 1, 0 for instant): ") or 1)

    def send_message(link):
        hook = dhooks.Webhook(link)
        hook.send(message)

    if messages_per_second == 0:
        while True:
            threads = []
            for link in webhook_links:
                t = threading.Thread(target=send_message, args=(link,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
    else:
        delay = 1.0 / messages_per_second
        while True:
            threads = []
            for link in webhook_links:
                t = threading.Thread(target=send_message, args=(link,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            time.sleep(delay)
            print("sending messages!")

def run_script(num):
    if num == 1:
        webhook_gen()
    elif num == 2:
        checker()
    elif num == 3:
        delete_webhooks()
    elif num == 4:
        subprocess.Popen(['start', 'cmd', '/c', 'python', 'guildfucker.py'], shell=True)
    elif num == 5:
        message_send()
    elif num == 6:
        pinger_flooder()
    elif num == 0:
        print("exiting the program")
        time.sleep(0.3)
        exit()
    else:
        print("invalid option")

while True:
    print("""
|              |                   |                         
|---.,---.,---.|__/ ,-.-.,---.,---.|--- ,---.,---. ,---.,   .
|   ||   ||   ||  \ | | |,---|`---.|    |---'|     |   ||   |
`   '`---'`---'`   `` ' '`---^`---'`---'`---'`    o|---'`---|
                                                   |    `---'
                                                   """)
    print("enter 1 to execute the webhook generator")
    print("enter 2 to execute the webhook checker")
    print("enter 3 to execute the webhook deleter")
    print("enter 4 to run the guild fucker 3000")
    print("enter 5 to execute the custom message flooder")
    print("enter 6 to execute the pinger flooder")
    print("enter 0 to exit the program")

    user_input = int(input("enter your selection...: "))
    run_script(user_input)

    input("press enter to go back to the option selections. ")
    os.system('cls' if os.name == 'nt' else 'clear')
