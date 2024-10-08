# Описание работы API

API написано с использованием FastAPI и предоставляет следующие возможности:
1. **Загрузка файлов**: Файлы могут быть загружены на локальное хранилище или в облако (например, Amazon S3). API принимает файл через HTTP-запрос и сохраняет его в указанное место.
2. **Выгрузка файлов**: API позволяет получать файлы по их уникальному идентификатору (UID). Запрос к соответствующему маршруту вернет файл.
3. **Потоковая загрузка**: Поддерживается функция потоковой передачи файлов, что особенно полезно для больших файлов.

## Миграции базы данных
Для управления миграциями базы данных используется Alembic. Миграции хранятся в директории `alembic/` и конфигурируются через `alembic.ini`.

## Контейнеризация
Проект полностью контейнеризирован, используя Docker. Основные файлы конфигурации для контейнеризации — `Dockerfile` и `docker-compose.yaml`.

## Логи и тестирование
Логи записываются в директорию `logs/`, что позволяет отслеживать работу приложения и ошибки. Для тестирования используются юнит-тесты, расположенные в `tests/unit_test/`.


## Запуск Api
1. Клонирование репозитория.
2. Настройка .env файла.

Необходимо настроить файл окружения .env. 

Файл .env находится в корневой директории проекта.

Укажите необходимые параметры для S3-хранилища.

```
ACCESS_KEY=<ваш access key>
SECRET_KEY=<ваш secret key>
ENDPOINT_URL=<путь до s3 хранилища>
BUCKET_NAME=<имя вашего S3-бакета>
```

3.Собрать докер контейнер
```docker-compose up --build ```


## Тестирование
Для тестирование используется pytest.
Для запуска нужно перейти в корень проекта и запустить тестирование командой 
```commandline
pytest
```

## Структура директорий проекта

- **`core/`**: Основной модуль, содержащий ключевые компоненты приложения.
  - **`alembic/`**: Содержит файлы миграции базы данных, управляемые с помощью Alembic.
  - **`http_load/`**: Здесь находится логика роутинга и обработки HTTP-запросов.
    - `router.py`: Файл, содержащий маршруты для HTTP-запросов, таких как загрузка и выгрузка файлов.
  - **`logs/`**: Директория для хранения логов.
    - `error_logs.log`: Лог-файл, в который записываются ошибки.
    - `logs.py`: Скрипт для конфигурации и управления логированием.
  - **`models/`**: Модели, используемые в приложении.
    - `files_models.py`: Модели данных, связанные с файлами, такими как метаданные и другие атрибуты.
  - **`orm/`**: Управление взаимодействием с базой данных через SQLAlchemy.
    - `base_orm.py`: Базовый файл ORM, определяющий основную конфигурацию SQLAlchemy.
    - `file_orm.py`: Модели и схемы базы данных для работы с файлами.
  - **`services/`**: Бизнес-логика приложения.
    - `file_service.py`: Сервисы, связанные с обработкой и управлением файлами.
    - `s3_service.py`: Логика взаимодействия с S3-совместимым облачным хранилищем.
    - `streaming_service.py`: Реализация потоковой загрузки файлов.
  - **`streaming_load/`**: Директория для реализации потоковой загрузки.
    - `router.py`: Роуты, связанные с потоковой передачей данных.

- **`static/`**: Статические файлы, хранящиеся в приложении.
  - **`images_files/`**: Директория для хранения изображений.
  - **`media_files/`**: Медиа-файлы, такие как видео и аудио.
  - **`other_files/`**: Другие типы файлов.
  - **`txt_files/`**: Текстовые файлы.

- **`tests/`**: Модуль для тестирования.
  - **`unit_test/`**: Юнит-тесты для проверки отдельных компонентов.
    - `conftest.py`: Файл конфигурации для Pytest.
    - `mock_files.json`: Мокированные данные для тестов.

- **`utils/`**: Вспомогательные утилиты.
  - `file_utils.py`: Утилиты для работы с файлами, такие как валидация, преобразование и т.д.
  - `validator_file.py`: Файл для валидации входных данных.
  - `config.py`: Конфигурационный файл для всего приложения.
  - `database.py`: Настройки базы данных, такие как подключение и сессии.
  - `main.py`: Главный файл запуска приложения.

- **`Dockerfile`** и **`docker-compose.yaml`**: Файлы конфигурации Docker для контейнеризации приложения.

- **`alembic.ini`**: Конфигурация Alembic для управления миграциями базы данных.

- **`pyproject.toml`** и **`pytest.ini`**: Файлы конфигурации для настройки проекта и тестов.

- **`requirements.txt`**: Список зависимостей Python, необходимых для работы приложения.

