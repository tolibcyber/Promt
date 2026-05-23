import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
 
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7288739341
 
CHANNELS = ["@TolibTokyo", "@ai_promt_news"]
PROMTS_CHANNEL = "@ai_promt_news"
SUPPORT_USERNAME = "@TolibDev"
 
PROMTS = {
    "p001": {
        "title": "Cinematik portret",
        "category": "Portret",
        "promt": "Use uploaded image as a reference person. Сохранить внешность и идентичность человека на 100% без изменений: лицо, форму головы, глаза, волосы, телосложение, оттенок кожи и естественные черты. Первое изображение image_1 использовать как главный template reference — полностью сохранить композицию, позу, ракурс камеры, расположение рук, освещение, интерьер кабинета и расположение объектов один к одному одинаково, заменив только лицо на лицо из reference image. Остальние фото которое должен созданный персона мои фото. Создать ультрареалистичный официальный портрет мужчины в государственном кабинете. Мужчина сидит за тёмным деревянным столом в кожаном кресле, руки спокойно сложены перед собой, строгий уверенный взгляд прямо в камеру. На нём тёмно-синий классический костюм, белая рубашка и тёмный галстук. Слева расположен флаг Узбекистана, на стене позади — официальный портрет президента в рамке, справа книжный шкаф. Изменить текст на настольной табличке на 'Tolibjon Mardonov', полностью сохранив оригинальный дизайн таблички, перспективу и реалистичную гравировку. Тёплое офисное освещение, clean presidential atmosphere, symmetrical centered composition, eye-level camera, 85mm lens, shallow depth of field, RAW DSLR quality, realistic skin texture, natural shadows, real-person photo, not AI-looking, no plastic skin, no HDR, no over-retouching, no distortion, no watermark."
    },
    "p002": {
        "title": "Cinematik portret",
        "category": "Portret",
        "promt": "Use uploaded image as a reference person. Сохранить внешность и идентичность человека на 100% без изменений: лицо, причёску, глаза, форму головы, телосложение и естественные черты.Создать ультрареалистичный cinematic street portrait мужчины в тёмном luxury style. Мужчина стоит перед чёрным автомобилем на узкой городской улице между высокими зданиями, корпус прямо, взгляд уверенный и холодный в камеру. Одна рука в чёрной кожаной перчатке поднята к губам жестом 'shhh'. На нём длинное чёрное пальто и полностью чёрный outfit. Фон — тёмный мегаполис с мокрой дорогой, дорогими машинами и глубоким urban bokeh. Холодное пасмурное освещение, moody атмосфера, low-key cinematic lighting, лёгкий туман, desaturated colors. Камера на уровне груди, medium full shot, 85mm lens, shallow depth of field, RAW DSLR quality, realistic skin texture, natural shadows, cinematic contrast, real-person photo, not AI-looking, no plastic skin, no HDR, no over-retouching, no distortion, no watermark."
    },
    "p003": {
        "title": "Fitnes portret",
        "category": "Portret",
        "promt": "Use uploaded image as a reference person. Сохранить внешность и идентичность человека на 100% без изменений: лицо, волосы, телосложение, мышцы, кожу, пропорции тела и естественные черты. Создать ультрареалистичное gym mirror selfie мужчины в современном тренажёрном зале. Мужчина стоит перед зеркалом с телефоном в руке, спокойный уверенный взгляд слегка вниз, natural relaxed pose. На нём облегающая белая athletic футболка, чёрные jogger pants, wrist wraps и проводные наушники. Фон — realistic gym equipment, зеркала и металлические тренажёры с мягким background blur. Естественное indoor gym lighting, realistic skin texture, visible muscle definition without exaggeration, RAW iPhone photo aesthetic, slight grain, candid fitness atmosphere, natural shadows, real-person photo, not AI-looking, no plastic skin, no fake muscles, no HDR, no over-retouching, no distortion, no watermark."
    },
    "p004": {
        "title": "Cinematik portret",
        "category": "Portret",
        "promt": "Use uploaded image as a reference person. Please transform the provided photograph into an ultra-realistic, cinematic artistic portrait without altering facial expression or expression. The man should appear seated on the ground in a relaxed and natural pose, elegant yet modern.He is dressed in a minimalist black top, paired with soft, gray jeans and chunky gray and white sneakers, giving him a contemporary urban aesthetic.The background should be an artistic monochrome (black and white) composition featuring a soft, blurred side profile of the same man; like a ghostly echo, it blends memory and presence.The overall atmosphere should convey a poetic, editorial, and timeless feel reminiscent of fine art fashion photography. Use soft, diffused studio lighting, subtle shadows, and shallow depth of field to emphasize emotion"
    },
    "p005": {
        "title": "Cinematik portret",
        "category": "Portret",
        "promt": "Use uploaded image as a reference person. Сохранить внешность и идентичность девушки на 100% без изменений: лицо, глаза, губы, форму носа, волосы, оттенок кожи, телосложение и естественные черты.Создать ультрареалистичный lifestyle portrait девушки сидящей на полу в расслабленной естественной позе. Одна нога согнута ближе к камере, рука мягко касается головы, лёгкая спокойная улыбка и тёплый взгляд в объектив. На девушке чёрный облегающий лонгслив, серые relaxed-fit джинсы и светлые кроссовки. Волосы заплетены в длинную небрежную косу с мягкими выбившимися прядями. На фоне — большой monochrome portrait этой же девушки с мягким blur эффектом, создающий cinematic layered composition. Мягкий natural window light, neutral grey background, shallow depth of field, 85mm lens, realistic skin texture, natural shadows, RAW DSLR quality, cozy editorial aesthetic, real-person photo, not AI-looking, no plastic skin, no HDR, no over-retouching, no distortion, no watermark."
    },
}
 
