from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# സപ്പോർട്ട് ഗ്രൂപ്പ് ഐഡി
SUPPORT_GROUP_ID = -1002238061487

# വെൽക്കം ഫോട്ടോയുടെ ലിങ്ക്
WELCOME_PHOTO = "https://files.catbox.moe/50v0ss.jpg"

# ചാനലുകളും എപ്പിസോഡുകളുമായി ബന്ധപ്പെട്ട കീവേഡുകൾ
CHANNEL_KEYWORDS = [
    "today episode", "today's episode", "yesterday episode", 
    "asianet", "zee keralam", "mazhavil manorama", "surya tv"
]

# എല്ലാ സീരിയലുകളുടെയും ലിസ്റ്റ്
SERIALS_LIST = [
    "kanmashi", "karnan", "valyettan", "pranayavilasam", "durga", "chembarathy", 
    "saregamapa", "saregamapa lil champs", "kudumbasametham", "meghasandhesham", 
    "seethayanam", "krishnagadha", "meghasandesam", "aval arundhati", "akale", 
    "snehapoorvam shyama", "mangalyam", "manathe kottaram", "ashwathi nakshatram", 
    "kudumbashree sharada", "bigg boss", "taste time", "sindhu bhairavi", 
    "comedy cooks", "ivar vivahitharayal", "oru kochu swapnam", "advocate anjali", 
    "kattathe kilikoodu", "ee puzhayum kadannu", "sindoorapottu", "star singer", 
    "teacheramma", "mazha thorum munpe", "pavithram", "ishtam mathram", 
    "santhwanam", "snehakkoottu", "mounaragam", "patharamattu", "amma manassu", 
    "chempaneer poovu", "dharmma yoddhavu garudan", "othiri othiri swapnangal", 
    "ottashikharam", "archana chechi llb", "super kanmani", "marimayam", 
    "oru chiri iru chiri bumper chiri", "the great family challenge", "roopavathi", 
    "thenmavin kombath", "punnaram", "anju sundarikal", "amme mookambike", 
    "peythozhiyathe", "chattambipparu", "hridayam", "kanyadaanam", 
    "swayamavarapanthal", "mangalyam thanthunanena"
]

# 1. പുതിയ മെമ്പേഴ്സ് ജോയിൻ ചെയ്യുമ്പോൾ ഫോട്ടോ സഹിതം വെൽക്കം മെസ്സേജ് അയക്കാൻ
@Client.on_message(filters.new_chat_members & ~filters.private, group=-1)
async def welcome_new_member(client, message):
    if message.chat.id != SUPPORT_GROUP_ID:
        return
        
    for member in message.new_chat_members:
        user_name = member.first_name if member.first_name else "User"
        
        caption_text = (
            f"<b>Hello there, {user_name} 👋 and welcome to the Support Group by Allu Group! How are you doing today? 🥰\n\n"
            f"🎬 Welcome to Our Group!\n\n"
            f"✨ Feel free to share anything here openly and share your thoughts or requests with everyone!\n\n"
            f"✅ This group is completely dedicated solely to serial support and assistance.\n\n"
            f"💬 You can ask your queries and discuss your issues freely anytime.\n\n"
            f"🛡️ Full admin support will always be available for you!</b>"
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 CONTACT ADMIN URGENT 📩", url="https://t.me/Anujith1238")]
        ])
        
        # ഫോട്ടോയും ക്യാപ്ഷനും ബട്ടണും അയക്കുന്നു
        await client.send_photo(
            chat_id=message.chat.id,
            photo=WELCOME_PHOTO,
            caption=caption_text,
            reply_markup=buttons
        )
    
    # ഗ്രൂപ്പിലെ ജോയിൻ ചെയ്ത നോട്ടിഫിക്കേഷൻ മെസ്സേജ് (System message) ഒഴിവാക്കാൻ വേണമെങ്കിൽ ഇത് കൊടുക്കാം
    try:
        await message.delete()
    except:
        pass

    return message.stop_propagation()


# 2. ഗ്രൂപ്പിലെ സാധാരണ ടെക്സ്റ്റ് മെസ്സേജുകൾ ഹാൻഡിൽ ചെയ്യാൻ
@Client.on_message(filters.text & ~filters.private, group=-1)
async def serial_restriction_handler(client, message):
    if message.chat.id != SUPPORT_GROUP_ID:
        return
        
    text = message.text.lower().strip()
    user_name = message.from_user.first_name if message.from_user else "User"
    
    # Hi / Hello greetings handler
    hi_keywords = ["hi", "hello", "hlo", "hai"]
    if any(word == text for word in hi_keywords):
        reply_text = (
            f"<b>Hello 👋 {user_name}\n\n"
            f"Welcome To Allu TV Serial ❤️\n"
            f"How are you doing today? 🥰\n\n"
            f"Team 🥰👇\n"
            f"@Anujith1238 , @Arunya18</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # GM / Good Morning / Good Night / Good Evening handler
    if "good morning" in text or text == "gm":
        await message.reply_text(f"<b>Good Morning, {user_name} 🌅 Have a wonderful day ahead! 🥰</b>")
        return message.stop_propagation()
    elif "good night" in text:
        await message.reply_text(f"<b>Good Night, {user_name} 🌙 Sweet dreams! ✨</b>")
        return message.stop_propagation()
    elif "good evening" in text:
        await message.reply_text(f"<b>Good Evening, {user_name} 🌆 Hope you had a great day! 👍</b>")
        return message.stop_propagation()

    # Urgent / Help handler
    urgent_keywords = ["urgent", "help", "emergency", "support"]
    if any(keyword in text for keyword in urgent_keywords):
        reply_text = (
            f"<b>Hello {user_name},\n\n"
            f"You can contact me if you have any urgent matters. 🥰\n\n"
            f"@Anujith1238\n\n"
            f"There will be all support from our side.\n\n"
            f"Best regards,\n"
            f"ALLU Team ✅</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # Today/Yesterday episodes or channels handler
    if any(keyword in text for keyword in CHANNEL_KEYWORDS):
        reply_text = (
            "<b>Ok bro ❤️\n\n"
            "It will be uploaded when the admin sees it ❤️\n\n"
            "Waiting until then... 🥰</b>"
        )
        await message.reply_text(reply_text)
        return message.stop_propagation()

    # Serials list handler
    if any(serial in text for serial in SERIALS_LIST):
        reply_text = (
            f"<b>Hello {user_name},\n\n"
            f"This is just a support group! ⚠️\n"
            f"If you want serials, please ask in the group below: 👇</b>"
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("👉 Click Here To Join Group 👈", url="https://t.me/AlluTvSerialGroup")]
        ])
        
        await message.reply_text(reply_text, reply_markup=buttons)
        return message.stop_propagation()
