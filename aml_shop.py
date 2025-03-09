import telebot
from telebot import types
from datetime import date

token="7757986535:AAGQ-ws4586vY-1A3d_9AdNm_sQb3T_kNNc"
bot = telebot.TeleBot(token)

TO_CHAT_ID = "7532173117"

start_id = 1
sup = 0
pay = 0
product = ""
history_list = ["Здесь ничего нет 😢", "", ""]


@bot.message_handler(commands=['start'])
def start(message):
    global start_id
    start_id = message.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sub = types.KeyboardButton("✅ Я подписан")
    markup.add(sub)

    bot.send_message(message.chat.id, text='''*Привет👋 {0.first_name}! \n\nДобро пожаловать в магазин Amulett Shop! Для использования бота необходимо подписаться на новостной канал магазина \n\nНаш канал 👉 @amulettshop *
    '''.format(message.from_user), reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func= lambda message: message.text ==  "✅ Я подписан")
def chack_channels(message):
    sup=0
    user_id = message.from_user.id
    channel_id = "@amulettshop"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back_to_menu = types.InlineKeyboardButton(text="📥 Главное меню", callback_data="f_back_to_menu")
    keyboard.add(back_to_menu)

    try:
        chat_member = bot.get_chat_member(channel_id, user_id)

        if chat_member.status != 'left':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAE7KLBnyugMY9GCOmY2vT_7Qx8m_yDOFQACfAEAAhZCawrtoK_LB7yPEzYE' , reply_markup=types.ReplyKeyboardRemove())
            bot.reply_to(message, "Спасибо за подписку!", reply_markup=keyboard)


        else:
            bot.reply_to(message, "Вы не подписаны на канал. Пожалуйста, подпишитесь, чтобы продолжить.")
    except Exception as e:

        bot.reply_to(message, "Произошла ошибка при проверке подписки на канал.")

@bot.callback_query_handler(func=lambda call: call.data == "f_back_to_menu")
def f_back_to_menu(call):
  global start_id
  i=0
  menu(call)
  bot.delete_message(call.message.chat.id, start_id+2)
  while call.message.message_id != start_id:
    i+=1
    call.message.message_id -= i
    print(start_id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def menu(call):
  global sup, pay
  sup=0
  pay=0

  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=2)

  catalog = types.InlineKeyboardButton(text="Каталог 🛒", callback_data="catalog")
  profile = types.InlineKeyboardButton(text="Профиль 🎮", callback_data="profile")
  support = types.InlineKeyboardButton(text="Поддержка 👨‍💻 ", callback_data="support")
  garanties = types.InlineKeyboardButton(text="Гарантии 📄", callback_data="garanties", url='https://telegra.ph/Garantii-AML-Shop-03-06')
  reviews = types.InlineKeyboardButton(text="Отзывы 🌟", callback_data="reviews", url='t.me/+xx83SO52oclhYWEy')

  keyboard.add(catalog, profile, support, garanties, reviews)

  main_menu_img = open('/content/img/main_menu.jpg', 'rb')
  bot.send_photo(call.message.chat.id, main_menu_img, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "catalog")
def callback_copy_text(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)

  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  fortnite = types.InlineKeyboardButton(text="Fortnite 🎮", callback_data="fortnite")

  keyboard.add(fortnite, back)
  catalog_img = open('/content/img/catalog.jpg', 'rb')
  bot.send_photo(call.message.chat.id, catalog_img, caption='Выберите игру', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "support")
def support(call):
  global sup
  sup = 1
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  keyboard.add(back)
  support_img = open('/content/img/support.jpg', 'rb')
  bot.send_photo(call.message.chat.id, support_img, caption='Здравствуйте! \n\nПожалуйста, подробно опишите вашу проблему. Это поможет нам быстрее и точнее решить ваш вопрос. Также укажите ваш @username для связи с вами. После этого ожидайте ответ со стороны поддержки.', reply_markup=keyboard)


  @bot.message_handler(content_types=['text'])
  def forward_mes(message):
      global sup
      if sup==1:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
        keyboard.add(back)
        bot.send_message(message.chat.id, text='Ваша жалоба успешно отправлена. Мы обязательно рассмотрим ее и свяжемся с вами в ближайшее время!',reply_markup=keyboard)
        bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        sup=0


@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  history = types.InlineKeyboardButton(text="История заказов", callback_data="history")
  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  keyboard.add(history, back)

  catalog_img = open('/content/img/profile.jpg', 'rb')
  bot.send_photo(call.message.chat.id, catalog_img, caption='\n🎮 Профильㅤㅤㅤㅤㅤㅤㅤ\n\n👤 Имя: '+ str(call.from_user.first_name) +'\n\n🔑 id: '+ str(call.message.chat.id)+"\n", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "history")
