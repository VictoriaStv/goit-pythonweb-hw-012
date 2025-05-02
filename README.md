# goit-pythonweb-hw-12

Розширене REST API з підтримкою авторизації, верифікації email, rate limiting та завантаженням аватарів. Побудоване на базі FastAPI, Docker та PostgreSQL.

---

##  Основний функціонал

-  Реєстрація з email-підтвердженням  
-  Вхід з JWT-аутентифікацією  
-  Отримання власного профілю (`/me`)  
-  Обмеження кількості запитів (rate limiting)  
-  Завантаження аватарів на Cloudinary  
-  Підтримка CORS  
-  CRUD-операції для контактів

---

##  Технології

- Python 3.12+
- FastAPI
- PostgreSQL (через Docker)
- SQLAlchemy + Alembic
- Pydantic
- JWT (PyJWT)
- Uvicorn
- Cloudinary API
- SMTP (email)
- SlowAPI (rate limiting)

---

## Запуск проєкту

### 1. Клонування репозиторію

```bash
git clone <your_repo_url>
cd goit-pythonweb-hw-12
```

### 2. Створення `.env`

```env
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

>  Скористайтесь шаблоном `.env.example`, щоб швидко налаштувати змінні середовища.

---

### 3. Запуск у Docker

```bash
docker compose up --build
```

> Застосунок буде доступний за адресою:  
> [http://localhost:8000](http://localhost:8000)

---

##  Документація (Swagger UI)

Доступна за адресою:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Приклади запитів

### Реєстрація користувача
`POST /auth/signup`

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}
```

### Отримання профілю
`GET /auth/me`  
> Потрібен токен у заголовку: `Authorization: Bearer <access_token>`

---

## Налаштування середовища

У файлі `.env.example` зібрані всі необхідні змінні для:

- підключення до PostgreSQL  
- роботи з JWT  
- надсилання листів через SMTP  
- інтеграції з Cloudinary
