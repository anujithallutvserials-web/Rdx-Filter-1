import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# ==========================================
# BOT SETTINGS
# ==========================================

CHANNELS = [-1003911112940]
AUTH_CHANNEL = -1003926879089

BOT_USERNAME = "Anujith1_bot"
BANNER_PHOTO = "https://ibb.co/cS5zrTGD"


# ==========================================
# SERIAL MAPPING
# ==========================================

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
    "santhwanam": "Santhwanam 2",
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
    "oru_chiri_iru_chiri_bumper_chiri":
        "Oru Chiri Iru Chiri Bumper Chiri",
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
}


# ==========================================
# VIDEO QUALITY PATTERN
# QUALITY AUTOMATICALLY DETECTED
# ==========================================

# Examples: 720p, 576p, 480p, 360p, 280p, 180p
# Examples are not a fixed list.
# Other 3- or 4-digit p tags are detected automatically.

QUALITY_PATTERN = r"(?<!\d)(\d{3,4})\s*[pP](?!\w)"


# ==========================================
# GET ORIGINAL FILE NAME
# ==========================================

def get_file_name(message):
    if message.document:
        return message.document.file_name or "Media File"

    if message.video:
        return message.video.file_name or "Media File"

    return "Media File"


# ==========================================
# FIND SERIAL NAME
# ==========================================

def find_serial_name(filename):
    normalized = re.sub(r"[._-]+", " ", filename.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()

    mapping_items = sorted(
        SERIALS_MAPPING.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, display_name in mapping_items:
        search_name = key.replace("_", " ").lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(search_name)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized):
            return display_name

    return clean_unknown_name(filename)


# ==========================================
# CLEAN UNKNOWN SERIAL NAME
# ==========================================

def clean_unknown_name(filename):
    name = re.sub(
        r"\.(mkv|mp4|avi|mov|webm|m4v|mpeg|mpg)$",
        "",
        filename,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bS\d+[ ._-]*E(?:P(?:ISODE)?)?[ ._-]*\d+"
        r"(?:[ ._-]*-[ ._-]*E?\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bSeason[ ._-]*\d+\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bEpisode[ ._-]*\d+(?:[ ._-]*-[ ._-]*\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    # Remove detected quality tags from unknown serial names.
    name = re.sub(
        QUALITY_PATTERN,
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\b(HS|WEB|WEB-DL|HDRIP|HDTV|X264|X265)\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(r"[._]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip(" -_.") or "Malayalam Serial"


# ==========================================
# GET SEASON
# Supports S02E739, S2E739, Season 2
# ==========================================

def get_season(filename):

    # First priority: S02E739 / S2E739
    match = re.search(
        r"(?<![A-Za-z0-9])S(\d+)\s*E\d+",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    # Second priority: Season 02 / Season 2
    match = re.search(
        r"\bSeason[ ._-]*(\d+)\b",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    # Third priority: S02 by itself
    match = re.search(
        r"(?<![A-Za-z0-9])S(\d{1,2})(?![A-Za-z0-9])",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    return "01"


# ==========================================
# GET EPISODE NUMBER / RANGE
# ==========================================

def get_episode(filename):

    patterns = [
        # S02E739
        # S01E769-E772
        # S01E769-772
        (
            r"(?<![A-Za-z0-9])S\d+\s*E\s*(\d+)"
            r"(?:\s*-\s*E?\s*(\d+))?"
        ),

        # Season 2 Episode 739
        (
            r"\bSeason\s*\d+\s*"
            r"(?:Episode|Ep|E)\s*(\d+)"
            r"(?:\s*-\s*(\d+))?"
        ),

        # Episode 739 / Episode 769-772
        (
            r"\bEpisode\s*(\d+)"
            r"(?:\s*-\s*(\d+))?"
        ),

        # EP739 / EP 739
        (
            r"\bEP\s*(\d+)"
            r"(?:\s*-\s*(\d+))?"
        ),

        # E739 / E739-E740
        (
            r"(?<![A-Za-z0-9])E\s*(\d+)"
            r"(?:\s*-\s*E?\s*(\d+))?"
        ),
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            filename,
            re.IGNORECASE
        )

        if match:
            start = match.group(1)
            end = match.group(2)

            if end:
                return f"{start}-{end}"

            return start

    return "1"


# ==========================================
# GET VIDEO QUALITY AUTOMATICALLY
# ==========================================

def get_quality(filename):

    # Find quality tags dynamically from the original filename.
    # Examples: 576p, 280p, 180p, 720p, 1080p, etc.

    matches = re.findall(
        QUALITY_PATTERN,
        filename,
        re.IGNORECASE
    )

    # Keep order and remove duplicate qualities.
    qualities = list(dict.fromkeys(
        f"{number}p" for number in matches
    ))

    if qualities:
        return ", ".join(qualities)

    # Alternative quality labels
    normalized = filename.lower()

    if re.search(r"(?<!\w)4k(?!\w)", normalized):
        return "4K"

    if re.search(r"(?<!\w)fhd(?!\w)", normalized):
        return "FHD"

    if re.search(r"(?<!\w)hd(?!\w)", normalized):
        return "HD"

    if re.search(r"(?<!\w)sd(?!\w)", normalized):
        return "SD"

    return "N/A"


# ==========================================
# GET CLEAN SERIAL NAME
# ==========================================

def get_clean_serial_name(filename):
    return find_serial_name(filename)


# ==========================================
# GET FILE LINK
# SERIAL NAME ONLY
# ==========================================

def make_start_link(serial_name):

    slug = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        serial_name
    ).strip("-")

    payload = f"getfile-{slug}"

    return (
        f"https://telegram.me/{BOT_USERNAME}"
        f"?start={payload}"
    )


# ==========================================
# AUTO POST FORMATTER
# ==========================================

@Client.on_message(
    filters.chat(CHANNELS)
    & (filters.document | filters.video)
)
async def auto_post_formatter(client, message):

    try:
        filename = get_file_name(message)

        # File Name — existing mapping logic unchanged
        serial_name = get_clean_serial_name(filename)

        # Extract information from the ORIGINAL filename
        season = get_season(filename)
        episode = get_episode(filename)
        quality = get_quality(filename)

        caption = (
            f"📁 <b>File Name :</b> {serial_name}\n"
            f"🎞️ <b>Season :</b> {season}\n"
            f"📌 <b>Episode :</b> {episode}\n"
            f"🎬 <b>Quality :</b> {quality}"
        )

        # Get File link — existing logic unchanged
        bot_link = make_start_link(serial_name)

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📥 Get File",
                        url=bot_link
                    )
                ]
            ]
        )

        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons
        )

        print(
            "Auto-post successful | "
            f"Filename: {filename} | "
            f"Name: {serial_name} | "
            f"Season: {season} | "
            f"Episode: {episode} | "
            f"Quality: {quality}"
        )

    except Exception as error:
        print(f"Auto-Formatter Error: {error}")
