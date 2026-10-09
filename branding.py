"""Central, user-facing Anujith ALLU TV SERIALS branding.

Internal package, class, database, and legacy environment names intentionally
remain unchanged so existing deployments and indexed data keep working.
"""

from os import environ


BRAND_NAME = environ.get("BRAND_NAME", "Anujith ALLU TV SERIALS")
BRAND_SHORT_NAME = environ.get("BRAND_SHORT_NAME", "Anujith ALLU TV SERIALS")
BRAND_TAGLINE = environ.get(
    "BRAND_TAGLINE",
    "SEARCH • STREAM • DOWNLOAD",
)

UPDATE_CHANNEL_LINK = environ.get(
    "CHNL_LNK",
    "https://t.me/AlluTvSerials",
)
MOVIE_GROUP_LINK = environ.get(
    "GRP_LNK",
    "https://t.me/AlluTvSerialGroup",
)
OWNER_LINK = environ.get(
    "OWNER_LNK",
    "https://t.me/Anujith1238",
)
MOVIE_UPDATE_LINK = environ.get(
    "DEENDAYAL_MOVIE_UPDATE_CHANNEL_LNK",
    "https://t.me/AlluTvSerials",
)

# Preserve upstream attribution unless the deployer supplies their own repo.
SOURCE_CODE_LINK = environ.get(
    "SOURCE_CODE_LINK",
    "https://github.com/RDX-EXPART/Rdx-auto-filter",
)

PROFILE_LOGO = environ.get(
    "PROFILE_LOGO",
    "https://files.catbox.moe/dc6g71.jpg",
)
WELCOME_BANNER = environ.get(
    "WELCOME_BANNER",
    "https://files.catbox.moe/dc6g71.jpg",
)
NO_RESULTS_BANNER = environ.get(
    "NO_RESULTS_BANNER",
    "https://files.catbox.moe/4nmdy0.jpg",
)
JOIN_CHANNEL_BANNER = environ.get(
    "JOIN_CHANNEL_BANNER",
    "https://files.catbox.moe/iyjprx.jpg",
)
PREMIUM_BANNER = environ.get(
    "PREMIUM_BANNER",
    "https://files.catbox.moe/pgq1l5.jpg",
)
