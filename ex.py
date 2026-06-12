import requests
from bs4 import BeautifulSoup

from userbot import catub
from ..core.managers import edit_or_reply

plugin_category = "utils"


# =========================
# 💵 USD IRR (TGJU)
# =========================
def get_usd():
    try:
        r = requests.get(
            "https://www.tgju.org/profile/price_dollar_rl",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(r.text, "html.parser")
        tag = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
        return int(tag.text.replace(",", "").strip()) if tag else None
    except:
        return None


# =========================
# 🌍 FX
# =========================
def get_fx():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10)
        return r.json().get("rates", {})
    except:
        return {}


# =========================
# ₿ CRYPTO
# =========================
def get_crypto():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": "bitcoin,ethereum,bnb,ripple,dogecoin,toncoin",
                "vs_currencies": "usd"
            },
            timeout=10
        )
        return r.json()
    except:
        return {}


@catub.cat_cmd(pattern="exchange$")
async def exchange(event):

    msg = await edit_or_reply(event, "`📡 درحال دریافت بازار...`")

    # 🔥 همه دیتاها یکجا
    usd = get_usd()
    fx = get_fx()
    crypto = get_crypto()

    # ❌ اگر فقط دلار نیومد
    if not usd:
        return await msg.edit("❌ خطا در دریافت بازار (TGJU)")

    text = "📊 بازار لحظه‌ای\n━━━━━━━━━━━━━━\n\n"

    # 💵 دلار
    text += f"💵 دلار : `{usd}`\n\n"

    # 🌍 ارزها
    currencies = {
        "💶 یورو": "EUR",
        "💷 پوند": "GBP",
        "🇦🇪 درهم": "AED",
        "🇹🇷 لیر": "TRY",
        "🇦🇫 افغانی": "AFN",
        "🇨🇦 کانادا": "CAD",
        "🇦🇺 استرالیا": "AUD",
        "🇨🇭 فرانک": "CHF",
        "🇨🇳 یوان": "CNY",
        "🇯🇵 ین": "JPY",
        "🇷🇺 روبل": "RUB",
        "🇸🇦 ریال": "SAR",
        "🇮🇳 روپیه": "INR",
        "🇵🇰 پاکستان": "PKR",
        "🇰🇼 دینار": "KWD",
        "🇶🇦 قطر": "QAR",
        "🇴🇲 عمان": "OMR",
        "🇧🇭 بحرین": "BHD",
    }

    if fx:
        for name, code in currencies.items():
            rate = fx.get(code)
            if rate:
                text += f"{name} : `{int(usd / rate)}`\n"

    # ₿ کریپتو
    text += "\n━━━━━━━━━━━━━━\n₿ کریپتو\n━━━━━━━━━━━━━━\n"

    crypto_map = {
        "bitcoin": "₿ بیت کوین",
        "ethereum": "♦️ اتریوم",
        "bnb": "🟡 بایننس",
        "ripple": "🔵 ریپل",
        "dogecoin": "🐕 دوج",
        "toncoin": "💎 تون",
    }

    if crypto:
        for key, name in crypto_map.items():
            if key in crypto:
                price = crypto[key].get("usd")
                if price:
                    text += f"{name} : `{int(price * usd)}`\n"

    await msg.edit(text)git