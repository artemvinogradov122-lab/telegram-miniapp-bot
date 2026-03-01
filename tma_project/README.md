# Telegram Mini App + бот (aiogram)

Этот проект содержит:

- бот на `aiogram 3.x` в папке `bot/`;
- фронтенд мини‑приложения в папке `app/`, которое открывается из бота как WebApp.

## Установка зависимостей

1. Перейдите в папку проекта:

```powershell
cd c:\Users\admin\Desktop\miniapp\tma_project
```

2. (Опционально) создайте виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

3. Установите зависимости:

```powershell
pip install -r requirements.txt
```

4. Заполните `.env`:

- `BOT_TOKEN` — токен бота от BotFather.
- `WEBAPP_URL` — позже сюда будет подставлен HTTPS‑адрес от ngrok.

Пример:

```env
BOT_TOKEN=1234567890:ABCDEF_your_real_token_here
WEBAPP_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

## Настройка и запуск ngrok (HTTPS‑туннель)

1. Перейдите на сайт `https://ngrok.com`, зарегистрируйтесь и скачайте **Windows**‑версию.
2. Распакуйте архив, например в `C:\tools\ngrok`.
3. Добавьте authtoken (его можно посмотреть в личном кабинете ngrok):

```powershell
cd C:\tools\ngrok
.\ngrok.exe config add-authtoken YOUR_NGROK_AUTHTOKEN
```

### Запуск локального сервера для фронтенда

В одном терминале поднимите простой HTTP‑сервер для папки `app/`:

```powershell
cd c:\Users\admin\Desktop\miniapp\tma_project\app
python -m http.server 8000
```

Страница мини‑приложения теперь доступна локально по адресу `http://localhost:8000/`.

### Запуск ngrok для публикации фронтенда

В **другом** терминале запустите ngrok:

```powershell
cd C:\tools\ngrok
.\ngrok.exe http 8000
```

ngrok выдаст временный HTTPS‑адрес вида:

```text
https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

Скопируйте этот адрес и вставьте его в `.env` в поле `WEBAPP_URL`, например:

```env
WEBAPP_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app
```

## Запуск бота

1. Убедитесь, что:
   - `.env` заполнен (`BOT_TOKEN`, `WEBAPP_URL`);
   - HTTP‑сервер (`python -m http.server 8000`) запущен;
   - ngrok (`ngrok http 8000`) запущен и выдаёт HTTPS‑адрес.

2. В новом терминале запустите бота:

```powershell
cd c:\Users\admin\Desktop\miniapp\tma_project
.\.venv\Scripts\activate  # если вы создавали виртуальное окружение
python bot\main.py
```

3. Откройте бота в Telegram, отправьте `/start` и нажмите кнопку
   **«Открыть мини‑приложение»** — откроется WebApp по адресу `WEBAPP_URL`.

Внутри мини‑приложения вы увидите:

- карточку пользователя с именем, username и аватаром (если Telegram передаёт эти данные);
- кнопку **«Отправить данные в бота»** (отправляет payload через `Telegram.WebApp.sendData`);
- кнопку **«Закрыть приложение»**, которая вызывает `Telegram.WebApp.close()`.

