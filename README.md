
# eMenu Service

  

## Project Description

eMenu is a service for managing online restaurant menu cards. The project includes APIs for creating, updating, and viewing menus and dishes, managing authentication, and a reporting mechanism.

  

## Prerequisites

- Docker

- Docker Compose

- PostgreSQL 14 (for database management)

- DBeaver (for database management)

- Postman (for API testing)

- Azure files container (for Files)

  

## Environment Setup

1. Clone the project repository.

2. Create a `.env` file in the folder containing `settings.py` with the following environment variables:

  

```plaintext

SECRET_KEY = <your_secret_key>

AZURE_ACCOUNT_NAME = <azure_account_name>

AZURE_ACCOUNT_KEY = <azure_account_key>

AZURE_CONTAINER = <azure_container>

POSTGRES_DB = <database_name>

POSTGRES_USER = <database_user>

POSTGRES_PASSWORD = <database_password>

DATABASE_HOST = db

EMAIL_HOST_USER = <email_user>

EMAIL_HOST_PASSWORD = <email_password>

DEBUG = True

ALLOWED_HOSTS = "127.0.0.1"

```

  

Replace `<...>` with appropriate values.

  

## Docker Commands

-  **Build Docker Compose**:

```bash

docker-compose build

```

-  **Start Services in Detached Mode**:

```bash

docker-compose up -d

```
-  **Restart Services**:

```bash

docker-compose restart

```

-  **Stop Running Services**:

```bash

docker-compose stop

```

-  **Bring Down Services and Remove Volumes**:

```bash

docker-compose down

```

-  **Create and Apply Database Migrations**:

```bash

docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

```

-  **Create Superuser**:

```bash

docker-compose exec web python manage.py createsuperuser

```

  

## Launch Instructions

1. Build and start the Docker containers:

```bash

docker-compose up --build -d

```

2. Create a superuser:

```bash

docker-compose exec web python manage.py createsuperuser

```

3. The application will be available at: `http://127.0.0.1:8000/`

  

## Testing

Run the tests using:

```bash

docker-compose  exec  web  python  manage.py  test

  

## API Documentation

The  API  documentation  is  available  at: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)

  

For  testing  logged-in  users,  use  the  JWT  token  obtained  during  authentication.

  

## Additional Notes

-  The  project  uses  JWT  authentication.  Creating  a  superuser  for  application  management  is  recommended.

-  Use  Postman  for  testing  the  API  with  a  JWT  token.

-  Localization  settings  and  query  optimization  for  the  database  have  been  considered  in  the  project.