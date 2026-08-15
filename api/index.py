import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@Morfinn051"    ]

    await update.message.reply_text(
        "برای استفاده از بات، ابتدا در کانال عضو شو 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
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


application.add_handler(CommandHandler("start", start))
application.add_handler(
    CallbackQueryHandler(check, pattern="^check$")
)


async def handler(request):
    data = await request.json()

    update = Update.de_json(
        data=data,
        bot=application.bot
    )

    if not application.running:
        await application.initialize()

    await application.process_update(update)

    return {
        "statusCode": 200,
        "body": "OK"
    }