def history(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="profile")
  keyboard.add(back)

  history_img = open('/content/img/history.jpg', 'rb')
  bot.send_photo(call.message.chat.id, history_img, caption= history_list[-1]+ "\n" + history_list[-2] + "\n" + history_list[-3], reply_markup=keyboard )

@bot.callback_query_handler(func=lambda call: call.data == "fortnite")
def fortnite_list(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  v_bucks = types.InlineKeyboardButton(text="В-баксы на аккаунт 🔥", callback_data="v_bucks")
  gift = types.InlineKeyboardButton(text="Донат подарком 🎁", callback_data="gift")
  band = types.InlineKeyboardButton(text="Отряд 👾", callback_data="band")
  back = types.InlineKeyboardButton(text="Назад", callback_data="catalog")
  keyboard.add(v_bucks, gift, band, back)

  fortnite_img = open('/content/img/fortnite.jpg', 'rb')
  bot.send_photo(call.message.chat.id,fortnite_img,caption="Выберите товар", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks")
def v_bucks(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  v_bucks10 = types.InlineKeyboardButton(text="1000 vb", callback_data="v_bucks10")
  v_bucks28 = types.InlineKeyboardButton(text="2800 vb ", callback_data="v_bucks28")
  v_bucks50 = types.InlineKeyboardButton(text="5000 vb", callback_data="v_bucks50")
  v_bucks13 = types.InlineKeyboardButton(text="13500 vb", callback_data="v_bucks13")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(v_bucks10, v_bucks28, v_bucks50, v_bucks13, back)

  v_bucks_img = open('/content/img/v_backs.jpg', 'rb')
  bot.send_photo(call.message.chat.id,v_bucks_img,caption="Категория: В-Баксы \n\n⚠️ Перед покупкой В-Баксов ознакомьтесь! https://telegra.ph/Pokupka-03-07", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks10")
def v_bucks10(call):
  global product
  product = " 1000 v-bucks"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="v_bucks")
  keyboard.add(payment, back)

  bot.send_message(call.message.chat.id, text='''
🎮 1000 В-баксов

💸 Цена: 749₽

📌 Описание:
После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks28")
def v_bucks28(call):
  global product
  product = " 2800 v-bucks"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="v_bucks")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''
🎮 2800 В-баксов

💸 Цена: 1499₽

📌 Описание:
После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks50")
def v_bucks50(call):
  global product
  product = " 5000 v-bucks"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="v_bucks")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''
🎮 5000 В-баксов

💸 Цена: 2499₽

📌 Описание:
После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks13")
def v_bucks13(call):
  global product
  product = " 13500 v-bucks"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="v_bucks")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''
🎮 13500 В-баксов

💸 Цена: 5699₽

📌 Описание:
После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)




@bot.callback_query_handler(func=lambda call: call.data == "gift")
def gift(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  v_bucks6_gift = types.InlineKeyboardButton(text="600 vb", callback_data="v_bucks6_gift")
  v_bucks8_gift = types.InlineKeyboardButton(text="800 vb", callback_data="v_bucks8_gift")
  v_bucks10_gift = types.InlineKeyboardButton(text="1000 vb", callback_data="v_bucks10_gift")
  v_bucks12_gift = types.InlineKeyboardButton(text="1200 vb", callback_data="v_bucks12_gift")
  v_bucks15_gift = types.InlineKeyboardButton(text="1500 vb ", callback_data="v_bucks15_gift")
  v_bucks18_gift = types.InlineKeyboardButton(text="1800 vb ", callback_data="v_bucks18_gift")
  v_bucks20_gift = types.InlineKeyboardButton(text="2000 vb ", callback_data="v_bucks20_gift")
  v_bucks22_gift = types.InlineKeyboardButton(text="2200 vb ", callback_data="v_bucks22_gift")
  v_bucks24_gift = types.InlineKeyboardButton(text="2400 vb ", callback_data="v_bucks24_gift")
  v_bucks26_gift = types.InlineKeyboardButton(text="2600 vb ", callback_data="v_bucks26_gift")
  v_bucks35_gift = types.InlineKeyboardButton(text="3500 vb", callback_data="v_bucks35_gift")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(v_bucks6_gift, v_bucks8_gift, v_bucks10_gift, v_bucks12_gift, v_bucks15_gift, v_bucks18_gift, v_bucks20_gift, v_bucks22_gift, v_bucks24_gift, v_bucks26_gift, v_bucks35_gift, back)

  gift_img = open('/content/img/gift.jpg', 'rb')
  bot.send_photo(call.message.chat.id, gift_img,caption='''🗒️Категория: Подарки

❗️ДОБАВЛЕНИЕ В ДРУЗЬЯ ОБЯЗАТЕЛЬНО

🎁Наши подарочные аккаунты (ДОБАВЛЯТЬ ВСЕ):

ESQ SHOP80
ESQ SHOP81
ESQ SHOP82
ESQ SHOP83
ESQ SHOP84
ESQ SHOP85
ESQ SHOP86
ESQ SHOP87
ESQ SHOP88
ESQ SHOP89
ESQ SHOP90
ESQ SHOP91
ESQ SHOP92
ESQ SHOP93
ESQ SHOP94
ESQ SHOP95
ESQ SHOP96
ESQ SHOP97
ESQ SHOP98
ESQ SHOP99
ESQ SHOP100

⚠️ Условия Получения Подарков - https://telegra.ph/Podarki-03-07-4''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks6_gift")
def v_bucks6_gift(call):
  global product
  product = " 600 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''
🎮 600 В-баксов подарком

💸 Цена: 249₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks8_gift")
def v_bucks8_gift(call):
  global product
  product = " 800 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 800 В-баксов подарком

💸 Цена: 329₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks10_gift")
def v_bucks10_gift(call):
  global product
  product = " 1000 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''
🎮 1000 В-баксов подарком

💸 Цена: 389₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks12_gift")
def v_bucks12_gift(call):
  global product
  product = " 1200 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 1200 В-баксов подарком

💸 Цена: 479₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks15_gift")
def v_bucks15_gift(call):
  global product
  product = " 1500 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''


🎮 1500 В-баксов подарком

💸 Цена: 529₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks18_gift")
def v_bucks18_gift(call):
  global product
  product = " 1800 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

  🎮 1800 В-баксов подарком

💸 Цена: 599₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks20_gift")
def v_bucks20_gift(call):
  global product
  product = " 2000 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 2000 В-баксов подарком

💸 Цена: 649₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks22_gift")
def v_bucks22_gift(call):
  global product
  product = " 2200 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 2200 В-баксов подарком

💸 Цена: 699₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "v_bucks24_gift")
def v_bucks24_gift(call):
  global product
  product = " 2400 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 2400 В-баксов подарком

💸 Цена: 639₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks26_gift")
def v_bucks26_gift(call):
  global product
  product = " 2600 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''

🎮 2600 В-баксов подарком

💸 Цена: 699₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks35_gift")
def v_bucks35_gift(call):
  global product
  product = " 3500 v-bucks gift"
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="gift")
  keyboard.add(payment, back)
  bot.send_message(call.message.chat.id, text='''


🎮 3500 В-баксов подарком

💸 Цена: 1 449₽

📌 Описание:
После оплаты вам необходимо добавить все аккануты в друзья.

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения В-баксов.''', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "band")
def band(call):
  global product
  product = " band"
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  band = types.InlineKeyboardButton(text="Купить подписку", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(band, back)

  band_img = open('/content/img/band.jpg', 'rb')
  bot.send_photo(call.message.chat.id, band_img,caption=

      '''Товар: Отряд Fortnite

      Цена: 649₽

      Подписка активна в течение 30 дней с момента оформления заказа и не подлежит автопродлению.

      ❗️ ВАЖНО: Перед покупкой Отряда в Fortnite убедитесь, что у вас нет действующей подписки. В противном случае вы можете столкнуться с ошибками в игре, и предметы из отряда не будут доступны.''', reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "payment")
def payment(call):
  global pay
  pay = 1
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(back)
  bot.send_message(call.message.chat.id, text='Отправьте скриншот оплаты и с вами свяжутся в скором времени, а также напишите ваш @username вместе с чеком одним сообщением', reply_markup=keyboard)

  @bot.message_handler(content_types=['photo', 'text'])
  def forward_mes(message):
      global pay, history_list, product
      if pay == 1:
        if message.content_type == 'photo':
        
          keyboard = types.InlineKeyboardMarkup(row_width=1)
          back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
          keyboard.add(back)
          bot.send_message(message.chat.id, text='Ваша оплата успешно отправлена. Мы обязательно рассмотрим ее и свяжемся с вами в ближайшее время!',reply_markup=keyboard)
          bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
          bot.send_message(TO_CHAT_ID, text = product)
          bot.delete_message(message.chat.id, message.message_id - 1)
          bot.delete_message(message.chat.id, message.message_id)

          history_list[0] = ""
          today = date.today()
          history_list.append((str(today)+" "+product))

          pay=0

        else:
          keyboard = types.InlineKeyboardMarkup(row_width=1)
          back = types.InlineKeyboardButton(text="Заново", callback_data="payment")
          keyboard.add(back)
          bot.reply_to(message, "Произошла ошибка, отправьте скриншот вместе c вашим @username",reply_markup=keyboard)
          bot.delete_message(message.chat.id, message.message_id-1)
          bot.delete_message(message.chat.id, message.message_id)


bot.polling(non_stop=True)