# Foydalanuvchilarni saqlash uchun (xotira)
user_ids = set()
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
 
# =============================================
# PASTKI MENYU (Reply Keyboard)
# =============================================
def get_main_keyboard():
    keyboard = [
        [
            KeyboardButton("🎨 Promt kanali"),
            KeyboardButton("🎬 AI Video yasash"),
        ],
        [
            KeyboardButton("🆘 Qo'llab-quvvatlash"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
 
 
# =============================================
# OBUNA TEKSHIRISH
# =============================================
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked", "restricted"]:
                return False
        except Exception:
            return False
    return True
 
 
# =============================================
# /start
# =============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    user_ids.add(user.id)
 
    is_subscribed = await check_subscription(user.id, context)
 
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 TolibTokyo", url="https://t.me/TolibTokyo")],
            [InlineKeyboardButton("🎨 AI Promt News", url="https://t.me/ai_promt_news")],
            [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Xush kelibsiz!\n\n"
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=markup
        )
        return
 
    if args and args[0].startswith("p"):
        promt_id = args[0]
        await send_promt(update, context, promt_id)
        return
 
    await show_main_menu(update, context)
 
 
# =============================================
# ASOSIY MENYU
# =============================================
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 *AI Promt Bot*\n\n"
        "Bu botda siz tayyor AI promtlarni topasiz.\n\n"
        "👇 Quyidagi tugmalardan foydalaning:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, parse_mode="Markdown", reply_markup=get_main_keyboard())
 
 
# =============================================
# PROMT YUBORISH
# =============================================
async def send_promt(update: Update, context: ContextTypes.DEFAULT_TYPE, promt_id: str):
    promt = PROMTS.get(promt_id)
 
    if not promt:
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
 
 
# =============================================
# PASTKI TUGMALAR HANDLER
# =============================================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    user_ids.add(user.id)
 
    # Admin broadcast xabar kutilayotgan bo'lsa
    if user.id == ADMIN_ID and context.user_data.get("waiting_broadcast"):
        context.user_data["waiting_broadcast"] = False
        await update.message.reply_text(f"⏳ Yuborilmoqda... ({len(user_ids)} ta foydalanuvchi)")
        success = 0
        failed = 0
        for uid in list(user_ids):
            try:
                await context.bot.send_message(chat_id=uid, text=text)
                success += 1
            except Exception:
                failed += 1
        await update.message.reply_text(
            f"✅ *Yuborish yakunlandi!*\n\n"
            f"✔️ Muvaffaqiyatli: *{success}* ta\n"
            f"❌ Xatolik: *{failed}* ta",
            parse_mode="Markdown"
        )
        return
 
    # Tugmalar
    if text == "🎨 Promt kanali":
        keyboard = [[InlineKeyboardButton("📢 Kanalga o'tish", url=f"https://t.me/{PROMTS_CHANNEL.lstrip('@')}")]]
        await update.message.reply_text(
            "🎨 *Promt kanali*\n\n"
            "Kanalimizda har kuni yangi AI promtlar chiqadi!\n"
            "Har bir post ostida *\"Promt olish\"* tugmasi bor — bosing va nusxalang.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
 
    elif text == "🎬 AI Video yasash":
        keyboard = [[InlineKeyboardButton("📢 Kanalga o'tish", url=f"https://t.me/{PROMTS_CHANNEL.lstrip('@')}")]]
        await update.message.reply_text(
            "🎬 *AI Video yasash*\n\n"
            "Tez kunda kanalimizda AI orqali video yasashning "
            "*to'liq qo'llanmasi* chiqadi!\n\n"
            "📌 Quyidagi mavzular yoritiladi:\n"
            "• Kling AI bilan video yasash\n"
            "• Rasmdan video qilish\n"
            "• Promt yozish sirlari\n"
            "• Bepul toollar ro'yxati\n\n"
            "🔔 Kanalga obuna bo'ling — o'tkazib yubormang!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
 
    elif text == "🆘 Qo'llab-quvvatlash":
        keyboard = [[InlineKeyboardButton("✉️ Admin bilan bog'lanish", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}")]]
        await update.message.reply_text(
            "🆘 *Qo'llab-quvvatlash*\n\n"
            "Savollar yoki takliflar bo'lsa,\n"
            "admin bilan to'g'ridan-to'g'ri bog'laning:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
 
 
# =============================================
# INLINE TUGMALAR
# =============================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
 
    if query.data == "check_sub":
        is_subscribed = await check_subscription(query.from_user.id, context)
        if is_subscribed:
            user_ids.add(query.from_user.id)
            await query.message.edit_text("✅ Rahmat! Obuna tasdiqlandi.")
            await show_main_menu(update, context)
        else:
            await query.answer("❌ Hali obuna bo'lmadingiz!", show_alert=True)
 
    elif query.data == "user_count":
        if query.from_user.id != ADMIN_ID:
            return
        await query.message.reply_text(f"👥 Jami foydalanuvchilar: *{len(user_ids)}* ta", parse_mode="Markdown")
 
    elif query.data == "broadcast":
        if query.from_user.id != ADMIN_ID:
            return
        context.user_data["waiting_broadcast"] = True
        await query.message.reply_text(
            "✍️ Hammaga yubormoqchi bo'lgan xabaringizni yozing:\n\n"
            "_(Bekor qilish uchun /cancel yozing)_",
            parse_mode="Markdown"
        )
 
 
# =============================================
# ADMIN PANEL
# =============================================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizda ruxsat yo'q!")
        return
 
    keyboard = [
        [InlineKeyboardButton("📨 Hammaga xabar yuborish", callback_data="broadcast")],
        [InlineKeyboardButton("👥 Foydalanuvchilar soni", callback_data="user_count")],
    ]
    await update.message.reply_text(
        f"⚙️ *Admin Panel*\n\n"
        f"👥 Hozirgi foydalanuvchilar: *{len(user_ids)}* ta",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
 
 
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_broadcast"] = False
    await update.message.reply_text("❌ Bekor qilindi.")
 
 
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot ishga tushdi ✅")
    app.run_polling()
 
 
if __name__ == "__main__":
    main()
