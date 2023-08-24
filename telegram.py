#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import yaml
import random
import logging
import copy
import re
import os

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

current_list = []
trash_list = []
current_task = (" ", " ")
combo = 0
topic = "a1"
filename = "unistrapg.yaml"
mode = "No"  # Test, Learn, Study, No


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mode
    global current_list
    global current_task
    global topic
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user.username != "ruslan130":
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Unfortanutely this bot is for Ruslan only."
        )
        return
    lang = update.effective_user.language_code
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! It is time to test Italian! "+lang
    )
    mode = "Test"
    with open(filename, mode="r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        words = data[topic]
        keys = list(words.keys())
        new_list = [(key, words[key]) for key in keys]
        inv_map = {v: k for k, v in words.items()}
        values = list(inv_map.keys())
        second_list = [(key, inv_map[key]) for key in values]
        current_list = new_list + second_list
        random.shuffle(current_list)
    current_task = current_list.pop(0)
    await update.message.reply_text(current_task[0])


async def study(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_list
    global current_task
    global mode
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user.username != "ruslan130":
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Unfortanutely this bot is for Ruslan only."
        )
        return
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! It is time to study Italian!"
    )
    mode = "Study"
    with open(filename, mode="r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        words = data["to_learn"]
        if not words:
            await update.message.reply_html("There is no words to study!")
            mode = "No"
            return
        await update.message.reply_html("It is founded " + str(len(words)) + " words to study.")
        keys = list(words.keys())
        new_list = [(key, words[key]) for key in keys]
        inv_map = {v: k for k, v in words.items()}
        values = list(inv_map.keys())
        second_list = [(key, inv_map[key]) for key in values]
        current_list = new_list + second_list
        random.shuffle(current_list)
    current_task = current_list.pop(0)
    await update.message.reply_text(current_task[0])


def rus_lat(string):
    x = copy.copy(string)
    a = {'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T',
         'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P',
         'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D',
         'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K',
         'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X',
         'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M',
         'Б': '<', 'Ю': '>', 'Ё': '~', 'й': 'q', 'ц': 'w',
         'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
         'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
         'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g',
         'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';',
         'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v',
         'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
         'ё': '`'}  # Список со всеми значениями
    res = ''  # Создание пустой строки
    j = 0  # Используется для выбора определённой буквы из x
    while j < len(x):  # Пока j < длинны строки x выполняется цикл
        if x[j] in a:  # Если в списке a есть буква из x под номером j, выполняется перевод в английскую раскладку
            i = a[x[j]]
            res += i
        else:  # Иначе добавляет пробел
            res += ' '
        j += 1
    return res

def lat_rus(string):
    x = copy.copy(string)
    a = {'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T',
         'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P',
         'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D',
         'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K',
         'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X',
         'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M',
         'Б': '<', 'Ю': '>', 'Ё': '~', 'й': 'q', 'ц': 'w',
         'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
         'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
         'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g',
         'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';',
         'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v',
         'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
         'ё': '`'}  # Список со всеми значениями
    new_dict = {
        value: key for key, value in a.items()
    }
    res = ''  # Создание пустой строки
    j = 0  # Используется для выбора определённой буквы из x
    while j < len(x):  # Пока j < длинны строки x выполняется цикл
        if x[j] in new_dict:  # Если в списке a есть буква из x под номером j, выполняется перевод в английскую раскладку
            i = new_dict[x[j]]
            res += i
        else:  # Иначе добавляет пробел
            res += ' '
        j += 1
    return res


async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_list
    global current_task
    global mode
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user.username != "ruslan130":
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Unfortanutely this bot is for Ruslan only."
        )
        return
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! It is time to learn Italian!"
    )
    mode = "Learn"
    with open(filename, mode="r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        words = data["to_learn"]
        if not words:
            await update.message.reply_html("There is no words to learn!")
            mode = "No"
            return
        await update.message.reply_html("It is founded " + str(len(words)) + " words to learn.")
        keys = list(words.keys())
        new_list = [(key, words[key]) for key in keys]
        inv_map = {v: k for k, v in words.items()}
        values = list(inv_map.keys())
        second_list = [(key, inv_map[key]) for key in values]
        current_list = new_list + second_list
        random.shuffle(current_list)
    current_task = current_list.pop(0)
    await update.message.reply_text(current_task[0])


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def Convert(tup, di):
    di = dict(tup)
    return di


def has_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")



async def protest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global trash_list
    if mode == "Test" and len(trash_list) > 0:
        await update.message.reply_text("Protest accepted.")
        trash_list.pop()
    else:
        await update.message.reply_text("Protest declined.")


async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mode
    global current_task
    if mode == "No":
        await update.message.reply_text("Choose the dict that you prefer.")
        mode = "Choose"
    else:
        await update.message.reply_text("You cant change the word during the training.")


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global current_list
    global trash_list
    global current_task
    global combo
    global mode
    user = update.effective_user
    if user.username != "ruslan130":
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Unfortanutely this bot is for Ruslan only."
        )
        return
    if mode == "No" or mode == "Change":
        mode = "No"
        current_task = (" ", " ")
        await update.message.reply_text("Please write command: /start, /learn, /study.")
        return
    if mode == "Study":
        await update.message.reply_text("The progress cannot be saved because you are in study mode!")
        current_list.clear()
        trash_list.clear()
        current_task = (" ", " ")
        mode = "No"
        combo = 0
        return
    with open(filename, mode="r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if mode == "Learn":
            temp = current_list + trash_list + [current_task]
        else:
            temp = trash_list
        temp2 = {}
        temp2 = Convert(temp, temp2)
        keys = list(temp2.keys())
        for each in keys:
            if has_cyrillic(each):
                value = temp2[each]
                del temp2[each]
                temp2[value] = each
        if mode == "Learn":
            data["to_learn"] = temp2
        if mode == "Test":
            data["to_learn"].update(temp2)
    with open(filename, mode="w", encoding="utf-8") as f:
        yaml.dump(data, f)
    await update.message.reply_text("The progress was saved! " + str(len(temp2)) + " is rest to learn.")
    current_list.clear()
    trash_list.clear()
    current_task = (" ", " ")
    mode = "No"
    combo = 0

async def load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mode
    global current_task
    if mode == "No":
        await update.message.reply_text(
            "Please paste the new dict:")
        mode = "Load"
    else:
        await update.message.reply_text("You cant load the word during the training.")


async def change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global mode
    global current_task
    if mode == "Change":
        await update.message.reply_text("Ok. Lets start again. Write the word you want to change:")
        current_task = (" ", " ")
        return
    if mode == "No":
        await update.message.reply_text(
            "We are in change mode. In case of error write /change. Write the word you want to change:")
        mode = "Change"
    else:
        await update.message.reply_text("You cant change the word during the training.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global trash_list
    global current_task
    global current_list
    global combo
    global mode
    global topic
    if mode == "Load":
        input_string = update.message.text
        input_list = list(input_string.split("\n"))
        data_new = {}
        for each in input_list:
            each_list = list(each.split(": "))
            data_new[each_list[0]] = each_list[1]
        with open(filename, mode="r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            data["loaded"] = data_new
        with open(filename, mode="w", encoding="utf-8") as f:
            yaml.dump(data, f)
        topic = "loaded"
        mode = "No"
        await update.message.reply_text("The new dict have been successfully loaded")
        return
    if mode == "Choose":
        new_topic = update.message.text
        with open(filename, mode="r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if new_topic in data:
                topic = new_topic
                await update.message.reply_text("The new dict have been successfully chosen")
            else:
                await update.message.reply_text("It is unknown dict.")
            mode = "No"
            return
    if mode == "Change":
        if current_task[0] == " ":
            current_task = (update.message.text, " ")
            await update.message.reply_text("Please write the correct word:")
        else:
            if current_task[1] == " ":
                old = current_task[0]
                current_task = (old, update.message.text)
                await update.message.reply_text("Please write the translation:")
            else:
                with open(filename, mode="r", encoding="utf-8") as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    for every in data:
                        if current_task[0] in data[every]:
                            del data[every][current_task[0]]
                            data[every][current_task[1]] = update.message.text
                    await update.message.reply_text("The word was successfully changed.")
                    current_task = (" ", " ")
                    mode = "No"
                with open(filename, mode="w", encoding="utf-8") as f:
                    yaml.dump(data, f)
        return

    if mode == "No":
        await update.message.reply_text("Please write command: /start, /learn, /study, /change, /save, /choose, /protest, /load.")
        return
    if update.message.text.lower() == current_task[1].lower() or rus_lat(update.message.text.lower()) == current_task[
        1].lower() or lat_rus(update.message.text.lower()) == current_task[1].lower():
        await update.message.reply_text("Correct!")
        combo += 1
        if combo > 2:
            await update.message.reply_text("Combo! x" + str(combo))
            await update.message.reply_text("🔥")
    else:
        await update.message.reply_text("Wrong: " + current_task[1])
        combo = 0
        trash_list.append(current_task)
    if not current_list:
        if trash_list and mode != "Test":
            current_list = copy.copy(trash_list)
            random.shuffle(current_list)
            trash_list.clear()
        else:
            await update.message.reply_text("Ok we are done!")
            if mode == "Study":
                await update.message.reply_text("The progress cannot be saved because you are in study mode!")
                current_list.clear()
                trash_list.clear()
                current_task = (" ", " ")
                mode = "No"
                combo = 0
                return
            with open(filename, mode="r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if mode == "Learn":
                    temp = current_list + trash_list
                else:
                    temp = trash_list
                temp2 = {}
                temp2 = Convert(temp, temp2)
                keys = list(temp2.keys())
                for each in keys:
                    if has_cyrillic(each):
                        value = temp2[each]
                        del temp2[each]
                        temp2[value] = each
                if mode == "Learn":
                    data["to_learn"] = temp2
                if mode == "Test":
                    data["to_learn"].update(temp2)
            with open(filename, mode="w", encoding="utf-8") as f:
                yaml.dump(data, f)
            await update.message.reply_text("The progress was saved! " + str(len(temp2)) + " is rest to learn.")
            current_list.clear()
            trash_list.clear()
            current_task = (" ", " ")
            mode = "No"
            combo = 0
            return
    current_task = current_list.pop(0)
    await update.message.reply_text(current_task[0])


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = "token"

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("learn", learn))
    application.add_handler(CommandHandler("study", study))
    application.add_handler(CommandHandler("change", change))
    application.add_handler(CommandHandler("save", save))
    application.add_handler(CommandHandler("choose", choose))
    application.add_handler(CommandHandler("protest", protest))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("load", load))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
