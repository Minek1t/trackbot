import aiogram
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, html, types
import asyncio
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import aiohttp
from datetime import datetime, timedelta
import os
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandObject
api = "https://api.joshlei.com/v2/growagarden/stock"
headers = {
    "accept": "application/json",
    "jstudio-key": "js_5206ce450dc0d41f7b0e1be99f91a250e760d31fc8d57d95a43ac54a4b4036a8"
}

bot = Bot(token="8124323700:AAHWqJdpI_wsdI3oa1jY9NM_MCgfi4ZEq20")
dp = Dispatcher()
SUBSCRIBERS_FILE = "subscribed_chats.json"
BANS_FILE = "BANS.json"
USER_SETTINGS_FILE = "user_settings.json"
ADMIN = [5064011310]


def load_bans():

    try:
        if os.path.exists(BANS_FILE):
            with open(BANS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки подписчиков: {e}")
        return []

def save_bans(BANS):

    try:
        with open(BANS_FILE, 'w') as f:
            json.dump(BANS, f)
    except Exception as e:
        print(f"Ошибка сохранения подписчиков: {e}")

def add_bans(text):

    bans = load_bans()
    if text not in bans:
        bans.append(text)
        save_bans(bans)
        return True
    return False

def remove_bans(text):

    bans = load_bans()
    if text in bans:
        bans.remove(text)
        save_bans(bans)
        return True
    return False


def load_subscribers():

    try:
        if os.path.exists(SUBSCRIBERS_FILE):
            with open(SUBSCRIBERS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки подписчиков: {e}")
        return []

def save_subscribers(subscribers):

    try:
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(subscribers, f)
    except Exception as e:
        print(f"Ошибка сохранения подписчиков: {e}")

def add_subscriber(chat_id):

    subscribers = load_subscribers()
    if chat_id not in subscribers:
        subscribers.append(chat_id)
        save_subscribers(subscribers)
        return True
    return False

def remove_subscriber(chat_id):

    subscribers = load_subscribers()
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers(subscribers)
        return True
    return False

#async def notify_subscribers(text):

#    subscribers = load_subscribers()
 #   for chat_id in subscribers:
  #      try:
   #         await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
    #    except Exception as e:
     #       print(f"Не удалось отправить сообщение {chat_id}: {e}")
      #      # Удаляем неактивных подписчиков
       #     remove_subscriber(chat_id)


print("BOT POWER IS ON\n press ctrl+c to exit")



EMOJI_MAP = {
    "carrot": "🥕",
    "strawberry": "🍓",
    "orange_tulip": "🌷",
    "blueberry": "🫐",
    "tomato": "🍅",
    "corn": "🌽",
    "daffodil": "🏵️",
    "watermelon": "🍉",
    "pumpkin": "🎃",
    "apple": "🍎",
    "bamboo": "🎋",
    "coconut": "🥥",
    "cactus": "🌵",
    "dragon_fruit": "🐉",
    "mango": "🥭",
    "grape": "🍇",
    "mushroom": "🍄",
    "pepper": "🌶️",
    "cacao": "🍫",
    "beanstalk": "🫛",
    "ember_lily": "🔥",
    "sugar_apple": "🍏",
    "burning_bud": "🌸",
    "giant_pinecone": "🥔",
    "elder_strawberry": "🔴🍓",
    "romanesco": "🥬",
}            

PRICE = {
    "carrot": "10$",
    "strawberry": "50$",
    "orange_tulip": "600$",
    "blueberry": "400$",
    "tomato": "800$",
    "corn": "1,300$",
    "daffodil": "1,000$",
    "watermelon": "2,500$",
    "pumpkin": "3,000$",
    "apple": "3,250$",
    "bamboo": "4,000$",
    "coconut": "6,000$",
    "cactus": "15,000$",
    "dragon_fruit": "50,000$",
    "mango": "100,000$",
    "grape": "850,000$",
    "mushroom": "150,000$",
    "pepper": "1,000,000$",
    "cacao": "2,500,000$",
    "beanstalk": "10,000,000$",
    "ember_lily": "15,000,000$",
    "sugar_apple": "25,000,000$",
    "burning_bud": "40,000,000$",
    "giant_pinecone": "55,000,000$",
    "elder_strawberry": "70,000,000$",
    "romanesco": "88,000,000$",
    "watering_can": "50,000$",
    "trowel": "100,000$",
    "trading_ticket": "100,000$",
    "recall_wrench": "150,000$",
    "basic_sprinkler": "25,000$",
    "advanced_sprinkler": "50,000$",
    "medium_treat": "4,000,000$",
    "medium_treattoy": "4,000,000$",
    "godly_sprinkler": "120,000$",
    "magnifying_glass": "10,000,000$",
    "master_sprinkler": "10,000,000$",
    "cleaning_spray": "15,000,000$",
    "favorite_tool": "20,000,000$",
    "harvest_tool": "30,000,000$",
    "friendship_pot": "15,000,000$",
    "level_up_lollipop": "10,000,000,000$",
    "grandmaster_sprinkler": "1,000,000,000$",
    "cleansing_pet_shard": "30,000,000$",

}         

# Все доступные для отслеживания предметы
ALL_TRACKABLE_ITEMS = {
    "carrot": "🥕Carrot",
    "strawberry": "🍓Strawberry",
    "orange_tulip": "🌷Orange tulip",
    "blueberry": "🫐Blueberry",
    "tomato": "🍅Tomato",
    "corn": "🌽Corn",
    "daffodil": "🏵️Daffodil",
    "watermelon": "🍉Watermelon",
    "pumpkin": "🎃Pumpkin",
    "apple": "🍎Apple",
    "bamboo": "🎋Bamboo",
    "coconut": "🥥Coconut",
    "cactus": "🌵Cactus",
    "dragon_fruit": "🐉Dragon fruit",
    "mango": "🥭Mango",
    "grape": "🍇Grape",
    "mushroom": "🍄Mushroom",
    "pepper": "🌶️Pepper",
    "cacao": "🍫Cacao",
    "beanstalk": "🫛Beanstalk",
    "ember_lily": "🔥Ember lily",
    "sugar_apple": "🍏Sugar apple",
    "burning_bud": "🌸Burning bud",
    "giant_pinecone": "🥔Giant pinecone",
    "romanesco": "🥬Romanesco",
    "elder_strawberry": "🔴🍓Elder strawberry",
    "watering_can": "🚿Watering Can",
    "trowel": "🥄Trowel",
    "trading_ticket": "🎟️Trading Ticket",
    "recall_wrench": "🔧Recall Wrench",
    "basic_sprinkler": "🔵Basic Sprinkler",
    "advanced_sprinkler": "🟡Advanced Sprinkler",
    "medium_treat": "🦴Medium Treat",
    "medium_treattoy": "🪀Medium Toy",
    "godly_sprinkler": "🔱Godly Sprinkler",
    "magnifying_glass": "🔍Magnifying Glass",
    "master_sprinkler": "♨️Master Sprinkler",
    "cleaning_spray": "🧽Cleaning Spray",
    "favorite_tool": "💖Favorite Tool",
    "harvest_tool": "🌱Harvest Tool",
    "friendship_pot": "🪴Friendship Pot",
    "level_up_lollipop": "🍭Level Up Lollipop",
    "grandmaster_sprinkler": "🔴Grandmaster Sprinkler",
    "cleansing_pet_shard": "🪟Cleanin Pet Shard",




}    



def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="🔄 Показать сток"), KeyboardButton(text="⚙️ Настройки автостока")],
        [KeyboardButton(text="👀 Отслеживаемые предметы"), KeyboardButton(text="🛠️API")],
        [KeyboardButton(text="🤖О боте")]
        
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Обработка нажатий на кнопки
@dp.message(lambda message: message.text in ["🔄 Показать сток","👀 Отслеживаемые предметы", "⚙️ Настройки автостока", "🛠️API", "🤖О боте"])
async def handle_button_clicks(message: types.Message):
    if message.text == "🔄 Показать сток":
        await command_send(message)
    elif message.text == "👀 Отслеживаемые предметы":
        await command_track(message)
    elif message.text == "⚙️ Настройки автостока":
        await command_settings(message)
    elif message.text == "🛠️API":
        await command_creator(message)
    elif message.text == "🤖О боте":
        await command_help(message)


       
