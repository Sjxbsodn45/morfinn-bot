import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route


TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL = os.environ.get("CHANNEL_USERNAME", "@Morfinn051")

tg_app = Application.builder().token(TOKEN).build()


async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_membership(update.effective_user.id, context):
        await update.message.reply_text(
            "✅ خوش اومدی! بات برای شما فعاله."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url="https://t.me/Morfinn051"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ عضو شدم",
                callback_data="check"
            )
        ],
    ]

    await update.message.reply_text(
        "برای استفاده از بات، ابتدا در کانال عضو شو 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await check_membership(query.from_user.id, context):
        await query.edit_message_text(
            "✅ عضویت تأیید شد! بات برای شما فعال شد."
        )
    else:
        await query.answer(
            "❌ هنوز عضو کانال نیستی.",
            show_alert=True
        )


tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(
    CallbackQueryHandler(check, pattern="^check$")
)


async def webhook(request: Request):
    try:
        data = await request.json()

        if not tg_app.running:
            await tg_app.initialize()

        update = Update.de_json(data, tg_app.bot)
        await tg_app.process_update(update)

        return PlainTextResponse("OK", status_code=200)

    except Exception as e:
        print("Webhook error:", repr(e))
        return PlainTextResponse("Webhook error", status_code=500)


async def health(request: Request):
    return PlainTextResponse("Bot is running", status_code=200)


app = Starlette(
    routes=[
        Route("/", webhook, methods=["POST"]),
        Route("/", health, methods=["GET"]),
    ]
)
