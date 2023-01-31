from config import bot
import config
from time import sleep
import re
import database.db as db
import logic

from telebot import types
from time import sleep


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)


@bot.message_handler(commands=['register'])
def on_command_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/register_owner')
    itembtn2 = types.KeyboardButton('/register_mechanic')
    markup.add(itembtn1, itembtn2)
    bot.send_message(
        message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)


# coger id del mensaje y buscar en la table del tipo ingresado, si no existe, el usuario no esta registrado
@bot.message_handler(regexp=r"^(start|str) (owner|mechanic)")
def on_command_start(message):

    types = {
        "owner": logic.find_owner,
        "mechanic": logic.find_mechanic
    }

    parts = re.match(
        r"^^(start|str) (owner|mechanic))",
        message.text,
        flags=re.IGNORECASE)

    oper1 = float(parts[1])
    oper2 = float(parts[3])

    types[oper2](message.chat.id)



@bot.message_handler(commands=['register_mechanic'])
def on_command_imc(message):
    response = bot.reply_to(message, "ingrese el telefono")
    bot.register_next_step_handler(response, save_mechanic)


def save_mechanic(message):
    try:
        print(message)
        mechanic = int(message.text)
        logic.register_mechanic(message.chat.id, mechanic)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


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


@bot.message_handler(regexp=r"^(register owner|ro) ([a-z0-9])")
def on_add(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)

    parts = re.match(
        r"^(register owner | ro) ([a-z0-9]+[@]\w+[.]\w{2,3}$)",
        message.text,
        flags=re.IGNORECASE)

    print(parts.groups())

    oper1 = float(parts[1])
    oper2 = float(parts[3])

    result = oper1 + oper2

    bot.reply_to(
        message,
        "Prueba"
    )

# 3


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
