import os
import sys
import settings
import telegram
import random
from util import press_enter
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
            print(get_string("bot_started"))
            if cfg.telegram_user_id is None:
                link_key = ""
                for i in range (0, 6):
                    link_key = link_key + str(random.randint(0,9))
                print(get_string("register_key").format(link_key))
                tgclass.set_auth_code(link_key)
            tg.polling()
            tg.stop_bot()
            print(get_string("bot_stopped"))
            press_enter()
            cfg.edit_settings()

        except ValueError as e:
            print("Error. " + str(e.args))
            sys.exit()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
