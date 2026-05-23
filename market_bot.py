"""
╔══════════════════════════════════════════════════════════════╗
║         OASIS — MARKET BOT                                   ║
║         ระบบเช็คราคาตลาด Albion Online                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from datetime import datetime, timezone

TOKEN = os.getenv("DISCORD_TOKEN", "")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ══════════════════════════════════════════════════════
# ITEM DATA
# ══════════════════════════════════════════════════════

WEAPONS = {
    "⚔️ Sword": {
        "Broadsword": "SWORD",
        "Claymore": "TWOHANDED_SWORD",
        "Dual Swords": "DUALSWORD",
        "Carving Sword": "CURVED_SWORD",
        "Bloodletter": "DAGGER_PAIR",
        "Camlann Sword": "QUESTITEM_TOKEN_AVALON_SWORD",
    },
    "🪓 Axe": {
        "Battleaxe": "AXE",
        "Greataxe": "TWOHANDED_AXE",
        "Halberd": "HALBERD",
        "Carrioncaller": "CARRIONCALLER",
        "Bear Paws": "BEARPAWS",
    },
    "🔱 Spear": {
        "Spear": "SPEAR",
        "Pike": "PIKE",
        "Glaive": "GLAIVE",
        "Heron Spear": "HERON_SPEAR",
        "Trinity Spear": "TRINITY_SPEAR",
    },
    "🔨 Hammer": {
        "Hammer": "HAMMER",
        "Polehammer": "POLEHAMMER",
        "Great Hammer": "GREAT_HAMMER",
        "Tombhammer": "TOMBHAMMER",
        "Hand of Justice": "ARTIFACT_HAMMER",
    },
    "🗡️ Dagger": {
        "Dagger": "DAGGER",
        "Dagger Pair": "DAGGER_PAIR",
        "Claws": "CLAWS",
        "Deathgivers": "DEATHGIVERS",
        "Bloodletter": "BLOODLETTER",
    },
    "🏹 Bow": {
        "Bow": "BOW",
        "Warbow": "WARBOW",
        "Longbow": "LONGBOW",
        "Wailing Bow": "WAILING_BOW",
        "Bow of Badon": "BOW_OF_BADON",
    },
    "🏹 Crossbow": {
        "Crossbow": "CROSSBOW",
        "Heavy Crossbow": "HEAVY_CROSSBOW",
        "Light Crossbow": "LIGHT_CROSSBOW",
        "Weeping Repeater": "WEEPING_REPEATER",
        "Boltcasters": "BOLTCASTERS",
    },
    "🔥 Fire Staff": {
        "Fire Staff": "FIRESTAFF",
        "Great Fire Staff": "GREAT_FIRESTAFF",
        "Infernal Staff": "INFERNAL_STAFF",
        "Wildfire Staff": "WILDFIRE_STAFF",
        "Brimstone Staff": "BRIMSTONE_STAFF",
    },
    "❄️ Frost Staff": {
        "Frost Staff": "FROSTSTAFF",
        "Great Frost Staff": "GREAT_FROSTSTAFF",
        "Glacial Staff": "GLACIAL_STAFF",
        "Permafrost Prism": "PERMAFROST_PRISM",
        "Icicle Staff": "ICICLE_STAFF",
    },
    "☠️ Cursed Staff": {
        "Cursed Staff": "CURSEDSTAFF",
        "Great Cursed Staff": "GREAT_CURSEDSTAFF",
        "Damnation Staff": "DAMNATION_STAFF",
        "Lifecurse Staff": "LIFECURSE_STAFF",
        "Shadowcaller": "SHADOWCALLER",
    },
    "🌿 Nature Staff": {
        "Nature Staff": "NATURESTAFF",
        "Great Nature Staff": "GREAT_NATURESTAFF",
        "Druidic Staff": "DRUIDIC_STAFF",
        "Rampant Staff": "RAMPANT_STAFF",
        "Blight Staff": "BLIGHT_STAFF",
    },
    "✨ Holy Staff": {
        "Holy Staff": "HOLYSTAFF",
        "Great Holy Staff": "GREAT_HOLYSTAFF",
        "Fallen Staff": "FALLEN_STAFF",
        "Redemption Staff": "REDEMPTION_STAFF",
        "Hallowfall": "HALLOWFALL",
    },
    "🌀 Arcane Staff": {
        "Arcane Staff": "ARCANESTAFF",
        "Great Arcane Staff": "GREAT_ARCANESTAFF",
        "Witchwork Staff": "WITCHWORK_STAFF",
        "Occult Staff": "OCCULT_STAFF",
        "Malevolent Locus": "MALEVOLENT_LOCUS",
    },
    "🛡️ Mace": {
        "Mace": "MACE",
        "Heavy Mace": "HEAVY_MACE",
        "Flanged Mace": "FLANGED_MACE",
        "Incubus Mace": "INCUBUS_MACE",
        "Camlann Mace": "CAMLANN_MACE",
    },
    "⚡ Quarterstaff": {
        "Quarterstaff": "QUARTERSTAFF",
        "Iron-clad Staff": "IRONCLADSTAFF",
        "Double Bladed Staff": "DOUBLE_BLADED_STAFF",
        "Black Monk Stave": "BLACK_MONK_STAVE",
        "Soulscythe": "SOULSCYTHE",
    },
}

ARMORS = {
    "🧵 Cloth — หัว (Cowl)": {
        "Scholar Cowl": "HEAD_CLOTH_SCHOLAR",
        "Mage Cowl": "HEAD_CLOTH_MAGE",
        "Cultist Cowl": "HEAD_CLOTH_CULTIST",
        "Royal Cowl": "HEAD_CLOTH_ROYAL",
        "Druid Cowl": "HEAD_CLOTH_DRUID",
    },
    "🧵 Cloth — ตัว (Robe)": {
        "Scholar Robe": "ARMOR_CLOTH_SCHOLAR",
        "Mage Robe": "ARMOR_CLOTH_MAGE",
        "Cultist Robe": "ARMOR_CLOTH_CULTIST",
        "Royal Robe": "ARMOR_CLOTH_ROYAL",
        "Druid Robe": "ARMOR_CLOTH_DRUID",
    },
    "🧵 Cloth — เท้า (Sandals)": {
        "Scholar Sandals": "SHOES_CLOTH_SCHOLAR",
        "Mage Sandals": "SHOES_CLOTH_MAGE",
        "Cultist Sandals": "SHOES_CLOTH_CULTIST",
        "Royal Sandals": "SHOES_CLOTH_ROYAL",
        "Druid Sandals": "SHOES_CLOTH_DRUID",
    },
    "🥋 Leather — หัว (Hood)": {
        "Stalker Hood": "HEAD_LEATHER_STALKER",
        "Ranger Hood": "HEAD_LEATHER_RANGER",
        "Mercenary Hood": "HEAD_LEATHER_MERCENARY",
        "Assassin Hood": "HEAD_LEATHER_ASSASSIN",
        "Hunter Hood": "HEAD_LEATHER_HUNTER",
    },
    "🥋 Leather — ตัว (Jacket)": {
        "Stalker Jacket": "ARMOR_LEATHER_STALKER",
        "Ranger Jacket": "ARMOR_LEATHER_RANGER",
        "Mercenary Jacket": "ARMOR_LEATHER_MERCENARY",
        "Assassin Jacket": "ARMOR_LEATHER_ASSASSIN",
        "Hunter Jacket": "ARMOR_LEATHER_HUNTER",
    },
    "🥋 Leather — เท้า (Shoes)": {
        "Stalker Shoes": "SHOES_LEATHER_STALKER",
        "Ranger Shoes": "SHOES_LEATHER_RANGER",
        "Mercenary Shoes": "SHOES_LEATHER_MERCENARY",
        "Assassin Shoes": "SHOES_LEATHER_ASSASSIN",
        "Hunter Shoes": "SHOES_LEATHER_HUNTER",
    },
    "🪖 Plate — หัว (Helmet)": {
        "Soldier Helmet": "HEAD_PLATE_SOLDIER",
        "Knight Helmet": "HEAD_PLATE_KNIGHT",
        "Guardian Helmet": "HEAD_PLATE_GUARDIAN",
        "Royal Helmet": "HEAD_PLATE_ROYAL",
        "Demon Helmet": "HEAD_PLATE_DEMON",
    },
    "🪖 Plate — ตัว (Armor)": {
        "Soldier Armor": "ARMOR_PLATE_SOLDIER",
        "Knight Armor": "ARMOR_PLATE_KNIGHT",
        "Guardian Armor": "ARMOR_PLATE_GUARDIAN",
        "Royal Armor": "ARMOR_PLATE_ROYAL",
        "Demon Armor": "ARMOR_PLATE_DEMON",
    },
    "🪖 Plate — เท้า (Boots)": {
        "Soldier Boots": "SHOES_PLATE_SOLDIER",
        "Knight Boots": "SHOES_PLATE_KNIGHT",
        "Guardian Boots": "SHOES_PLATE_GUARDIAN",
        "Royal Boots": "SHOES_PLATE_ROYAL",
        "Demon Boots": "SHOES_PLATE_DEMON",
    },
}

CITIES = [
    "Caerleon", "Bridgewatch", "Martlock",
    "Thetford", "Lymhurst", "Fort Sterling", "Brecilien"
]

CITY_EMOJI = {
    "Caerleon": "🔴",
    "Bridgewatch": "🟠",
    "Martlock": "🔵",
    "Thetford": "🟤",
    "Lymhurst": "🟢",
    "Fort Sterling": "⚪",
    "Brecilien": "🟣",
}

TIERS = ["T4", "T5", "T6", "T7", "T8"]
ENCHANTS = [".0", ".1", ".2", ".3", ".4"]
QUALITIES = {
    "1": "Normal",
    "2": "Good",
    "3": "Outstanding",
    "4": "Excellent",
    "5": "Masterpiece"
}

API_BASE = "https://west.albion-online-data.com/api/v2/stats/prices"


# ══════════════════════════════════════════════════════
# API FETCH
# ══════════════════════════════════════════════════════
async def fetch_prices(item_id: str, quality: str) -> dict:
    locations = ",".join(CITIES)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    url = f"https://east.albion-online-data.com/api/v2/stats/prices/{item_id}.json?locations={locations}&qualities={quality}"
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    return await resp.json()
    except Exception:
        pass
    return []


def build_price_embed(item_name: str, item_id: str, tier: str, enchant: str, quality_num: str, data: list) -> discord.Embed:
    quality_name = QUALITIES.get(quality_num, "Normal")
    enchant_display = enchant if enchant != ".0" else ""
    title = f"💰 {tier}{enchant_display} {item_name} — {quality_name}"

    embed = discord.Embed(title=title, color=0xf39c12)

    sell_lines = ""
    buy_lines = ""
    sell_prices = []
    buy_prices = []

    city_data = {city: {"sell": 0, "buy": 0, "updated": None} for city in CITIES}

    for entry in data:
        city = entry.get("city", "")
        if city in city_data:
            city_data[city]["sell"] = entry.get("sell_price_min", 0)
            city_data[city]["buy"] = entry.get("buy_price_max", 0)
            city_data[city]["updated"] = entry.get("sell_price_min_date", None)

    for city in CITIES:
        emoji = CITY_EMOJI.get(city, "🏙️")
        sell = city_data[city]["sell"]
        buy = city_data[city]["buy"]
        updated = city_data[city]["updated"]

        # คำนวณเวลาที่อัปเดต
        time_str = "ไม่มีข้อมูล"
        if updated and updated != "0001-01-01T00:00:00":
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                diff = datetime.now(timezone.utc) - dt
                mins = int(diff.total_seconds() / 60)
                if mins < 60:
                    time_str = f"{mins}นาทีที่แล้ว"
                elif mins < 1440:
                    time_str = f"{mins//60}ชม.ที่แล้ว"
                else:
                    time_str = f"{mins//1440}วันที่แล้ว"
            except Exception:
                time_str = "ไม่ทราบ"

        sell_str = f"{sell:,}" if sell > 0 else "ไม่มีข้อมูล"
        buy_str = f"{buy:,}" if buy > 0 else "ไม่มีข้อมูล"

        sell_lines += f"{emoji} **{city}**\n💰 {sell_str} `{time_str}`\n"
        buy_lines += f"{emoji} **{city}**\n🤝 {buy_str}\n"

        if sell > 0:
            sell_prices.append((city, sell))
        if buy > 0:
            buy_prices.append((city, buy))

    embed.add_field(name="📤 Sell Order (ราคาขาย)", value=sell_lines or "ไม่มีข้อมูล", inline=True)
    embed.add_field(name="📥 Buy Order (ราคารับซื้อ)", value=buy_lines or "ไม่มีข้อมูล", inline=True)

    # สรุป
    summary = ""
    if sell_prices:
        cheapest = min(sell_prices, key=lambda x: x[1])
        priciest = max(sell_prices, key=lambda x: x[1])
        summary += f"🏷️ **ซื้อถูกสุด:** {cheapest[0]} — {cheapest[1]:,}\n"
        summary += f"💎 **ซื้อแพงสุด:** {priciest[0]} — {priciest[1]:,}\n"
    if buy_prices:
        best_sell = max(buy_prices, key=lambda x: x[1])
        summary += f"💵 **ขายได้ราคาดีสุด:** {best_sell[0]} — {best_sell[1]:,}"

    if summary:
        embed.add_field(name="━" * 30, value=summary, inline=False)

    embed.set_footer(text=f"ข้อมูลจาก Albion Online Data Project • {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    return embed


# ══════════════════════════════════════════════════════
# VIEWS
# ══════════════════════════════════════════════════════

class MarketMainView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="⚔️ อาวุธ", style=discord.ButtonStyle.primary)
    async def weapons(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.edit_message(
            embed=discord.Embed(title="⚔️ เลือกประเภทอาวุธ", color=0x9b59b6),
            view=CategorySelectView(list(WEAPONS.keys()), "weapon")
        )

    @discord.ui.button(label="🛡️ เกราะ", style=discord.ButtonStyle.primary)
    async def armors(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.edit_message(
            embed=discord.Embed(title="🛡️ เลือกประเภทเกราะ", color=0x9b59b6),
            view=CategorySelectView(list(ARMORS.keys()), "armor")
        )


class CategorySelectView(discord.ui.View):
    def __init__(self, categories: list, cat_type: str):
        super().__init__(timeout=120)
        self.add_item(CategoryDropdown(categories, cat_type))

    @discord.ui.button(label="◀️ กลับ", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.edit_message(
            embed=discord.Embed(title="🏪 Albion Market", description="เลือกหมวดหมู่ที่ต้องการค่ะ", color=0x9b59b6),
            view=MarketMainView()
        )


class CategoryDropdown(discord.ui.Select):
    def __init__(self, categories: list, cat_type: str):
        self.cat_type = cat_type
        options = [discord.SelectOption(label=cat, value=cat) for cat in categories[:25]]
        super().__init__(placeholder="เลือกประเภท...", options=options)

    async def callback(self, i: discord.Interaction):
        cat = self.values[0]
        items = WEAPONS.get(cat) or ARMORS.get(cat) or {}
        await i.response.edit_message(
            embed=discord.Embed(title=f"{cat}\nเลือกไอเทม", color=0x9b59b6),
            view=ItemSelectView(cat, items)
        )


class ItemSelectView(discord.ui.View):
    def __init__(self, cat: str, items: dict):
        super().__init__(timeout=120)
        self.cat = cat
        self.add_item(ItemDropdown(cat, items))

    @discord.ui.button(label="◀️ กลับ", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, i: discord.Interaction, b: discord.ui.Button):
        cat_type = "weapon" if self.cat in WEAPONS else "armor"
        categories = list(WEAPONS.keys()) if cat_type == "weapon" else list(ARMORS.keys())
        title = "⚔️ เลือกประเภทอาวุธ" if cat_type == "weapon" else "🛡️ เลือกประเภทเกราะ"
        await i.response.edit_message(
            embed=discord.Embed(title=title, color=0x9b59b6),
            view=CategorySelectView(categories, cat_type)
        )


class ItemDropdown(discord.ui.Select):
    def __init__(self, cat: str, items: dict):
        self.cat = cat
        self.items = items
        options = [discord.SelectOption(label=name, value=name) for name in list(items.keys())[:25]]
        super().__init__(placeholder="เลือกไอเทม...", options=options)

    async def callback(self, i: discord.Interaction):
        item_name = self.values[0]
        item_base_id = self.items[item_name]
        await i.response.edit_message(
            embed=discord.Embed(
                title=f"🎯 {item_name}",
                description="เลือก Tier, Enchantment และ Quality ได้เลยค่ะ",
                color=0x9b59b6
            ),
            view=TierEnchantQualityView(item_name, item_base_id, self.cat)
        )


class TierEnchantQualityView(discord.ui.View):
    def __init__(self, item_name: str, item_base_id: str, cat: str):
        super().__init__(timeout=120)
        self.item_name = item_name
        self.item_base_id = item_base_id
        self.cat = cat
        self.selected_tier = "T8"
        self.selected_enchant = ".0"
        self.selected_quality = "1"

        self.add_item(TierDropdown(self))
        self.add_item(EnchantDropdown(self))
        self.add_item(QualityDropdown(self))

    @discord.ui.button(label="◀️ กลับ", style=discord.ButtonStyle.secondary, row=3)
    async def back(self, i: discord.Interaction, b: discord.ui.Button):
        items = WEAPONS.get(self.cat) or ARMORS.get(self.cat) or {}
        await i.response.edit_message(
            embed=discord.Embed(title=f"{self.cat}\nเลือกไอเทม", color=0x9b59b6),
            view=ItemSelectView(self.cat, items)
        )

    @discord.ui.button(label="✅ ดูราคา", style=discord.ButtonStyle.success, row=3)
    async def confirm(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.defer()

        # สร้าง item_id
        tier_num = self.selected_tier[1]
        enchant_num = self.selected_enchant.replace(".", "")
        if enchant_num == "0":
            item_id = f"T{tier_num}_{self.item_base_id}"
        else:
            item_id = f"T{tier_num}_{self.item_base_id}@{enchant_num}"

        data = await fetch_prices(item_id, self.selected_quality)
        embed = build_price_embed(
            self.item_name, item_id,
            self.selected_tier, self.selected_enchant,
            self.selected_quality, data
        )
        await i.edit_original_response(
            embed=embed,
            view=RefreshView(self.item_name, self.item_base_id, self.cat,
                           self.selected_tier, self.selected_enchant, self.selected_quality)
        )


class TierDropdown(discord.ui.Select):
    def __init__(self, parent):
        self.parent = parent
        options = [discord.SelectOption(label=t, value=t, default=(t == "T8")) for t in TIERS]
        super().__init__(placeholder="🎯 เลือก Tier...", options=options, row=0)

    async def callback(self, i: discord.Interaction):
        self.parent.selected_tier = self.values[0]
        for opt in self.options:
            opt.default = opt.value == self.values[0]
        await i.response.edit_message(view=self.parent)


class EnchantDropdown(discord.ui.Select):
    def __init__(self, parent):
        self.parent = parent
        options = [discord.SelectOption(label=e, value=e, default=(e == ".0")) for e in ENCHANTS]
        super().__init__(placeholder="✨ เลือก Enchantment...", options=options, row=1)

    async def callback(self, i: discord.Interaction):
        self.parent.selected_enchant = self.values[0]
        for opt in self.options:
            opt.default = opt.value == self.values[0]
        await i.response.edit_message(view=self.parent)


class QualityDropdown(discord.ui.Select):
    def __init__(self, parent):
        self.parent = parent
        options = [
            discord.SelectOption(label=f"{v}", value=k, default=(k == "1"))
            for k, v in QUALITIES.items()
        ]
        super().__init__(placeholder="💎 เลือก Quality...", options=options, row=2)

    async def callback(self, i: discord.Interaction):
        self.parent.selected_quality = self.values[0]
        for opt in self.options:
            opt.default = opt.value == self.values[0]
        await i.response.edit_message(view=self.parent)


class RefreshView(discord.ui.View):
    def __init__(self, item_name, item_base_id, cat, tier, enchant, quality):
        super().__init__(timeout=120)
        self.item_name = item_name
        self.item_base_id = item_base_id
        self.cat = cat
        self.tier = tier
        self.enchant = enchant
        self.quality = quality

    @discord.ui.button(label="🔄 Refresh", style=discord.ButtonStyle.primary)
    async def refresh(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.defer()
        tier_num = self.tier[1]
        enchant_num = self.enchant.replace(".", "")
        if enchant_num == "0":
            item_id = f"T{tier_num}_{self.item_base_id}"
        else:
            item_id = f"T{tier_num}_{self.item_base_id}@{enchant_num}"
        data = await fetch_prices(item_id, self.quality)
        embed = build_price_embed(self.item_name, item_id, self.tier, self.enchant, self.quality, data)
        await i.edit_original_response(embed=embed, view=self)

    @discord.ui.button(label="🔍 ค้นหาใหม่", style=discord.ButtonStyle.secondary)
    async def new_search(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.edit_message(
            embed=discord.Embed(title="🏪 Albion Market", description="เลือกหมวดหมู่ที่ต้องการค่ะ", color=0x9b59b6),
            view=MarketMainView()
        )


# ══════════════════════════════════════════════════════
# SLASH COMMAND
# ══════════════════════════════════════════════════════
@bot.tree.command(name="market", description="เช็คราคาไอเทมใน Albion Online")
async def market_cmd(i: discord.Interaction):
    await i.response.send_message(
        embed=discord.Embed(
            title="🏪 Albion Market",
            description="เลือกหมวดหมู่ที่ต้องการค่ะ",
            color=0x9b59b6
        ),
        view=MarketMainView(),
        ephemeral=True
    )


# ══════════════════════════════════════════════════════
# EVENTS
# ══════════════════════════════════════════════════════
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Market Bot ONLINE: {bot.user}")
        print(f"✅ Slash synced: {len(synced)}")
    except Exception as e:
        print(f"❌ Sync error: {e}")


if __name__ == "__main__":
    if not TOKEN:
        print("❌ DISCORD_TOKEN not set!")
    else:
        bot.run(TOKEN)
