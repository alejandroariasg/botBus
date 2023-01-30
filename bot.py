from config import bot
import config
from time import sleep
import re
import database.db as db

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)



@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = (
        "Hola, soy un \U0001F916, de la empresa BotBus \U0001F68D \U0001F699 \n"
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*registraru {valor1} y {valor2}* - Registrar un nuevo usuario\n"
        "*regitrarv {valor1} y {valor2}* - Registrar vehiculo\n"
        "*registrarm {valor1} y {valor2}* - Registrar mantenimiento\n"
        "*consultamatenimientos {valor1} y {valor2}* - Consultar los mantenimientos realizados\n"
    )
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*registraru {valor1} y {valor2}* - Registrar un nuevo usuario\n"
        "*regitrarv {valor1} y {valor2}* - Registrar vehiculo\n"
        "*registrarm {valor1} y {valor2}* - Registrar mantenimiento\n"
        "*consultamatenimientos {valor1} y {valor2}* - Consultar los mantenimientos realizados\n"
    )
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="Markdown"
    ) 

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")

#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################