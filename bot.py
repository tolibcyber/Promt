import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = ["@TolibTokyo", "@ai_promt_news"]
PROMPTS_CHANNEL = "@ai_promt_news"

# =============================================
# PROMPTLAR — yangi prompt qo'shish uchun
# shu ro'yxatga yangi {} blok qo'shing
# =============================================
PROMPTS = {
    "p001": {
        "title": "Cinematik portret",
        "category": "Portret",
        "prompt": "Use uploaded image as a reference person. Сохранить внешность и идентичность человека на 100% без изменений: лицо, форму головы, глаза, волосы, телосложение, оттенок кожи и естественные черты. Первое изображение image_1 использовать как главный template reference — полностью сохранить композицию, позу, ракурс камеры, расположение рук, освещение, интерьер кабинета и расположение объектов один к одному одинаково, заменив только лицо на лицо из reference image. Остальние фото которое должен созданный персона мои фото. Создать ультрареалистичный официальный портрет мужчины в государственном кабинете. Мужчина сидит за тёмным деревянным столом в кожаном кресле, руки спокойно сложены перед собой, строгий уверенный взгляд прямо в камеру. На нём тёмно-синий классический костюм, белая рубашка и тёмный галстук. Слева расположен флаг Узбекистана, на стене позади — официальный портрет президента в рамке, справа книжный шкаф. Изменить текст на настольной табличке на “Tolibjon Mardonov”, полностью сохранив оригинальный дизайн таблички, перспективу и реалистичную гравировку. Тёплое офисное освещение, clean presidential atmosphere, symmetrical centered composition, eye-level camera, 85mm lens, shallow depth of field, RAW DSLR quality, realistic skin texture, natural shadows, real-person photo, not AI-looking, no plastic skin, no HDR, no over-retouching, no distortion, no watermark."
    },
    "p002": {
        "title": "Cinematik portret",
        "category": "Portret",
        "prompt":"Use uploaded image as a reference person. Сохранить внешность и идентичность человека на 100% без изменений: лицо, причёску, глаза, форму головы, телосложение и естественные черты.Создать ультрареалистичный cinematic street portrait мужчины в тёмном luxury style. Мужчина стоит перед чёрным автомобилем на узкой городской улице между высокими зданиями, корпус прямо, взгляд уверенный и холодный в камеру. Одна рука в чёрной кожаной перчатке поднята к губам жестом “shhh”. На нём длинное чёрное пальто и полностью чёрный outfit. Фон — тёмный мегаполис с мокрой дорогой, дорогими машинами и глубоким urban bokeh. Холодное пасмурное освещение, moody атмосфера, low-key cinematic lighting, лёгкий туман, desaturated colors. Камера на уровне груди, medium full shot, 85mm lens, shallow depth of field, RAW DSLR quality, realistic skin texture, natural shadows, cinematic contrast, real-person photo, not AI-looking, no plastic skin, no HDR, no over-retouching, no distortion, no watermark."
    }, 
    
    # ---- yangi prompt shu yerdan pastga qo'shing ----
    # "p004": {
    #     "title": "Prompt nomi",
    #     "category": "Kategoriya",
    #     "prompt": "Bu yerga to'liq promptni yozing..."
    # },
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked", "restricted"]:
                return False
        except Exception:
            return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    # Obunani tekshirish
    is_subscribed = await check_subscription(user.id, context)

    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 TolibTokyo", url="https://t.me/TolibTokyo")],
            [InlineKeyboardButton("🎨 AI Promt New", url="https://t.me/ai_promt_new")],
            [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Xush kelibsiz!\n\n"
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=markup
        )
        return

    # Agar prompt ID bilan kelgan bo'lsa
    if args and args[0].startswith("p"):
        prompt_id = args[0]
        await send_prompt(update, context, prompt_id)
        return

    # Asosiy menyu
    await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎨 Promtlar kanaliga o'tish", url=f"https://t.me/{PROMPTS_CHANNEL.lstrip('@')}")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🤖 *AI Promt Bot*\n\n"
        "Bu botda siz tayyor AI promtlarni topasiz.\n\n"
        "👇 Promtlar kanalida har bir rasmning ostida "
        "*\"Promtni olish\"* tugmasi bor — bosing va promptni oling!"
    )

    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)


async def send_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt_id: str):
    prompt = PROMPTS.get(prompt_id)

    if not prompt:
        if update.message:
            await update.message.reply_text("❌ Promt topilmadi.")
        return

    text = (
        f"🎨 *{promt['title']}*\n"
        f"📁 Kategoriya: {promt['category']}\n\n"
        f"📋 *Promt:*\n`{promt['promt']}`\n\n"
        "👆 Yuqoridagi promtni bosib nusxalang!"
    )

    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_sub":
        is_subscribed = await check_subscription(query.from_user.id, context)
        if is_subscribed:
            await query.message.edit_text("✅ Rahmat! Obuna tasdiqlandi.")
            await show_main_menu(update, context)
        else:
            await query.answer("❌ Hali obuna bo'lmadingiz!", show_alert=True)


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot ishga tushdi ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
