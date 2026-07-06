import asyncio
import os
import logging
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Get Credentials from Environment Variables ---
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
STRING_SESSION = os.environ.get('STRING_SESSION', '')

# --- Settings ---
NOTIFICATION_BOT_ID = 468253535
MAFIA_CHAT = -1001230631243
INTERVAL_SECONDS = 90

async def click_gabung_buttons(event):
    try:
        msg = event.message
        if not msg or not msg.buttons:
            return
        for row in msg.buttons:
            for button in row:
                text = getattr(button, 'text', '').lower()
                if any(word in text for word in ["join", "gabung", "sertai"]):
                    await button.click()
                    logger.info("Clicked button '%s'", text)
    except Exception as e:
        logger.error("Button click error: %s", e)

async def main():
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    logger.info("Client started successfully!")

    @client.on(events.NewMessage)
    async def handler(event):
        if getattr(event, 'sender_id', None) == NOTIFICATION_BOT_ID:
            await click_gabung_buttons(event)

    async def send_next_periodically():
        while True:
            try:
                await client.send_message(MAFIA_CHAT, "/next")
                logger.info("Sent /next")
            except Exception as e:
                logger.error("Error sending /next: %s", e)
            await asyncio.sleep(INTERVAL_SECONDS)

    await asyncio.gather(
        client.run_until_disconnected(),
        send_next_periodically()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted — shutting down...")
