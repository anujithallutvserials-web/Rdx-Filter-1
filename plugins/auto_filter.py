import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ഇവിടെ ചാനൽ ഐഡികൾ നൽകുക
CHANNELS = [-1003911112940]      # ഫയലുകൾ പരിശോധിക്കേണ്ട ചാനൽ ഐഡി
AUTH_CHANNEL = -1003926879089   # പോസ്റ്റും ഫോട്ടോയും അയക്കേണ്ട ചാനൽ ഐഡി

# നിങ്ങൾ നൽകിയ സീരിയലുകളുടെ മാപ്പിംഗ് ലിസ്റ്റ്
SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri": "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena",
    "santhwanam 2": "Santhwanam 2"
}

# ഒരുമിച്ച് വരുന്ന ഫയലുകൾ ശേഖരിക്കാൻ (Batch Collection)
batch_storage = {}
batch_timers = {}

async def process_batch(client, serial_key):
    """ഒരു ബാച്ചിലെ മുഴുവൻ ഫയലുകളും പരിശോധിച്ച് മിനിമം, മാക്സിമം എപ്പിസോഡുകൾ കണ്ടെത്തി പോസ്റ്റ് ചെയ്യുന്നു"""
    await asyncio.sleep(3) # എല്ലാ ഫയലുകളും എത്തുന്നതുവരെ 3 സെക്കൻഡ് കാത്തിരിക്കുന്നു
    
    if serial_key not in batch_storage:
        return

    items = batch_storage.pop(serial_key)
    if serial_key in batch_timers:
        del batch_timers[serial_key]

    for data in items:
        file_name_raw = data["file_name"]
        season = data["season"]
        quality = data["quality"]
        clean_name = data["clean_name"]
        is_from_mapping = data["is_from_mapping"]
        all_eps = data["all_eps"]

        # കിട്ടിയ എല്ലാ എപ്പിസോഡുകളിൽ നിന്നും ഏറ്റവും ചെറുതും വലുതും കണ്ടെത്തുന്നു
        if len(all_eps) > 1:
            min_ep = min(all_eps)
            max_ep = max(all_eps)
            if min_ep != max_ep:
                episode_str = f"{min_ep}-{max_ep}"
            else:
                episode_str = str(min_ep)
        elif len(all_eps) == 1:
            episode_str = str(all_eps[0])
        else:
            episode_str = "1"

        BOT_USERNAME = "Anujith1_bot"

        # ലിങ്കുകൾ തയ്യാറാക്കുന്നു
        if is_from_mapping:
            formatted_name_for_link = clean_name.replace(" ", "")
            bot_link = f"https://telegram.me/{BOT_USERNAME}?start=getfile-{formatted_name_for_link}"
        else:
            formatted_name_for_link = clean_name.replace(" ", "")
            first_ep = episode_str.split('-')[0]
            bot_link = f"https://telegram.me/{BOT_USERNAME}?start=getfile-{formatted_name_for_link}-S{season}E{first_ep}"

        # ക്യാപ്ഷൻ ഫോർമാറ്റ്
        caption = (
            f"📁 **File Name :** {clean_name}\n"
            f"🎞️ **Season :** {season}\n"
            f"📌 **Episode :** {episode_str}\n"
            f"🎬 **Quality :** {quality}"
        )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Get File", url=bot_link)]]
        )

        BANNER_PHOTO = "https://ibb.co/cS5zrTGD"

        try:
            await client.send_photo(
                chat_id=AUTH_CHANNEL,
                photo=BANNER_PHOTO,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode="markdown"
            )
        except Exception as e:
            print(f"Send Error: {e}")

@Client.on_message(filters.chat(CHANNELS) & (filters.document | filters.video))
async def auto_post_formatter(client, message):
    try:
        if message.document:
            file_name_raw = message.document.file_name
        elif message.video:
            file_name_raw = message.video.file_name or "Media File"
        else:
            return

        # സീസൺ കണ്ടെത്തുന്നു
        season_match = re.search(r'(?:s|season\s*)(\d+)', file_name_raw, re.IGNORECASE)
        season = season_match.group(1).zfill(2) if season_match else "01"

        # ഫയൽ നാമത്തിലുള്ള എപ്പിസോഡ് നമ്പറുകൾ കണ്ടെത്തുന്നു
        episodes_found = re.findall(r'(?:e|episode\s*)?(\d+)', file_name_raw, re.IGNORECASE)
        valid_eps = []
        for ep in episodes_found:
            if len(ep) <= 4 and int(ep) < 5000:
                valid_eps.append(int(ep))

        # സീസൺ നമ്പർ ഒഴിവാക്കി ബാക്കിയുള്ളവ എപ്പിസോഡ് ആയി പരിഗണിക്കുന്നു
        file_eps = [e for e in valid_eps if e != int(season)]
        if not file_eps and valid_eps:
            file_eps = valid_eps

        # ക്വാളിറ്റി കണ്ടെത്തുന്നു
        quality_match = re.search(r'(\d{3,4}p)', file_name_raw, re.IGNORECASE)
        quality = quality_match.group(1) if quality_match else "N/A"

        # സീരിയൽ പേര് മാപ്പിംഗ് ലിസ്റ്റിൽ ഉണ്ടോ എന്ന് നോക്കുന്നു
        clean_name = None
        lower_file_name = file_name_raw.lower()
        sorted_serials = sorted(SERIALS_MAPPING.keys(), key=len, reverse=True)
        
        is_from_mapping = False
        for key in sorted_serials:
            normalized_key = key.replace("_", " ").lower()
            if normalized_key in lower_file_name or key in lower_file_name:
                clean_name = SERIALS_MAPPING[key]
                is_from_mapping = True
                break

        if not clean_name:
            temp_name = re.sub(r's\d+|season\s*\d+|e\d+|episode\s*\d+|\d{3,4}p|web-dl|hdtv|mkv|mp4|hevc', '', file_name_raw, flags=re.IGNORECASE)
            clean_name = temp_name.replace('.', ' ').replace('_', ' ').strip()
            if not clean_name:
                clean_name = "Malayalam Serial"

        serial_key = clean_name.lower()

        if serial_key not in batch_storage:
            batch_storage[serial_key] = []

        # ഈ ഫയലിൽ കിട്ടിയ എപ്പിസോഡുകൾ സ്റ്റോറേജിലേക്ക് ചേർക്കുന്നു
        batch_storage[serial_key].append({
            "file_name": file_name_raw,
            "season": season,
            "quality": quality,
            "clean_name": clean_name,
            "is_from_mapping": is_from_mapping,
            "all_eps": file_eps
        })

        # ബാച്ച് പ്രോസസ്സിing ടൈമർ മാനേജ് ചെയ്യുക
        if serial_key in batch_timers:
            batch_timers[serial_key].cancel()
        
        batch_timers[serial_key] = asyncio.create_task(process_batch(client, serial_key))

    except Exception as e:
        print(f"Auto-Formatter Error: {e}")
