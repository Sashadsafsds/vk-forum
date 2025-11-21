# bot/forum_checker.py
import os
import requests
from bs4 import BeautifulSoup
import hashlib

XF_USER = os.getenv("XF_USER")
XF_SESSION = os.getenv("XF_SESSION")
XF_TFA_TRUST = os.getenv("XF_TFA_TRUST")
TOPIC_ID = os.getenv("TOPIC_ID")  # ID темы, например "51821"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def build_cookie():
    parts = []
    if XF_USER:
        parts.append(f"xf_user={XF_USER}")
    if XF_SESSION:
        parts.append(f"xf_session={XF_SESSION}")
    if XF_TFA_TRUST:
        parts.append(f"xf_tfa_trust={XF_TFA_TRUST}")
    return "; ".join(parts)

def get_topic_url():
    if not TOPIC_ID:
        raise ValueError("TOPIC_ID не задан")
    return f"https://matrp.ru/threads/{TOPIC_ID}/"

def fetch_posts():
    """
    Возвращает список постов (новейшие в начале) как словарей:
    { "id": <строка>, "text": <строка> }
    Для id берём комбинацию (если есть) data-message-id или хэш текста.
    """
    url = get_topic_url()
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": build_cookie()
    }
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Ошибка доступа к форуме: {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Попытка найти сообщения: класс .js-post (или .message etc.) — подстрой при необходимости.
    posts_html = soup.select(".message, .message--post, .structItem--thread .message") or soup.select(".message-body")
    posts = []
    for ph in posts_html:
        # попробуем доставать id
        pid = ph.get("data-message-id") or ph.get("id") or None
        text = ph.get_text(separator="\n", strip=True)
        if not pid:
            pid = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        posts.append({"id": str(pid), "text": text})
    # Удалим дубликаты и оставим уникальные
    unique = []
    seen = set()
    for p in posts:
        if p["id"] not in seen:
            unique.append(p)
            seen.add(p["id"])
    # Возвращаем в порядке от новых к старым, если сайт вывел старые вначале — возможно потребуется reverse
    return unique[::-1] if len(unique) else unique
