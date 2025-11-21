# VK Forum Monitor

Мониторит тему на форуме matrp.ru и присылает новые сообщения в ВК.

## Как настроить

1. Залей репозиторий на GitHub.
2. В Settings → Secrets and variables → Actions → New repository secret добавь:
   - `VK_TOKEN` — токен группы вк (messages)
   - `VK_PEER_ID` — numeric peer_id (чат или пользователь)
   - `XF_USER` — значение cookie xf_user
   - `XF_SESSION` — значение cookie xf_session
   - `XF_TFA_TRUST` — значение cookie xf_tfa_trust (если есть 2FA)
   - `TOPIC_ID` — ID темы на matrp.ru
3. Проверь файл `requirements.txt`.
4. Запусти workflow вручную или дождись cron (каждые 5 минут).
