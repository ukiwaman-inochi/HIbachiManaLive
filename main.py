import os
import time
import requests

USER_KEY = os.environ["PUSHOVER_USER_KEY"]
APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]

sent = False
confirm = 0

URL = "www.youtube.com/@HibachiMana/live"

def is_live():
    try:
        r = requests.get(
            URL,
            allow_redirects=False,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code == 302:
            return True

        if "watching" in r.text:
            return True

        return False

    except Exception as e:
        print("error:", e)
        return False


while True:
    live_now = is_live()

    print("live:", live_now, "confirm:", confirm, "sent:", sent)

    if live_now:
        confirm += 1
    else:
        confirm = 0
        sent = False

    if confirm >= 2 and not sent:
        requests.post(
            "api.pushover.net/1/messages.json",
            data={
                "token": APP_TOKEN,
                "user": USER_KEY,
                "message": "緋八マナが配信開始しました",
                "title": "緋八マナライブ通知",
                "priority": 2,
                "retry": 60,
                "expire": 3600,
            },
            timeout=20
        )
        sent = True
        print("NOTIFIED")

    time.sleep(60)
