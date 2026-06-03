import os

print("ENV KEYS:")
print(list(os.environ.keys()))

import time
import requests

USER_KEY = os.environ["PUSHOVER_USER_KEY"]
APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]

sent = False

requests.post(
    "api.pushover.net/1/messages.json",
    data={
        "token": APP_TOKEN,
        "user": USER_KEY,
        "message": "テスト通知成功！",
        "title": "緋八マナ通知システム",
        "priority": 2,
        "retry": 60,
        "expire": 3600,
    },
)

while True:
    try:
        r = requests.get(
            "www.youtube.com/@HibachiMana/live",
            allow_redirects=False,
            timeout=20
        )

        live_now = r.status_code == 302

        if live_now and not sent:
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
            )
            sent = True

        if not live_now:
            sent = False

    except Exception as e:
        print(e)

    time.sleep(60)

