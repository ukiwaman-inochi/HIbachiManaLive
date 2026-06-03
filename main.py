import os
import time
import requests

USER_KEY = os.environ["PUSHOVER_USER_KEY"]
APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]

URL = "https://www.youtube.com/@HibachiMana/live"

confirm = 0
sent = False


def is_live():
    try:
        r = requests.get(
            URL,
            allow_redirects=True,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        final_url = r.url
        html = r.text.lower()

        # ===== 重要ロジック =====

        # ① 明確なライブページ判定
        if "/watch?v=" in final_url:

            # ② 待機所（プレミア枠）除外
            if "list=" in final_url:
                return False

            # ③ 追加保険（ライブ要素）
            if "watching" in html or "live" in html:
                return True

        return False

    except Exception as e:
        print("error:", e)
        return False


while True:
    live_now = is_live()

    print("live:", live_now, "confirm:", confirm, "sent:", sent)

    # ===== 連続判定（誤爆防止） =====
    if live_now:
        confirm += 1
    else:
        confirm = 0
        sent = False

    # ===== 3回連続で確定通知 =====
    if confirm >= 3 and not sent:
        try:
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

        except Exception as e:
            print("push error:", e)

    time.sleep(60)
