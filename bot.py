import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import uvicorn

# ============ SETTINGS ============
BOT_TOKEN = os.getenv("8466271055:AAFJHcvJ3WR2oAI7g1Xky2760qLgM68WXMM")  # Telegram bot token from env
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("VERCEL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{BASE_URL}{WEBHOOK_PATH}"

# ============ INIT BOT ============
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ HANDLERS ============
# Example: replace with your real handlers
@dp.message()
async def handle_activity(message: types.Message):
    await message.answer(f"✅ You said: {message.text}")

# You can add your other handlers here
# e.g. commands, photo uploads, etc.

# ============ FASTAPI APP ============
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("⚡ Setting webhook...")
    await bot.set_webhook(WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# Local run (dev only)
if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

