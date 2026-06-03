import time
import requests
import os

USER_KEY = os.environ["PUSHOVER_USER_KEY"]
APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]

URL = "www.youtube.com/@HibachiMana/live"

sent = False
confirm = 0


def is_live():
    try:
        r = requests.get(
            URL,
            allow_redirects=True,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        # 強化ポイント①：URL変化を見る
        final_url = r.url

        # 強化ポイント②：両方チェック（かなり重要）
        if "/watch?v=" in final_url:
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

    # 強化ポイント③：連続3回確認（重要）
    if live_now:
        confirm += 1
    else:
        confirm = 0
        sent = False

    # 強化ポイント④：3回連続で初めて通知
    if confirm >= 3 and not sent:
        requests.post(
            "api.pushover.net/1/messages.json",
            data={
                "token": APP_TOKEN,
                "user": USER_KEY,
                "message": "緋八マナが配信開始しました",
                "title": "ライブ通知",
                "priority": 2,
                "retry": 60,
                "expire": 3600,
            },
            timeout=20
        )

        sent = True
        print("NOTIFIED")

    time.sleep(60)
