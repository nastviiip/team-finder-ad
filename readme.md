# TeamFinder

TeamFinder — это веб-платформа для поиска единомышленников и создания команд для IT-проектов. Проект реализован в рамках Варианта 2: пользователи могут указывать свои навыки, а другие участники могут фильтровать пользователей по этим навыкам.

## Автор

- **Попова Анастасия Павловна**
- **GitHub:** [nastviiip](https://github.com/nastviiip)
- **Email:** [ana0707@gmail.com](mailto:ana0707@gmail.com)

## Техно-стек

- **Backend:** Python 3.10, Django 5.2
- **Database:** PostgreSQL (в Docker-контейнере)
- **Frontend:** HTML, CSS, JavaScript (Vanilla JS), AJAX
- **Инструменты:** Docker Compose, python-dotenv, Pillow

---

## Развертывание проекта

### 1. Клонирование репозитория

Для начала клонируйте репозиторий на свой локальный компьютер и перейдите в папку проекта:

```bash
git clone https://github.com/nastviiip/team-finder-ad.git
cd team-finder-ad
```

### 2. Виртуальное окружение и зависимости

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Переменные окружения

Создайте файл `.env` в корне проекта на основе шаблона:

```bash
cp .env_example .env
```

Убедитесь, что в файле `.env` указан правильный вариант задания: `TASK_VERSION=2`.

### 4. Подготовка Базы Данных (Развертывание)

Запустите PostgreSQL в Docker-контейнере:

```bash
docker compose up -d
```

Примените миграции для создания таблиц в базе данных:

```bash
python manage.py migrate
```

### 5. Наполнение демо-данными

Создайте суперпользователя (администратора), от имени которого можно будет управлять проектом:

```bash
python manage.py createsuperuser
```

*(После запуска сайта вы сможете зайти под этими данными и создать демо-проекты).*

---

## Запуск проекта

После успешного развертывания запустите локальный сервер разработки:

```bash
python manage.py runserver
```

## Адреса сайта

- [Главная страница TeamFinder](http://127.0.0.1:8000/)
- [Панель Администратора](http://127.0.0.1:8000/admin/)
