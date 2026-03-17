import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

TOKEN = os.getenv('TOKEN')
MY_CHAT_ID = os.getenv('MY_CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app)  # Разрешаем сайту отправлять запросы на этот сервер

@app.route('/send_order', methods=['POST'])
def handle_order():
    try:
        data = request.json
        
        service = data.get('service')
        street = data.get('street')
        apartment = data.get('apartment')
        extra = data.get('extra')
        shop_list = data.get('shopList')

        # Формируем красивое сообщение для тебя
        msg = (
            f"🔔 **НОВЫЙ ЗАКАЗ!**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🛠 **Услуга:** {service}\n"
            f"📍 **Адрес:** ул. {street}, кв. {apartment}\n"
            f"💬 **Доп. инфо:** {extra if extra else 'не указано'}\n"
        )
        
        if service == 'Сходить в магазин' and shop_list:
            msg += f"🛒 **Список покупок:**\n{shop_list}\n"
        
        msg += f"━━━━━━━━━━━━━━━"

        # Отправка сообщения в твой Telegram
        bot.send_message(MY_CHAT_ID, msg, parse_mode="Markdown")
        
        return jsonify({"status": "success", "message": "Заказ отправлен!"}), 200
    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print(f"Сервер запущен! Бот готов принимать заказы.")
    # Запуск на порту 5000
    app.run(host='0.0.0.0', port=5000)
