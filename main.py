import os
import sys
import settings
import telegram
import random
import re
import twitter_
from util import press_enter
import converter
from languages import get_string


def main():
    """Main function of the program.

    :return: None
    """
    if os.name == 'nt':
        from util import download_ffmpeg
        download_ffmpeg()
    random.seed()
    cfg = settings.Settings()
    while True:
        try:
            tgclass = telegram.TGBot(cfg)
            tg = tgclass.bot
            print("Bot successfully started. Do CTRL-C to stop.")
            if cfg.telegram_user_id is None:
                link_key = ""
                for i in range (0, 6):
                    link_key = link_key + str(random.randint(0,9))
                print("Please send your bot the following code as a Telegram message: " + link_key)
                tgclass.set_auth_code(link_key)
            tg.polling()
            tg.stop_bot()
            print("Bot stopped. It may be because you pressed CTRL-C or because an error occurred. Press enter.")
            press_enter()
            cfg.edit_settings()

        except ValueError as e:
            print("Error. " + e.args)
            sys.exit()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
