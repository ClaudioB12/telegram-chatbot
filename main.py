import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from dotenv import load_dotenv

# ======================================
# CONFIGURACIÓN
# ======================================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Tus datos personales
MI_NOMBRE = "Claudio Bustinza Inofuente"
MI_DESCRIPCION = (
    "Soy Claudio Bustinza, estudiante de Ingeniería de Sistemas en la UPeU, "
    "desarrollador backend/frontend y apasionado por la tecnología, IA y proyectos "
    "de software aplicados al turismo y negocios del Perú."
)

# Descripción general del bot
BOT_DESCRIPCION = (
    "¡Hola! Soy un bot personal creado por Claudio. Estoy diseñado para ayudarte, "
    "responder preguntas, interactuar contigo y servir como asistente digital."
)

app = FastAPI()

telegram_app = Application.builder().token(TOKEN).build()


# ======================================
# HANDLER /start
# ======================================
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Descripción del Bot 🤖", callback_data="descripcion_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "¡Hola! Soy tu bot personalizado 🤖🔥\n"
        "Presiona el botón para saber más:",
        reply_markup=reply_markup
    )


# ======================================
# HANDLER para el botón “Descripción del bot”
# ======================================
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "descripcion_bot":
        await query.edit_message_text(BOT_DESCRIPCION)


# ======================================
# HANDLER para detectar “¿quién soy?”, “mi nombre”, etc.
# ======================================
async def identificar_usuario(update: Update, context):
    texto = update.message.text.lower()

    if any(frase in texto for frase in ["quien soy", "quién soy", "como me llamo", "mi nombre", "quién soy yo", "quien soy yo"]):
        respuesta = (
            f"Tu nombre es:\n\n"
            f"👤 *{MI_NOMBRE}*\n\n"
            f"📄 *Descripción personal:*\n{MI_DESCRIPCION}"
        )
        await update.message.reply_markdown(respuesta)
        return

    # Respuesta común
    await update.message.reply_text(f"Recibí tu mensaje: {update.message.text}")


# ======================================
# STARTUP PARA INICIALIZAR EL BOT
# ======================================
@app.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    await telegram_app.start()
    print("Bot iniciado correctamente ✔")


@app.on_event("shutdown")
async def shutdown_event():
    await telegram_app.stop()
    print("Bot detenido ❌")


# ======================================
# ENDPOINT DEL WEBHOOK
# ======================================
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}


# ======================================
# RUTA DE PRUEBA
# ======================================
@app.get("/")
def home():
    return {"status": "Bot funcionando", "author": MI_NOMBRE}


# ======================================
# REGISTRO DE HANDLERS
# ======================================
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button_handler))
telegram_app.add_handler(MessageHandler(filters.TEXT, identificar_usuario))
