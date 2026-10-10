import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from info import (
    VERIFY,
    VERIFY_ACCESS_HOURS,
    SHORTLINK_URL,
    SHORTLINK_API,
    TUTORIAL,
    HOW_TO_VERIFY,
    VERIFY_POSTER,
    VERIFIED_POSTER
)
from utils import get_shortlink

# 24 മണിക്കൂർ വെരിഫിക്കേഷൻ സ്റ്റാറ്റസ് ചെക്ക് ചെയ്യുന്ന ഫംഗ്ഷൻ
async def check_24hrs_verification(user_id):
    if not VERIFY:
        return True
        
    user = await db.get_user(user_id)
    if not user or "verified_time" not in user:
        return False
        
    verified_time = user["verified_time"]
    if verified_time.tzinfo is None:
        verified_time = pytz.utc.localize(verified_time)
        
    now = datetime.datetime.now(pytz.utc)
    time_diff = (now - verified_time).total_seconds()
    
    # 24 മണിക്കൂർ (24 * 3600 സെക്കൻഡ്) കഴിഞ്ഞിട്ടുണ്ടോ എന്ന് പരിശോധിക്കുന്നു
    if time_diff < (VERIFY_ACCESS_HOURS * 3600):
        return True
    return False

# വെരിഫിക്കേഷൻ ആവശ്യപ്പെട്ടുകൊണ്ടുള്ള മെസ്സേജും ബട്ടണും അയക്കാൻ
async def send_24hrs_verification_box(client, message, file_id=None):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    param = f"verify24_{user_id}_{file_id}" if file_id else f"verify24_{user_id}"
    original_link = f"https://telegram.me/{client.me.username}?start={param}"
    
    # നിങ്ങളുടെ ഷോർട്ട്നർ URL ഉം API യും ഉപയോഗിച്ച് ലിങ്ക് ജനേറ്റ് ചെയ്യുന്നു
    short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, original_link)
    
    caption = (
        f"<b>HEY {first_name.upper()},</b>\n\n"
        f"<b>‼️ YOU'RE NOT VERIFIED TODAY ‼️</b>\n\n"
        f"<b>›› PLEASE VERIFY AND GET UNLIMITED ACCESS FOR {VERIFY_ACCESS_HOURS} HOURS ✅</b>\n\n"
        f"<b>›› IF YOU WANT DIRECT FILES THEN YOU CAN TAKE PREMIUM SERVICES.</b>"
    )
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("CLICK HERE TO VERIFY", url=short_link)
        ],
        [
            InlineKeyboardButton("HOW TO VERIFY", url=HOW_TO_VERIFY or TUTORIAL)
        ]
    ])
    
    if VERIFY_POSTER:
        await message.reply_photo(photo=VERIFY_POSTER, caption=caption, reply_markup=buttons)
    else:
        await message.reply_text(text=caption, reply_markup=buttons)

# ഉപയോക്താവ് വെരിഫിക്കേഷൻ ലിങ്ക് പൂർത്തിയാക്കി വരുമ്പോൾ ഡാറ്റാബേസ് അപ്ഡേറ്റ് ചെയ്യുന്നത്
@Client.on_message(filters.regex(r"^/start verify24_") & filters.private)
async def complete_24hrs_verification(client, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    params = message.text.split("_")
    data_user_id = params[1]
    file_id = params[2] if len(params) > 2 else None
    
    if str(user_id) == str(data_user_id):
        now = datetime.datetime.now(pytz.utc)
        await db.update_user(user_id, {"verified_time": now})
        
        caption = (
            f"<b>👏 HEY {first_name}, YOU'RE ARE SUCCESSFULLY VERIFIED ✅</b>\n\n"
            f"<b>NOW YOU'VE UNLIMITED ACCESS FOR {VERIFY_ACCESS_HOURS} HOURS 🥳</b>"
        )
        
        btn_list = []
        if file_id:
            file_link = f"https://telegram.me/{client.me.username}?start=file_{file_id}"
            btn_list.append([InlineKeyboardButton("CLICK HERE TO GET FILE", url=file_link)])
            
        buttons = InlineKeyboardMarkup(btn_list) if btn_list else None
        
        if VERIFIED_POSTER:
            await message.reply_photo(photo=VERIFIED_POSTER, caption=caption, reply_markup=buttons)
        else:
            await message.reply_text(text=caption, reply_markup=buttons)
    else:
        await message.reply_text("<b>⚠️ INVALID VERIFICATION LINK!</b>")
