# E-commerce Backend
Backend интернет-магазина на FastAPI с асинхронной архитектурой, PostgreSQL и Alembic. Реализована система аутентификации и авторизации пользователей, управление категориями товаров и отзывы. <!-- описание репозитория -->
<!--Блок информации о репозитории в бейджах-->
![Static Badge](https://img.shields.io/badge/iklimantov-fastapi-ecommerce)
![GitHub top language](https://img.shields.io/github/languages/top/iklimantov/fastapi-ecommerce-backend)
![GitHub](https://img.shields.io/github/license/iklimantov/fastapi-ecommerce-backend)
![GitHub Repo stars](https://img.shields.io/github/stars/iklimantov/fastapi-ecommerce-backend)
![GitHub issues](https://img.shields.io/github/issues/iklimantov/fastapi-ecommerce-backend)

<!--![Logotype](./docs/img.png)-->

<!--Установка-->
## Установка (Windows)
<!--У вас должны быть установлены [зависимости проекта](https://github.com/iklimantov/fastapi-ecommerce-backend/blob/main/requirements#зависимости)-->


### 1. Клонирование репозитория 

```git clone https://github.com/iklimantov/fastapi-ecommerce-backend```

### 2. Переход в директорию проекта

```bash
cd fastapi-ecommerce-backend
```

### 3. Создание виртуального окружения

```bash
python -m venv venv
```

### 4. Активация виртуального окружения

```
source venv/bin/activate # для Linux / MacOS
venv\Scripts\activate      # для Windows
```

### 5. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 6. Создание файла конфигурации

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```
После этого заполните переменные окружения в файле .env.

### 7. Запуск приложения через uvicorn

```bash
uvicorn app.main: app --reload
```

<!--Пользовательская документация-->
<!--## Документация-->
<!--Пользовательскую документацию можно получить по [этой ссылке](./docs/ru/index.md).-->

<!--[Релизы программы]: https://github.com/OkulusDev/Oxygen/releases -->

<!--Поддержка-->
## Поддержка
Если у вас возникли сложности или вопросы по использованию пакета, создайте 
[обсуждение](https://github.com/iklimantov/fastapi-ecommerce-backend/issues/new/choose) в данном репозитории или напишите на электронную почту <iklimantov@yandex.ru>.

<!--зависимости-->
## Зависимости
Эта программа зависит от интепретатора Python версии 3.12 или выше, PIP 25.1.1 или выше. 

<!--описание коммитов-->
## Описание коммитов
### (Начиная с 13.02.2026)

| Название | Описание                                                        |
|----------|-----------------------------------------------------------------|
| build	   | Сборка проекта или изменения внешних зависимостей               |
| sec      | Безопасность, уязвимости                                        |
| ci       | Настройка CI и работа со скриптами                              |
| docs	   | Обновление документации                                         |
| feat	   | Добавление нового функционала                                   |
| fix	   | Исправление ошибок                                              |
| perf	   | Изменения направленные на улучшение производительности          |
| refactor | Правки кода без исправления ошибок или добавления новых функций |
| revert   | Откат на предыдущие коммиты                                     |
| style	   | Правки по кодстайлу (табы, отступы, точки, запятые и т.д.)      |
| test	   | Добавление тестов                                               |