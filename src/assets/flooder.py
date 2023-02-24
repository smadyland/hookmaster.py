import dhooks
import time

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
