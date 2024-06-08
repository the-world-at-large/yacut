# URL Shortener

URL Shortener - это веб-приложение для сокращения длинных URL-адресов. Приложение предоставляет API для создания коротких ссылок и получения оригинальных URL по коротким ссылкам.

## Установка

### Требования

- Python 3.8+
- Flask
- SQLAlchemy

### Установка зависимостей

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/your-username/url-shortener.git
    cd url-shortener
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

### Настройка базы данных

1. Создайте файл конфигурации `config.py` и добавьте настройки базы данных:

    ```python
    import os

    class Config:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'yacut.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```

2. Инициализируйте базу данных:

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

## Запуск

1. Запустите приложение:

    ```bash
    flask run
    ```

2. Откройте браузер и перейдите по адресу `http://127.0.0.1:5000`.

## API

### Создание короткой ссылки

**Запрос:**

```http
POST /api/id/
Content-Type: application/json

{
    "url": "http://example.com",
    "custom_id": "custom123"  # не обязательное поле
}

Ответ:

{
    "short_link": "http://127.0.0.1:5000/custom123",
    "url": "http://example.com"
}


## Тестирование
Для запуска тестов используйте *pytest*:

```pytest
```

## Автор

Автор: [the-world-at-large](https://github.com/the-world-at-large)

## Лицензия

Этот проект лицензируется по лицензии MIT. См. файл `LICENSE` для получения дополнительной информации.
