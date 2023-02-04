from config import bot
import config
from time import sleep
import re
import database.db as db
import logic

from telebot import types
from time import sleep
from record import Record
record = Record()

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)


# Auth
def auth_middleware(user_types):
    def wrapper(func):
        def innerr(*args, **kwargs):
            user_id = args[0].chat.id
            ok_login = logic.login_user(user_id)
            if (not ok_login or ok_login not in user_types):
                return bot.send_message(
                    user_id,
                    "No tienes acceso a estos datos o aun no te registras",
                    parse_mode="Markdown")
            return func(*args, **kwargs)
        return innerr
    return wrapper


# Hello handler
@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(0.6)
    response = ()
    is_loged_user = logic.login_user(message.chat.id)
    if (is_loged_user):
        response = (
            "Hola, soy un \U0001F916, de la empresa BotBus \U0001F68D \U0001F699 \n"
            "Bienvenido, eres un {}".format(is_loged_user)
        )
    else:
        response = (
            "Hola, soy un \U0001F916, de la empresa BotBus \U0001F68D \U0001F699 \n"
            "Aun no te has registrado"
            "*/register* - Muestra menu de registro"
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
        "*/register* - Muestra menu de registro"
        "*/register_mechanic {mechanic_phone}* - Registrar un nuevo mecanico\n"
        "*/register_owner {owner_email}* - Registrar un nuevo owner\n"
        "*/register_vehicle {vehicle}* - Registrar un nuevo vehículo\n"

    )
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="Markdown"
    )


# Registrar
@bot.message_handler(commands=['register'])
def on_command_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/register_owner')
    itembtn2 = types.KeyboardButton('/register_mechanic')
    markup.add(itembtn1, itembtn2)
    bot.send_message(
        message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)


# Registrar mecanico
@bot.message_handler(commands=['register_mechanic'])
def on_command_imc(message):
    response = bot.reply_to(message, "ingrese el telefono del mecanico")
    bot.register_next_step_handler(response, save_mechanic)


def save_mechanic(message):
    try:
        print(message)
        mechanic = int(message.text)
        success_transaction = logic.register_mechanic(
            message.chat.id, mechanic)
        if (success_transaction):
            bot.reply_to(message, f"Mecanico agregado exitosamente")
        else:
            bot.reply_to(
                message, f"El mecanico ya ha sido agregado con anterioridad")
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


# Registrar Owner
@bot.message_handler(commands=['register_owner'])
def on_command_imc(message):
    response = bot.reply_to(message, "Ingrese el email del owner")
    bot.register_next_step_handler(response, save_owner)


def save_owner(message):
    try:
        print(message)

        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', message.text):
            owner = (message.text)
            success_transaction = logic.register_owner(
                message.chat.id, owner)
            if (success_transaction):
                bot.reply_to(message, f"Owner agregado exitosamente")
            else:
                bot.reply_to(
                    message, f"El owner ya ha sido agregado con anterioridad")
        else:
            bot.reply_to(
                message, f"El email ingresado no es valido")
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

#Registrar Vehiculo
@bot.message_handler(commands=['register_vehicle'])
def on_command_imc(message):
    response = bot.reply_to(message, "Ingrese la placa del vehiculo")
    bot.register_next_step_handler(response, vehicle_id)

def vehicle_id(message):
    response = bot.reply_to(
        message, "Ingrese el modelo del vehiculo")
    record.vehicle["id"] = message.text
    bot.register_next_step_handler(response, vehicle_model)


def vehicle_model(message):
    response = bot.reply_to(
        message, "Ingrese la marca del vehiculo")
    record.vehicle["model"] = int(message.text)
    bot.register_next_step_handler(response, vehicle_mark)


def vehicle_mark(message):
    response = bot.reply_to(
        message, "Ingrese el ID del owner")
    record.vehicle["mark"] = message.text
    bot.register_next_step_handler(response, vehicle_owner)

def vehicle_owner(message):
    record.vehicle["id_owner"] = int(message.text)
    try:
        transaction = logic.register_vehicle(**record.vehicle)
        bot.reply_to(
            message, transaction)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


# Registrar revision
@bot.message_handler(commands=['register_review'])
@auth_middleware(user_types=['mechanic'])
def register_review(message):
    response = bot.reply_to(message, "Ingrese los detalles de la revision")
    bot.register_next_step_handler(response, review_description)


def review_description(message):
    response = bot.reply_to(
        message, "Ingrese los repuestos utilizados separados por coma")
    record.review["description"] = message.text
    bot.register_next_step_handler(response, review_spare_parts)


def review_spare_parts(message):
    response = bot.reply_to(message, "Ingrese la placa del vehiculo")
    record.review["spare_parts"] = message.text
    bot.register_next_step_handler(response, review_vehicle)


def review_vehicle(message):
    record.review["vehicle_id"] = message.text
    record.review["user_id"] = message.chat.id
    try:
        is_success_transaction = logic.register_review(**record.review)
        if (is_success_transaction):
            markup = with_check_fluids()
            response = bot.reply_to(
                message,
                "Se ha registrado la revision con exito, desea agregar revision de liquidos?",
                reply_markup=markup
            )
            bot.register_next_step_handler(response, check_fluids)
        else:
            bot.send_message(
                message, "Ocurrio un error, posiblemente no estes registrado o el vehiculo no existe")

    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")



def with_check_fluids():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Si')
    itembtn2 = types.KeyboardButton('No')
    markup.add(itembtn1, itembtn2)

    return markup

def check_fluids(message):
    print(message.text)

# Default response
@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")


if __name__ == '__main__':
    bot.polling(timeout=20)
