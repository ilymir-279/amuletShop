import telebot
from telebot import types
from datetime import date

token="7747531890:AAFDSlj0_dra8nZQBj_n9vpyUtDBNMEn4HI"
bot = telebot.TeleBot(token)

TO_CHAT_ID = "7532173117"


start_id = 1
sup = 0
pay = 0
reply_sup = 0
product = ""
cost = 0
description = ""
history_list = ["Здесь ничего нет 😢", "", ""]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sub = types.KeyboardButton("✅ Я подписан")
    markup.add(sub)

    bot.send_message(message.chat.id, text='''*Привет👋 {0.first_name}! \n\nДобро пожаловать в магазин Amulett Shop! Для использования бота необходимо подписаться на новостной канал магазина \n\nНаш канал 👉 @amulettshop *
    '''.format(message.from_user), reply_markup=markup, parse_mode="Markdown")


@bot.message_handler(func= lambda message: message.text ==  "✅ Я подписан")
def chack_channels(message):
    sup=0
    pay=0
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
  global start_id, complaint_chat_id
  complaint_chat_id = call.message.chat.id

  i=0
  menu(call)
  bot.delete_message(call.message.chat.id, start_id+2)
  while call.message.message_id != start_id:
    i+=1
    call.message.message_id -= i
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def menu(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=2)

  catalog = types.InlineKeyboardButton(text="Каталог 🛒", callback_data="catalog")
  profile = types.InlineKeyboardButton(text="Профиль 🎮", callback_data="profile")
  support = types.InlineKeyboardButton(text="Поддержка 👨‍💻 ", callback_data="support")
  garanties = types.InlineKeyboardButton(text="Гарантии 📄", callback_data="garanties", url='https://telegra.ph/Garantii-AML-Shop-03-06')
  reviews = types.InlineKeyboardButton(text="Отзывы 🌟", callback_data="reviews", url='t.me/+xx83SO52oclhYWEy')

  keyboard.add(catalog, profile, support, garanties, reviews)
  main_menu_img = open('img/main_menu.jpg', 'rb')
  bot.send_photo(call.message.chat.id, main_menu_img, reply_markup=keyboard)

@bot.message_handler(content_types=['photo', 'text', "video"])
def forward_mes(message):
  global sup, pay, reply_sup, complaint_chat_id

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  reply = types.InlineKeyboardButton(text="Ответить", callback_data="reply")
  if sup==1:
    keyboard.add(back)
    bot.send_message(complaint_chat_id, text='Ваша жалоба успешно отправлена. Мы обязательно рассмотрим ее и свяжемся с вами в ближайшее время!',reply_markup=keyboard)
    keyboard.add(reply)
    if message.content_type=="photo":
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_photo(TO_CHAT_ID, downloaded_file, caption=message.caption, reply_markup=keyboard)
    if message.content_type=="video":
        video = message.video
        file_id = video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_video(TO_CHAT_ID, downloaded_file, caption=message.caption, reply_markup=keyboard)
    elif message.content_type=="text":
      text_mes = message.text
      bot.send_message(TO_CHAT_ID, text=text_mes, reply_markup = keyboard)

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

    reply_sup = 1
    sup=0
  elif pay == 1:
    if message.content_type=="photo":
      confirm = types.InlineKeyboardButton(text="Принять оплату", callback_data="confirm")
      reject = types.InlineKeyboardButton(text="Отклонить", callback_data="reject")
      keyboard.add(back)

      bot.send_message(message.chat.id, text='Ваша оплата успешно отправлена. Мы обязательно рассмотрим ее и свяжемся с вами в ближайшее время!',reply_markup=keyboard)

      keyboard.add(confirm, reject)
      bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
      bot.send_message(TO_CHAT_ID, text = product, reply_markup=keyboard)

      bot.delete_message(message.chat.id, message.message_id - 1)
      bot.delete_message(message.chat.id, message.message_id)

      pay=0
    else:
      bot.delete_message(message.chat.id, message.message_id-1)
      keyboard.add(back)
      bot.send_message(message.chat.id, text='Похоже, что вы отправили текст или видео. Отправьте фотографию чека вместе с прикреплённым @username для подтверждения оплаты!',reply_markup=keyboard)

  elif reply_sup == 1:
    reply_sup_user = types.InlineKeyboardButton(text="Ответить", callback_data="reply_sup_user")
    keyboard.add(reply_sup_user, back)
    if message.content_type=="photo":
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_photo(complaint_chat_id, downloaded_file, caption="🧑‍💻 Модератор Дмитрий:\n\n"+message.caption, reply_markup=keyboard)
    elif message.content_type=="video":
        video = message.video
        file_id = video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_video(complaint_chat_id, downloaded_file, caption="🧑‍💻 Модератор Дмитрий:\n\n"+message.caption, reply_markup=keyboard)
    elif message.content_type=="text":
        text_mes = message.text
        bot.send_message(complaint_chat_id, text="🧑‍💻 Модератор Дмитрий:\n\n"+text_mes, reply_markup = keyboard)

    bot.send_message(message.chat.id, text='Сообщение доставлено')
    reply_sup = 0

