import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "27872628")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "7827da20241e75908c85deb5b44e7bea")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7044609105:AAEbL7gi84MMfESHFnsoSBsHVVyHNB1IQCo")  # ⚠️ Required

    # database config
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://s2lk:s2lk@cluster0.h2h9ia6.mongodb.net/?retryWrites=true&w=majority")  # ⚠️ Required
    DB_NAME = os.environ.get("DB_NAME", "AutoAcceptBot")

    # other configs
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/0ceb5f176f3cf877a08b5.jpg")
    ADMIN = int(os.environ.get('ADMIN', '7181106700'))  # ⚠️ Required
    DEFAULT_WELCOME_MSG = os.environ.get("WELCOME_MSG", "Hey {user},\nYour Request Approved ✅,\n\nWelcome to **{title}**")
    DEFAULT_LEAVE_MSG = os.environ.get("LEAVE_MSG", "By {user},\nSee You Again 👋\n\nFrom **{title}**")

    # user client config
    SESSION = os.environ.get("SESSION", "BQFPq6kAGlC1i1BxEpKYNOfHEaIhjTHOZNd4TURN7rfeL27Qilf925LsasW24i_gj9uXB_h2Y5TeMFoz-AJqbf8oMKGh_BgUTFyYYsJ7QrgO8_-LSCNZcWnykE7H5kpzZpWb4fU03BXd_lUntYj68mDXWvNw4OcNuorK8azmj5XT1NiXOkfa_R4XxHxD5emylvlAQSW0IUlhliNQGXjpB3j648oLYjY8C71WIQNETUdfUvBzouSOITzgCd_VjsfEtU45JK-Sb8_QMWs-hhzADekSbat1cWAsy58ZNwAobxlLQ8LVQbqVSUN1RRbmPP7E_mECNRTsmOMBuBlh_-be0AY7VUacogAAAAGtSVqzAA")  # ⚠️ Required @SnowStringGenBot

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "4040"))


class TxT(object):

    HELP_MSG = """
<b> ADMIN Available commands:- </b>

➜ /set_welcome - To set custom welcome message (support photo & video & animation or gif)
➜ /set_leave - To set custom leave message (support photo & video & animation or gif)
➜ /option - To toggle your welcome & leave message also auto accept (whether it'll show to user or not and will auto accept or not)
➜ /auto_approves - To toggle your auto approve channel or group
➜ /status - To see status about bot
➜ /restart - To restart the bot
➜ /broadcast - To brodcast the users (only those user who has started your bot)
➜ /acceptall - To accept all the pending join requests
➜ /declineall - To decline all the pending join requests

⚠️ <b> Support HTML & Markdown formating in welcome or leave message for more info <a href=https://core.telegram.org/api/entities#:~:text=%2C%20MadelineProto.-,Allowed%20entities,-For%20example%20the> Link </a>. </b>


<b>⦿ Developer:</b> <a href=https://t.me/Snowball_Official>ѕησωвαℓℓ ❄️</a>
"""
