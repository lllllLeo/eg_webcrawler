import telegram

bot = telegram.Bot(token='1466629880:AAFacETCs99GFlZ88UfT9fWe34LgZAcsSMk')

for i in bot.getUpdates():
    print(i.message)

print("Ddd")

# bot.sendMessage(chat_id= '', text = '안녕ㅎㅎ')