@bot.callback_query_handler(func=lambda call: call.data == "reply_sup")
def reply_sup(call):
  global reply_sup
  reply_sup = 1

@bot.callback_query_handler(func=lambda call: call.data == "reply_sup_user")
def reply_sup(call):
  support(call)

@bot.callback_query_handler(func=lambda call: call.data == "catalog")
def callback_copy_text(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)

  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  fortnite = types.InlineKeyboardButton(text="Fortnite 🎮", callback_data="fortnite")

  keyboard.add(fortnite, back)
  catalog_img = open('img/catalog.jpg', 'rb')
  bot.send_photo(call.message.chat.id, catalog_img, caption='Выберите игру', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "support")
def support(call):
  global sup, start_id
  start_id = call.message.id
  sup = 1
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  keyboard.add(back)
  support_img = open('img/support.jpg', 'rb')
  bot.send_photo(call.message.chat.id, support_img, caption='Здравствуйте! \n\nПожалуйста, подробно опишите вашу проблему. Это поможет нам быстрее и точнее решить ваш вопрос. Также укажите ваш @username для связи с вами. После этого ожидайте ответ со стороны поддержки.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  history = types.InlineKeyboardButton(text="История заказов", callback_data="history")
  back = types.InlineKeyboardButton(text="Назад", callback_data="back_to_menu")
  keyboard.add(history, back)

  catalog_img = open('img/profile.jpg', 'rb')
  bot.send_photo(call.message.chat.id, catalog_img, caption='\n🎮 Профильㅤㅤㅤㅤㅤㅤㅤ\n\n👤 Имя: '+ str(call.from_user.first_name) +'\n\n🔑 id: '+ str(call.message.chat.id)+"\n", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "history")
def history(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="profile")
  keyboard.add(back)

  history_img = open('img/history.jpg', 'rb')
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

  fortnite_img = open('img/fortnite.jpg', 'rb')
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

  v_bucks_img = open('img/v_backs.jpg', 'rb')
  bot.send_photo(call.message.chat.id,v_bucks_img,caption="Категория: В-Баксы \n\n⚠️ Перед покупкой В-Баксов ознакомьтесь! https://telegra.ph/Pokupka-03-07", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks10")
def v_bucks10(call):
  global product, cost, description
  product = " 1000 v-bucks"
  cost = 749
  description = "После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games."

  prepayment(call)


@bot.callback_query_handler(func=lambda call: call.data == "v_bucks28")
def v_bucks28(call):
  global product, cost, description
  product = " 2800 v-bucks"
  cost = 1499
  description = "После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks50")
def v_bucks50(call):
  global product, cost, description
  product = " 5000 v-bucks"
  cost = 2499
  description = "После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks13")
