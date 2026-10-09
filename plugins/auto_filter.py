import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# ==========================================
# CHANNEL SETTINGS
# ==========================================

CHANNELS = [-1003911112940]

AUTH_CHANNEL = -1003926879089

BOT_USERNAME = "Anujith1_bot"

BANNER_PHOTO = "https://ibb.co/cS5zrTGD"


# ==========================================
# AUTO POST FORMATTER
# ==========================================

@Client.on_message(
    filters.chat(CHANNELS) & (filters.document | filters.video)
)
async def auto_post_formatter(client, message):

    try:
        # 1. ORIGINAL FILE NAME

        if message.document:
            file_name_raw = message.document.file_name or "Media File"
        elif message.video:
            file_name_raw = message.video.file_name or "Media File"
        else:
            return

        # 2. SEASON DETECTION

        season_match = re.search(
            r'\b(?:S|Season[ ._-]*)(\d+)\b',
            file_name_raw,
            re.IGNORECASE
        )

        season = (
            season_match.group(1).zfill(2)
            if season_match else "01"
        )

        # 3. EPISODE DETECTION
        # Supports S01E739, S01E769-E772,
        # S01E769-772 and Episode 769-772

        episode_match = re.search(
            r'\bS\d+[ ._-]*E(?:P(?:ISODE)?)?[ ._-]*'
            r'(\d+)(?:[ ._-]*-[ ._-]*(?:E)?(\d+))?',
            file_name_raw,
            re.IGNORECASE
        )

        if not episode_match:
            episode_match = re.search(
                r'\bEpisode[ ._-]*(\d+)'
                r'(?:[ ._-]*-[ ._-]*(\d+))?',
                file_name_raw,
                re.IGNORECASE
            )

        if not episode_match:
            episode_match = re.search(
                r'\bE[ ._-]*(\d+)'
                r'(?:[ ._-]*-[ ._-]*E?[ ._-]*(\d+))?',
                file_name_raw,
                re.IGNORECASE
            )

        if episode_match:
            start_episode = episode_match.group(1)
            end_episode = episode_match.group(2)

            if end_episode:
                episode_num = f"{start_episode}-{end_episode}"
            else:
                episode_num = start_episode
        else:
            episode_num = "1"

        # 4. MULTIPLE QUALITY DETECTION

        quality_matches = re.findall(
            r'(?<!\d)(2160p|1440p|1080p|720p|480p|360p)(?!\w)',
            file_name_raw,
            re.IGNORECASE
        )

        # Duplicate qualities ഒഴിവാക്കുന്നു
        qualities = list(dict.fromkeys(
            q.lower() for q in quality_matches
        ))

        quality = ", ".join(qualities) if qualities else "N/A"

        # 5. CLEAN SERIAL NAME

        clean_name = file_name_raw

        # File extension remove
        clean_name = re.sub(
            r'\.(mkv|mp4|avi|mov|webm|m4v)$',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Remove Season
        clean_name = re.sub(
            r'\bSeason[ ._-]*\d+\b',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Remove S01E739 and episode ranges
        clean_name = re.sub(
            r'\bS\d+[ ._-]*E(?:P(?:ISODE)?)?[ ._-]*\d+'
            r'(?:[ ._-]*-[ ._-]*(?:E)?\d+)?',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Remove Episode 769-772
        clean_name = re.sub(
            r'\bEpisode[ ._-]*\d+'
            r'(?:[ ._-]*-[ ._-]*\d+)?',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Remove E739 and E769-E772
        clean_name = re.sub(
            r'\bE[ ._-]*\d+'
            r'(?:[ ._-]*-[ ._-]*E?[ ._-]*\d+)?',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Remove quality tags
        clean_name = re.sub(
            r'(?<!\d)(2160p|1440p|1080p|720p|480p|360p)(?!\w)',
            '',
            clean_name,
            flags=re.IGNORECASE
        )

        # Clean separators and spaces
        clean_name = re.sub(r'[._]+', ' ', clean_name)
        clean_name = re.sub(r'\s+', ' ', clean_name)
        clean_name = clean_name.strip(' -_.')

        if not clean_name:
            clean_name = "Malayalam Serial"

        # 6. CAPTION
        # Labels മാത്രം Bold ആണ്

        caption = (
            f"📁 <b>File Name :</b> {clean_name}\n"
            f"🎞️ <b>Season :</b> {season}\n"
            f"📌 <b>Episode :</b> {episode_num}\n"
            f"🎬 <b>Quality :</b> {quality}"
        )

        # 7. GET FILE BUTTON

        formatted_name_for_link = clean_name.replace(" ", "")
        episode_str = f"E{episode_num}"

        bot_link = (
            f"https://telegram.me/{BOT_USERNAME}"
            f"?start=getfile-{formatted_name_for_link}"
            f"-S{season}{episode_str}"
        )

        reply_markup = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "📥 Get File",
                    url=bot_link
                )
            ]]
        )

        # 8. SEND PHOTO + CAPTION + BUTTON

        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )

        print(
            f"Auto-post successful: {clean_name} "
            f"- Episode {episode_num} - Quality {quality}"
        )

    except Exception as e:
        print(f"Auto-Formatter Error: {e}")
