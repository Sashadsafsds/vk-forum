# check_and_post.py
import json
import os
from pathlib import Path
from bot.forum_checker import fetch_posts
from bot.vk_client import send_text
from datetime import datetime

LAST_FILE = Path("last_post.json")

def load_last():
    if not LAST_FILE.exists():
        return {"last_id": None}
    try:
        return json.loads(LAST_FILE.read_text(encoding="utf-8"))
    except:
        return {"last_id": None}

def save_last(data):
    LAST_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    print("Start check:", datetime.utcnow().isoformat())
    try:
        posts = fetch_posts()
    except Exception as e:
        print("Ошибка при получении постов:", e)
        return 2

    if not posts:
        print("Постов не найдено")
        return 0

    last = load_last()
    last_id = last.get("last_id")

    # Найдём новые посты после last_id
    new_posts = []
    for p in posts:
        if p["id"] == last_id:
            break
        new_posts.append(p)

    if not new_posts:
        print("Новых постов нет")
        # но обновим last_id на самый последний на всякий случай
        save_last({"last_id": posts[0]["id"]})
        return 0

    # отправляем новые посты в порядке от старых к новым
    for p in reversed(new_posts):
        text = p["text"]
        # можно форматировать: автор, время, ссылка — если извлечём
        snippet = text if len(text) < 1900 else text[:1900] + "..."
        ok = send_text(snippet)
        if not ok:
            print("Не удалось отправить пост:", p["id"])

    # обновляем последний id
    save_last({"last_id": posts[0]["id"]})
    print(f"Отправлено {len(new_posts)} новых постов.")
    return 0

if __name__ == "__main__":
    exit(main())
