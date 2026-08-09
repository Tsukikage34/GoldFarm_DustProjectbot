import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

BOT_TOKEN = "8614044710:AAHqn3BDEjSeJXe6K86MqJL4C9Q3NCxNQh4"
CHANNELS = ["@faisetDustProject", "@TsukikageDastProject"]
MIN_REFERRALS = 5

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
referrals = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    ref = message.text.split()
    if len(ref) > 1 and ref[1] != user_id:
        if user_id not in referrals:
            referrals[user_id] = []
        if ref[1] not in referrals.get(user_id, []):
            referrals.setdefault(ref[1], []).append(user_id)
            await bot.send_message(ref[1], "✅ Новый реферал! +500 голды")
    subscribed = True
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                subscribed = False
        except:
            subscribed = False
    count = len(referrals.get(user_id, []))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📢 Канал 1", url="https://t.me/faisetDustProject")],
        [InlineKeyboardButton("📢 Канал 2", url="https://t.me/TsukikageDastProject")],
        [InlineKeyboardButton("📤 Моя ссылка", switch_inline_query=f"start={user_id}")],
    ])
    text = f"💰 Баланс: {count * 500} голды\n👥 Рефералов: {count} / {MIN_REFERRALS}\n📌 Для вывода нужно {MIN_REFERRALS} рефералов\n\n"
    text += "❌ Подпишитесь на каналы!" if not subscribed else "✅ Вы подписаны!"
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)

@dp.message(Command("ref"))
async def ref_link(message: types.Message):
    user_id = str(message.from_user.id)
    link = f"https://t.me/{bot.username}?start={user_id}"
    await message.answer(f"Ваша ссылка:\n{link}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