# Функции для работы с настройками пользователей
def load_user_settings():
    """Загружает настройки пользователей из файла"""
    try:
        if os.path.exists(USER_SETTINGS_FILE):
            with open(USER_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Ошибка загрузки настроек пользователей: {e}")
        return {}

def save_user_settings(settings):
    """Сохраняет настройки пользователей в файл"""
    try:
        with open(USER_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения настроек пользователей: {e}")

def get_user_tracked_items(chat_id):
    """Получает список отслеживаемых предметов для пользователя"""
    settings = load_user_settings()
    if str(chat_id) in settings:
        return settings[str(chat_id)].get('tracked_items', [])
    return []

def set_user_tracked_items(chat_id, items):
    """Устанавливает отслеживаемые предметы для пользователя"""
    settings = load_user_settings()
    if str(chat_id) not in settings:
        settings[str(chat_id)] = {}
    settings[str(chat_id)]['tracked_items'] = items
    save_user_settings(settings)

def format_time(date_str, hours_to_add=3):
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    dt += timedelta(hours=hours_to_add)
    return dt.strftime("%H:%M")


async def get_current_stock():
    async with aiohttp.ClientSession() as session:
        async with session.get(api, headers=headers) as response:
            data = await response.json()
            return data.get("seed_stock", []) + data.get("gear_stock", []) + data.get("egg_stock", [])
            print (get_current_stock)

async def get_current_stock2():
    async with aiohttp.ClientSession() as session:
        async with session.get(api, headers=headers) as response:
            data = await response.json()
            return {
                "seed_stock": data.get("seed_stock", []),
                "gear_stock": data.get("gear_stock", []),
                "egg_stock": data.get("egg_stock", [])
            }


async def check_user_tracked_items(stock, chat_id):
    """Проверяет отслеживаемые предметы для конкретного пользователя"""
    user_items = get_user_tracked_items(chat_id)
    found_items = []
    
    for item in stock:
        if item["item_id"] in user_items:
            time_str = format_time(item["Date_End"])
            pricet = PRICE.get(item['item_id'])
            emoji = EMOJI_MAP.get(item['item_id'])     
            sed = f"{ALL_TRACKABLE_ITEMS.get(item['item_id'])}: {item['quantity']}x, Цена: {pricet}\n"
            found_items.append(sed)
    return found_items

@dp.message(CommandStart())
async def command_send(message: Message) -> None:
    stock = await get_current_stock2()
    sub = load_bans()
    chat_id = message.chat.id
    add_subscriber(message.chat.id)
    all_items = []
    all_items2 = []
    all_items3 = []

    for item in stock["gear_stock"]:
        time_str = format_time(item["Date_End"])
        pricet = PRICE.get(item['item_id'])
        emoji = EMOJI_MAP.get(item['item_id'])        
        sed = f"{ALL_TRACKABLE_ITEMS.get(item['item_id'])}: {item['quantity']}x, Цена: {pricet}\n"
        all_items.append(sed)

    for item in stock["seed_stock"]:
        time_str = format_time(item["Date_End"])
        pricet = PRICE.get(item['item_id'])
        emoji = EMOJI_MAP.get(item['item_id'])        
        sed = f"{ALL_TRACKABLE_ITEMS.get(item['item_id'])}: {item['quantity']}x, Цена: {pricet}\n"
        all_items2.append(sed)
    
    for item in stock["egg_stock"]:
        time_str = format_time(item["Date_End"])
        pricet = PRICE.get(item['item_id'])
        emoji = EMOJI_MAP.get(item['item_id'])        
        sed = f"{ALL_TRACKABLE_ITEMS.get(item['item_id'])}: {item['quantity']}x, Цена: {pricet}\n"
        all_items3.append(sed)
    result_message = "\n".join(all_items2) +"\n<b>━━━🔧GEARS━━━</b>\n\n"+"\n".join(all_items)
    
    if chat_id in sub:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        await message.answer(f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>.", parse_mode = "HTML")
        
    else:
        await message.answer(
        f"<b>🌱Сток сейчас</b>:\n\n<b>━━━🪴SEEDS━━━</b>\n\n{result_message}\n<b>Следующее обновление магазина</b> {time_str} по <b>мск</b>\n<b>Чтобы настроить автосток /settings</b>",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
        )
#1912008185
#    "tracked_items":   
#    "sugar_apple",
#      "giant_pinecone",
#      "elder_strawberry",
#      "ember_lily",
#      "burning_bud",
#      "romanesco"
@dp.message(Command("ban"))
async def command_ban(message: types.Message):
    chat_id = int(message.chat.id)
    print (chat_id, ADMIN)
    if chat_id in ADMIN:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        if text:
            add_bans(int(text))
            await bot.send_message(chat_id=text, text=texts, parse_mode="HTML")
        else:
            await message.answer(f"Ошибка", parse_mode="HTML")
    else:
        await message.answer(f"У вас нет прав", parse_mode="HTML")

@dp.message(Command("unban"))
async def command_unban(message: types.Message):
    chat_id = int(message.chat.id)
    if chat_id in ADMIN:
        text = message.text.replace('/unban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"✅<b>Вы были разблокированы!!!</b>"
        if text:
            remove_bans(int(text))
            await bot.send_message(chat_id=text, text=texts, parse_mode="HTML")
        else:
            await message.answer(f"Ошибка", parse_mode="HTML")
    else:
        await message.answer(f"У вас нет прав", parse_mode="HTML")

@dp.message(Command("help"))
async def command_help(message: types.Message):
    sub = load_bans()
    chat_id = message.chat.id
    if chat_id in sub:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        await message.answer(f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>.", parse_mode = "HTML")
        
    else:
        await message.answer(f"<b>Функции:</b>\nПоказывает сток\nОтправляет уведомления о отслеживаемых ростках\n\nОсновные команды:\n /start - Показывает текущий сток\n /settings - Настройка отслеживания предметов\n /track - Показывает текущие предметы которые отслеживаются\n /creator - база данных(api)", parse_mode="HTML")


@dp.message(Command("track"))
async def command_track(message: types.Message):
    sub = load_bans()
    chat_id = message.chat.id
    user_items = get_user_tracked_items(message.chat.id)
    if not user_items:
        await message.answer("❌ Вы еще не выбрали предметы для отслеживания. Используйте /settings чтобы настроить отслеживание.", parse_mode="HTML" )
        return
    
    tracked_names = []
    for item_id in user_items:
        if item_id in ALL_TRACKABLE_ITEMS:
            tracked_names.append(ALL_TRACKABLE_ITEMS[item_id])
    
            formatted_names = "\n".join(tracked_names)
            tracked_names = [ALL_TRACKABLE_ITEMS[item_id] for item_id in user_items if item_id in ALL_TRACKABLE_ITEMS]
        
            text = f"<b>Сейчас отслеживаются</b>:\n\n" + "\n\n".join([f"<b>{name}</b>" for name in tracked_names])
    if chat_id in sub:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        await message.answer(f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>.", parse_mode = "HTML")
        
    else:   
        await message.answer(f"{text}\n\n <b>Настроить отслеживание /settings</b> " , parse_mode="HTML")

@dp.message(Command("settings"))
async def command_settings(message: types.Message):
    sub = load_bans()
    chat_id = message.chat.id
    """Меню настроек отслеживания"""
    buttons = [
        [InlineKeyboardButton(text="📋 Выбрать предметы", callback_data="select_items")],
        [InlineKeyboardButton(text="👀 Показать мои предметы", callback_data="show_my_items")],
        [InlineKeyboardButton(text="❌ Очистить все", callback_data="clear_all")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    if chat_id in sub:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        await message.answer(f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>.", parse_mode = "HTML")
        
    else:    
        await message.answer(
            "⚙️ <b>Настройки отслеживания</b>\n\n"
            "Здесь вы можете выбрать какие предметы хотите отслеживать",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

@dp.callback_query(lambda c: c.data == "select_items")
async def select_items_callback(callback_query: CallbackQuery):
    """Показывает список всех предметов для выбора"""
    user_items = get_user_tracked_items(callback_query.from_user.id)
    
    buttons = []
    buttons.append([InlineKeyboardButton(
    text="🌱Seeds",
    callback_data="dummy"
    )])
    row = []
    
    # Создаем все обычные кнопки
    for i, (item_id, item_name) in enumerate(ALL_TRACKABLE_ITEMS.items()):
        is_selected = "✅ " if item_id in user_items else "❌ "
        row.append(InlineKeyboardButton(
            text=f"{is_selected}{item_name}",
            callback_data=f"toggle_{item_id}"
        ))
        
        # Добавляем новую строку после каждых 2 кнопок
        if (i + 1) % 2 == 0 or i == len(ALL_TRACKABLE_ITEMS) - 1:
            buttons.append(row)
            row = []
    
    # Вставляем специальную кнопку посередине
    buttons.insert(14, [
    InlineKeyboardButton(
        text="⚙Gears",
        callback_data="dummy"
    )
])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(
        "📋 <b>Выберите предметы для отслеживания:</b>\n\n"
        "Нажмите на предмет чтобы добавить/убрать его из отслеживания",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback_query.answer()
@dp.callback_query(lambda c: c.data.startswith("toggle_"))
async def toggle_item_callback(callback_query: CallbackQuery):
    """Переключает состояние отслеживания предмета"""
    item_id = callback_query.data.replace("toggle_", "")
    user_items = get_user_tracked_items(callback_query.from_user.id)
    
    if item_id in user_items:
        user_items.remove(item_id)
    else:
        user_items.append(item_id)
    
    set_user_tracked_items(callback_query.from_user.id, user_items)
    
    # Обновляем сообщение
    buttons = []
    buttons.append([InlineKeyboardButton(
    text="🌱Seeds",
    callback_data="dummy"
    )])
    row = []
    
    for i, (current_item_id, item_name) in enumerate(ALL_TRACKABLE_ITEMS.items()):
        is_selected = "✅ " if current_item_id in user_items else "❌ "
        row.append(InlineKeyboardButton(
            text=f"{is_selected}{item_name}",
            callback_data=f"toggle_{current_item_id}"
        ))
        
        # Добавляем новую строку после каждых 2 кнопок
        if (i + 1) % 2 == 0 or i == len(ALL_TRACKABLE_ITEMS) - 1:
            buttons.append(row)
            row = []
    
    # Вставляем специальную кнопку посередине
    buttons.insert(14, [
    InlineKeyboardButton(
        text="⚙Gears",
        callback_data="dummy"
    )
])
    
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer(f"Предмет обновлен!")

@dp.callback_query(lambda c: c.data == "show_my_items")
async def show_my_items_callback(callback_query: CallbackQuery):
    """Показывает текущие отслеживаемые предметы"""
    user_items = get_user_tracked_items(callback_query.from_user.id)
    
    if not user_items:
        text = "❌ Вы еще не выбрали предметы для отслеживания."
    else:
        tracked_names = [ALL_TRACKABLE_ITEMS[item_id] for item_id in user_items if item_id in ALL_TRACKABLE_ITEMS]
        
        text = f"<b>Сейчас отслеживаются</b>:\n\n" + "\n\n".join([f"<b>{name}</b>" for name in tracked_names])

    buttons = [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "clear_all")
async def clear_all_callback(callback_query: CallbackQuery):
    """Очищает все отслеживаемые предметы"""
    set_user_tracked_items(callback_query.from_user.id, [])
    
    buttons = [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(
        "✅ Все предметы удалены из списка отслеживания.",
        reply_markup=keyboard
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "back_to_settings")
async def back_to_settings_callback(callback_query: CallbackQuery):
    """Возврат в главное меню настроек"""
    buttons = [
        [InlineKeyboardButton(text="📋 Выбрать предметы", callback_data="select_items")],
        [InlineKeyboardButton(text="👀 Показать мои предметы", callback_data="show_my_items")],
        [InlineKeyboardButton(text="❌ Очистить все", callback_data="clear_all")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(
        "⚙️ <b>Настройки отслеживания</b>\n\n"
        "Здесь вы можете выбрать какие предметы хотите отслеживать",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback_query.answer()

@dp.message(Command("creator"))
async def command_creator(message: types.Message):
    sub = load_bans()
    chat_id = message.chat.id
    if chat_id in sub:
        text = message.text.replace('/ban', '').strip()
        link = '<a href="https://telegram.org/privacy-tpa">политики конфиденциальности</a>'
        texts = f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>."
        await message.answer(f"❌<b>Вы были заблокированы за нарушение {link}\n\nПо поводу разблокировки писать @Minekit</b>.", parse_mode = "HTML")
        
    else:   
        await message.answer("<b>api</b>: api.joshlei.com\n\n<b>api discord</b>: discord.gg/growagardenapi", parse_mode="HTML")



async def notify_subscribers():
    """Отправляет персонализированные уведомления всем подписчикам"""
    stock = await get_current_stock()
    subscribers = load_subscribers()
    sub = load_bans()
    if subscribers not in sub:
        for chat_id in subscribers:
            try:
                user_tracked_items = await check_user_tracked_items(stock, chat_id)
            
                if user_tracked_items:
                    result_message = "\n".join(user_tracked_items)
                    time_str = format_time(stock[0]["Date_End"]) if stock else "N/A"
                
                    message_text = (
                        f"🔄 <b>Найдены ваши отслеживаемые предметы</b>\n\n"
                        f"{result_message}\n\n"
                        f"<b>Следующее обновление магазина</b> {time_str} по <b>мск</b>\n"
                        f"<b>Управление отслеживанием</b>: /settings"
                    )
                
                    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode="HTML")
                
            except Exception as e:
                print(f"Не удалось отправить сообщение {chat_id}: {e}")
                remove_subscriber(chat_id)

async def check_time_and_notify():
    stock = await get_current_stock2()
    last_notification_minute = -1
    sub = load_bans()
    subscribers = load_subscribers()
    if subscribers not in sub:
        while True:
            now = datetime.now()
            if now.minute % 5 == 0 and now.second == 20 and now.minute != last_notification_minute:
                await notify_subscribers()
                last_notification_minute = now.minute
                await asyncio.sleep(40)
            else:
                await asyncio.sleep(1)

async def check_time_and_notifyEG():
    last_notification_minute = -1
    sub = load_bans()
    subscribers = load_subscribers()
    if subscribers not in sub:
        while True:
            now = datetime.now()
            if now.minute % 30 == 0 and now.second == 15 and now.minute != last_notification_minute:
                await notify_subscribers()
                last_notification_minute = now.minute
                await asyncio.sleep(45)
            else:
                await asyncio.sleep(1)



async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        check_time_and_notify()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("BOT POWER IS OFF")

#Hello world ))