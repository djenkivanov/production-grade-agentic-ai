import ngrok
import time
import os

# production or dev check
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

token = os.getenv("NGROK_AUTHTOKEN")

listener = ngrok.forward("localhost:9000", authtoken=token)

print(f"Ngrok URL: {listener.url()}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down ngrok...")
    ngrok.disconnect(listener.url())