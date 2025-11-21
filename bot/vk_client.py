# bot/vk_client.py
import os
import vk_api

VK_TOKEN = os.getenv("VK_TOKEN")  # token группы
VK_PEER_ID = int(os.getenv("VK_PEER_ID", "0"))  # куда отправлять: peer_id (чат или пользователь)

def send_text(message: str):
    if not VK_TOKEN or VK_PEER_ID == 0:
        print("VK_TOKEN или VK_PEER_ID не заданы, пропускаю отправку")
        return False

    try:
        session = vk_api.VkApi(token=VK_TOKEN)
        vk = session.get_api()
        vk.messages.send(
            peer_id=VK_PEER_ID,
            message=message,
            random_id=0
        )
        print("Отправлено в VK")
        return True
    except Exception as e:
        print("Ошибка отправки в VK:", e)
        return False

