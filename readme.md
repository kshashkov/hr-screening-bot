# HR Bot

## Используем
### General
- Python 3
- PostgreSQL 16
## Библиотеки
- aiogram (для работы с Telegram API)
- sqlalchemy (ORM для работы с базой данных)
- psycopg3 (драйвер для базы данных PostgreSQL)

## Установить зависимости
- Docker
- Docker Compose

## Конфигурация
- Переименовать файл .env.example в .env и заменить в нем токен бота и OpenAI на реальные
- Получить telegram ID HR:
  - Открывать @chatIDrobot бота
  - Пересылаем ему сообщение от человека id которого хотим получить
  - Из поля chat_id получаем id и редактируем пункт HR_IDS в docker-compose.yml
  
## Запуск
```bash
docker compose up
```
Запустится база, а потом и бот

## Структура проекта
- bot - главная папка проекта
  - routers - обработчики команд
  - filters - фильтры для команд
  - database - работа с базой данных
  - middlewares - middleware для обработки запросов
  - utils - вспомогательные функции