def v_bucks13(call):
  global product, cost, description
  product = " 13500 v-bucks"
  cost = 5699
  description = "После оплаты вам необходимо сообщить данные от вашей учетной записи Epic Games."

  prepayment(call)


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
  v_bucks28_gift = types.InlineKeyboardButton(text="2800 vb ", callback_data="v_bucks28_gift")
  v_bucks35_gift = types.InlineKeyboardButton(text="3500 vb", callback_data="v_bucks35_gift")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(v_bucks6_gift, v_bucks8_gift, v_bucks10_gift, v_bucks12_gift, v_bucks15_gift, v_bucks18_gift, v_bucks20_gift, v_bucks22_gift, v_bucks24_gift, v_bucks26_gift, v_bucks28_gift, v_bucks35_gift, back)

  gift_img = open('img/gift.jpg', 'rb')
  bot.send_photo(call.message.chat.id, gift_img,caption='''🗒️Категория: Подарки

🎁 Наши подарочные аккаунты (ДОБАВЛЯТЬ ВСЕ) иначе не сможем подарить вам предмет! 🎁

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
  global product, cost, description
  product = " v_bucks 600 gift"
  cost = 279
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks8_gift")
def v_bucks8_gift(call):
  global product, cost, description
  product = " v_bucks 800 gift"
  cost = 349
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks10_gift")
def v_bucks10_gift(call):
  global product, cost, description
  product = " v_bucks 1000 gift"
  cost = 429
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks12_gift")
def v_bucks12_gift(call):
  global product, cost, description
  product = " v_bucks 1200 gift"
  cost = 499
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks15_gift")
def v_bucks15_gift(call):
  global product, cost, description
  product = " v_bucks 1500 gift"
  cost = 569
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks18_gift")
def v_bucks18_gift(call):
  global product, cost, description
  product = " v_bucks 1800 gift"
  cost = 649
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks20_gift")
def v_bucks20_gift(call):
  global product, cost, description
  product = " v_bucks 2000 gift"
  cost = 729
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks22_gift")
def v_bucks22_gift(call):
  global product, cost, description
  product = " v_bucks 2200 gift"
  cost = 799
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks24_gift")
def v_bucks24_gift(call):
  global product, cost, description
  product = " v_bucks 2400 gift"
  cost = 869
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks26_gift")
def v_bucks26_gift(call):
  global product, cost, description
  product = " v_bucks 2400 gift"
  cost = 929
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks28_gift")
def v_bucks28_gift(call):
  global product, cost, description
  product = " v_bucks 2800 gift"
  cost = 919
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "v_bucks35_gift")
def v_bucks35_gift(call):
  global product, cost, description
  product = " v_bucks 3500 gift"
  cost = 1119
  description = "После оплаты вам необходимо добавить все аккануты в друзья."

  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "band")
def band(call):
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  band2 = types.InlineKeyboardButton(text="Купить", callback_data="band2")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(band2, back)
  band_img = open('img/band.jpg', 'rb')
  bot.send_photo(call.message.chat.id, band_img,caption='''
🗒️Категория: Отряд

📌 Описание: Подписка активна в течение 30 дней с момента оформления заказа и не подлежит автопродлению. Перед покупкой Отряда в Fortnite убедитесь, что у вас нет действующей подписки. В противном случае вы можете столкнуться с ошибками в игре, и предметы из отряда не будут доступны!
  ''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "band2")
def band2(call):
  global product, cost, description
  product = "отряд"
  cost = 599
  description = ""
  prepayment(call)

@bot.callback_query_handler(func=lambda call: call.data == "prepayment")
def prepayment(call):
  global product, description, cost
  bot.delete_message(call.message.chat.id, call.message.message_id)
  keyboard = types.InlineKeyboardMarkup(row_width=1)
  payment = types.InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment")
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(payment, back)

  bot.send_message(call.message.chat.id, text=f'''
🎮 {product}

💸 Цена: {cost}₽

📌 Описание: {description}

Оплата происходит на карту: 2202208166272568
Внимание, отправляйте ровно ту сумму, которая указана в боте!

После завершения платежа, пожалуйста, нажмите кнопку «Я оплатил» и отправьте скриншот с чеком оплаты и укажите ваш @username для получения товара.''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "payment")
def payment(call):
  global pay
  pay = 1
  bot.delete_message(call.message.chat.id, call.message.message_id)

  keyboard = types.InlineKeyboardMarkup(row_width=1)
  back = types.InlineKeyboardButton(text="Назад", callback_data="fortnite")
  keyboard.add(back)
  bot.send_message(call.message.chat.id, text='Отправьте скриншот оплаты и с вами свяжутся в скором времени, а также напишите ваш @username вместе с чеком одним сообщением. За статусом платежа можете наблюдать в истории заказов.', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "confirm")
def confirm(call):
  global history_list, product, cost

  today = date.today()
  history_list.append((str(today)+" "+product+ " " +str(cost)+" "+"оплата принята"))

@bot.callback_query_handler(func=lambda call: call.data == "reject")
def reject(call):
  global history_list, product, cost

  today = date.today()
  history_list.append((str(today)+" "+product+ " " +str(cost)+" "+"оплата отклонена"))

bot.polling(non_stop=True)
