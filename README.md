# goit-pythonweb-hw-10

Розширене REST API з аутентифікацією, верифікацією електронної пошти, обмеженням запитів і завантаженням аватарів. Реалізовано на базі FastAPI, SQLAlchemy, PostgreSQL, Docker.

---

## Функціонал

- Реєстрація користувача з email-верифікацією
- Вхід через JWT
- Отримання інформації про себе `/me`
- Обмеження кількості запитів (rate limiting)
- Завантаження аватара на Cloudinary
- CORS
- CRUD для контактів

---

## Технології

- Python 3.12+
- FastAPI
- PostgreSQL (через Docker)
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn
- JWT (PyJWT)
- Cloudinary
- SMTP
- SlowAPI

---

## Запуск проєкту

### 1. Клонувати репозиторій:

```bash
git clone 
cd goit-pythonweb-hw-10
```

### 2. Створити файл `.env`:

```env
# .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=contacts_db
DB_HOST=db
DB_PORT=5432

SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password

CLOUDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

> 📎 Можна використати шаблон `.env.example`

---

### 3. Запуск через Docker:

```bash
docker compose up --build
```

> API буде доступне за адресою: [http://localhost:8000](http://localhost:8000)

---

## Swagger

Документація:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Приклад POST-запиту на реєстрацію

`POST /auth/signup`

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}
```

---

## Приклад GET-запиту на отримання свого профілю

`GET /auth/me`  
> Потрібен `Bearer` токен у заголовку Authorization

---

## Налаштування середовища

Файл `.env.example` містить шаблон змінних середовища. Створіть `.env` на його основі, щоб налаштувати:

- Підключення до бази даних PostgreSQL
- Секретний ключ для JWT
- SMTP для надсилання листів
- Cloudinary для аватарів

---
