import os
import random
import logging
from telebot import TeleBot, types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch Telegram Bot Token from Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided. Please set it in Railway environment variables.")

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

# Demo Data / Custom Links (Replace with your actual links)
OFFICIAL_CHANNEL = os.getenv("CHANNEL_LINK", "https://t.me/your_channel")
MAIN_CASINO_LINK = os.getenv("CASINO_LINK", "https://example.com/play")
SUPPORT_USERNAME = os.getenv("SUPPORT_USER", "your_support_username")

# Main Menu Keyboard
def get_main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_play = types.InlineKeyboardButton("🎰 Play Now / Register", url=MAIN_CASINO_LINK)
    btn_bonus = types.InlineKeyboardButton("🎁 Daily Bonus", callback_data="claim_bonus")
    btn_boost = types.InlineKeyboardButton("🚀 Boost Channel / VIP", callback_data="boost_info")
    btn_referral = types.InlineKeyboardButton("👥 Referral Boost", callback_data="referral_info")
    btn_channel = types.InlineKeyboardButton("📢 Join Channel", url=OFFICIAL_CHANNEL)
    btn_support = types.InlineKeyboardButton("💬 Support 24/7", url=f"https://t.me/{SUPPORT_USERNAME}")

    markup.add(btn_play)
    markup.add(btn_bonus, btn_boost)
    markup.add(btn_referral, btn_channel)
    markup.add(btn_support)
    return markup

# Back to main menu button
def get_back_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")
    markup.add(btn_back)
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🔥 <b>Welcome to the Ultimate Casino Booster, {user_name}!</b> 🔥\n\n"
        f"🎰 Enjoy exclusive casino bonuses, free spins, VIP tier upgrades, and fast payouts.\n\n"
        f"<b>Features:</b>\n"
        f"• 💰 <b>Daily Free Bonus:</b> Up to $100 everyday!\n"
        f"• 🚀 <b>Telegram VIP Boost:</b> Unlock special cashback rates.\n"
        f"• 🤝 <b>Referral Program:</b> Earn rewards for inviting friends.\n\n"
        f"Select an option below to get started:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "main_menu":
        welcome_text = (
            f"🔥 <b>Main Casino Hub</b> 🔥\n\n"
            f"Choose an option below to explore bonuses, VIP boosts, or start playing:"
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=welcome_text,
            reply_markup=get_main_keyboard()
        )

    elif call.data == "claim_bonus":
        reward = random.choice([5, 10, 25, 50, 100])
        bonus_text = (
            f"🎉 <b>CONGRATULATIONS!</b> 🎉\n\n"
            f"You received a mystery deposit bonus of <b>${reward} FREE CREDIT</b>!\n\n"
            f"👉 Register your account now to claim your reward code: <code>BOOST-{random.randint(1000, 9999)}</code>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎁 Claim Reward Now", url=MAIN_CASINO_LINK))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=bonus_text,
            reply_markup=markup
        )

    elif call.data == "boost_info":
        boost_text = (
            f"🚀 <b>Telegram Channel VIP Boost</b> 🚀\n\n"
            f"Boost our official channel to unlock premium benefits:\n"
            f"✅ 20% Weekly Cashback\n"
            f"✅ Instant Withdrawal Priority\n"
            f"✅ Free Tournament Entries\n\n"
            f"Click below to boost our channel on Telegram!"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⚡ Boost Telegram Channel", url=OFFICIAL_CHANNEL))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=boost_text,
            reply_markup=markup
        )

    elif call.data == "referral_info":
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start=ref_{call.from_user.id}"
        
        ref_text = (
            f"👥 <b>Referral Boost Program</b>\n\n"
            f"Invite active users to earn commission & extra bonuses!\n\n"
            f"🔗 <b>Your Invite Link:</b>\n<code>{ref_link}</code>\n\n"
            f"<b>Rewards:</b>\n"
            f"• $5 Free Bonus per 5 Active Friends\n"
            f"• 10% Extra Deposit Commission"
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=ref_text,
            reply_markup=get_back_keyboard()
        )

if __name__ == "__main__":
    logger.info("Bot starting...")
    bot.infinity_polling(skip_pending=True)
