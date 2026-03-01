// Работа с Telegram Web App API
const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;

if (tg) {
    // Сообщаем Telegram, что мини‑приложение готово
    if (typeof tg.ready === "function") {
        tg.ready();
    }
    tg.expand();
}

const nameEl = document.getElementById("user-name");
const usernameEl = document.getElementById("user-username");
const avatarEl = document.getElementById("user-avatar");
const userCardEl = document.getElementById("user-card");

function fillUserFromTelegram() {
    if (!tg || !tg.initDataUnsafe || !tg.initDataUnsafe.user) {
        if (nameEl) {
            nameEl.textContent = "Откройте приложение внутри Telegram";
        }
        if (usernameEl) {
            usernameEl.textContent = "";
        }
        if (avatarEl) {
            avatarEl.style.display = "none";
        }
        return;
    }

    const user = tg.initDataUnsafe.user;

    if (nameEl) {
        const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ");
        nameEl.textContent = fullName || "Без имени";
    }

    if (usernameEl) {
        usernameEl.textContent = user.username ? `@${user.username}` : "";
    }

    if (avatarEl) {
        if (user.photo_url) {
            avatarEl.src = user.photo_url;
            avatarEl.style.display = "block";
        } else {
            avatarEl.style.display = "none";
        }
    }
}

document.addEventListener("DOMContentLoaded", fillUserFromTelegram);

// Кнопка "Отправить данные в бота"
const actionButton = document.getElementById("action-button");

if (actionButton) {
    actionButton.addEventListener("click", () => {
        const payload = {
            action: "demo",
            timestamp: Date.now(),
        };

        if (tg && typeof tg.sendData === "function") {
            tg.sendData(JSON.stringify(payload));
        } else {
            alert("Telegram Web App API недоступен. Откройте страницу внутри Telegram.");
        }
    });
}

// Кнопка "Закрыть приложение"
const closeButton = document.getElementById("close-button");

if (closeButton) {
    closeButton.addEventListener("click", () => {
        if (tg && typeof tg.close === "function") {
            tg.close();
        } else {
            window.close();
        }
    });
}

