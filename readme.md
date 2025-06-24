# HR Bot

## Technologies Used
### General
- Python 3
- PostgreSQL 16

### Libraries
- aiogram (for working with the Telegram API)
- sqlalchemy (ORM for working with the database)
- psycopg3 (PostgreSQL database driver)
- pypdf (PDF file parsing)

### Install Dependencies
- Docker
- Docker Compose

## Configuration
- Rename the `.env.example` file to `.env` and replace the bot token and OpenAI key with real ones.
- Get the HR's Telegram ID:
  - Open the @chatIDrobot bot
  - Forward it a message from the person whose ID you want to obtain
  - Get the ID from the `chat_id` field and update the `HR_IDS` field in `docker-compose.yml`
- Unzip `data.zip`. Place the resulting `data` folder in the root of the project.
  
## Run
```bash
docker compose up
```
The database will start first, followed by the bot.

## Project Structure
- bot – main project folder
  - routers – command handlers
  - filters – user category filters for commands
  - database – database handling
  - middlewares – middleware for request processing
  - utils – helper functions
