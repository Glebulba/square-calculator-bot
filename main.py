import re
import math
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

solve_session_is_started = False


def correct(string):
    regex = re.compile("-*[0-9]+ -*[0-9]+ -*[0-9]+")
    return len(string.split()) == 3 and regex.findall(string=string)[0] == string


def solve_square_answer(a, b, c):
    if b * b - 4 * a * c >= 0:
        x1 = (-b - math.sqrt((b * b) - (4 * a * c))) / (2 * a)
        x2 = (-b + math.sqrt(b * b - (4 * a * c))) / (2 * a)
        return x1, x2
    else:
        return None


def get_solution_string(message_text):
    if correct(message_text):
        a, b, c = map(int, message_text.split())
        answer = solve_square_answer(a, b, c)
        if answer is not None:
            x1, x2 = answer
            if x1 == x2:
                return str(x1)
            else:
                return str(answer)
        else:
            return "Нет действительных корней"
    else:
        return "Неверный формат данных"


def message_(update, contex):
    global solve_session_is_started
    if solve_session_is_started:
        msg = get_solution_string(update.message.text)
        solve_session_is_started = False
    else:
        msg = "Для ввода коэффициентов, введите команду /solve"
    contex.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def solve_(update, context):
    global solve_session_is_started
    if len(update.message.text) > len("/solve ") and update.message.text.startswith("/solve "):
        msg = get_solution_string(update.message.text[7:len(update.message.text)])
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Введите коэффциенты а,b,c")
        solve_session_is_started = True


def help_(update, context):
    msg = 'Команды:\n' \
          '/help - выводит это сообщение\n' \
          '/solve - решает уравнение заданное в формате: а b c(где a,b,c коэффициенты квадратного уравнения)\n' \
          '/solve a b c - формат ввода данных'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


updater = Updater(token='1689627421:AAEdQYDHTMM5dzaOg26gISCrdf4d9ImuJO8', use_context=True)

dispatcher = updater.dispatcher

help_handler = CommandHandler('help', help_)
dispatcher.add_handler(help_handler)

solve_handler = CommandHandler('solve', solve_)
dispatcher.add_handler(solve_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

message_handler = MessageHandler(Filters.text, message_)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()
