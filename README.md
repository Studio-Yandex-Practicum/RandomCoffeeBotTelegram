# RandomCoffeeBotTelegram
Random Coffee bot for the Telegram

#### Проект телеграм-бота, который предоставляет возможность пообщаться с IT-специалистами - выпускниками разных IT направлений практикума.

# Содержание


1. [БРИФ](docs/materials/briff.md)

   1.1. [Инструкции и ритуалы на проекте](docs/materials/instructions.md)

   1.2. [ER - диаграмма сущностей](docs/RandomCoffeeModelsER.jpg)

   1.3. [Feature list проекта](docs/materials/featch_list.md)

   1.4. [Диаграмма логики работы бота](docs/Diagramm_of_bot_logic.jpg)

2. [О проекте](#project)

    2.1. [Структура проекта](#structure)

    2.2. [Используемых технологий в проекте](#technologies-project)

3. [Подготовка к запуску](#start)

    3.1. [Правила работы с git](#git)

    3.2. [Настройка poetry](#poetry)

    3.3. [Настройка pre-commit](#pre-commit)

    3.4. [Настройка переменных окружения](#env)

4. [Запуск бота](#run-bot)

    4.1. [Запуск проекта локально](#run-local)

    4.2. [Запуск в Docker](#run-docker)

5. [Требования к тестам](#test-bot)

<br><br>

# 2. О проекте <a id="project"></a>

## 2.1 Структура проекта <a id="structure"></a>

| Имя  | Описание |
| ------------- | ------------- |
| infrastructure | Docker-compose файлы для запуска проекта с помощью Docker |
| src | к описанию этой папки стоит вернутся когда рефакторинг закончим |

## 2.2 Используемые технологии в проекте<a id="technologies-project"></a>:

[![Python][Python-badge]][Python-url]
[![Poetry][Poetry-badge]][Poetry-url]
[![Pre-commit][Pre-commit-badge]][Pre-commit-url]
[![Python-telegram-bot][Python-telegram-bot-badge]][Python-telegram-bot-url]
[![Django][Django-badge]][Django-url]
[![Docker][Docker-badge]][Docker-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Redis][Redis-badge]][Redis-url]

# 3. Подготовка к запуску <a id="start"></a>

Примечание: для работы над проектом необходим Python не ниже версии 3.11.
Также необходимо установить Poetry (не ниже 1.5.0) и pre-commit.

## 3.1. Правила работы с git (как делать коммиты и pull request-ы)<a id="git"></a>:

1. Две основные ветки: `master` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. Создавая новую ветку, наследуйтесь от ветки `develop`
4. В `master` находится только production-ready код (CI/CD)
5. Правила именования веток
   - весь новый функционал — `feature/название-функционала`
   - исправление ошибок — `bugfix/название-багфикса`
6. Пушим свою ветку в репозиторий и открываем Pull Request

## 3.2. Poetry (инструмент для работы с виртуальным окружением и сборки пакетов)<a id="poetry"></a>:


Poetry - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>

<details>
 <summary>
 Как скачать и установить?
 </summary>

### Установка:

Установите poetry, не ниже версии 1.5.0 следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
<details>
 <summary>
 Команды для установки:
 </summary>

Если у Вас уже установлен менеджер пакетов pip, то можно установить командой:

> *pip install poetry==1.5.0*

Если по каким-то причинам через pip не устанавливается,
то для UNIX-систем и Bash on Windows вводим в консоль следующую команду:

> *curl -sSL https://install.python-poetry.org | python -*

Для WINDOWS PowerShell:

> *(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -*

</details>
<br>
После установки перезапустите оболочку и введите команду

> poetry --version

Если установка прошла успешно, вы получите ответ в формате

> Poetry (version 1.5.0)

P.S.: Если при попытке проверить версию возникает ошибка об отсутствии исполняемого файла
(poetry), необходимо после установки добавить его в Path Вашей системы
(пути указаны по ссылке на официальную инструкцию по установке чуть выше.)

Для дальнейшей работы введите команду:

> poetry config virtualenvs.in-project true

Выполнение данной команды необходимо для создания виртуального окружения в
папке проекта.

После предыдущей команды создадим виртуальное окружение нашего проекта с
помощью команды:

> poetry install

Результатом выполнения команды станет создание в корне проекта папки .venv.
Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)
и pyproject.toml

Для добавления новой зависимости в окружение необходимо выполнить команду

> poetry add <package_name>

_Пример использования:_

> poetry add starlette

Также poetry позволяет разделять зависимости необходимые для разработки, от
основных.
Для добавления зависимости необходимой для разработки и тестирования необходимо
добавить флаг ***--dev***

> poetry add <package_name> --dev

_Пример использования:_

> poetry add pytest --dev

</details>

<details>
 <summary>
 Порядок работы после настройки
 </summary>

<br>

Чтобы активировать виртуальное окружение, введите команду:

> poetry shell

Существует возможность запуска скриптов и команд с помощью команды без
активации окружения:

> poetry run <script_name>.py

_Примеры:_

> poetry run python script_name>.py
>
> poetry run pytest
>
> poetry run black

Порядок работы в оболочке не меняется. Пример команды для Win:

> python src\run_bot.py

Доступен стандартный метод работы с активацией окружения в терминале с помощью команд:

Для WINDOWS:

> source .venv/Scripts/activate

Для UNIX:

> source .venv/bin/activate

</details>

В этом разделе представлены наиболее часто используемые команды.
Подробнее: https://python-poetry.org/docs/cli/

#### Активировать виртуальное окружение
```shell
poetry shell
```

#### Добавить зависимость
```shell
poetry add <package_name>
```

#### Обновить зависимости
```shell
poetry update
```
## 3.3. Pre-commit (инструмент автоматического запуска различных проверок перед выполнением коммита)<a id="pre-commit"></a>:

<details>
 <summary>
 Настройка pre-commit
 </summary>
<br>
1. Убедиться, что pre-comit установлен:

   ```shell
   pre-commit --version
   ```
2. Настроить git hook скрипт:

   ```shell
   pre-commit install
   ```

Далее при каждом коммите у вас будет происходить автоматическая проверка
линтером, а так же будет происходить автоматическое приведение к единому стилю.
</details>

## 3.4. Настройка переменных окружения <a id="env"></a>

Перед запуском проекта необходимо создать копию файла
```.env.example```, назвав его ```.env``` и установить значение токена бота, базы данных почты и тд.

# 4. Запуск бота <a id="run-bot"></a>

### Сейчас возможен запуск бота только в режиме `polling`.<br>

## 4.1. Запуск проекта локально <a id="run-local"></a>

В локальной разработке предусмотрено использование персистентности бота в файле pickle. (Хранится в корневой директории `local_persistence`, если необходимо сбросить состояние бота - необоходимо удалить файл.)


Запуск бота в локальной среде рекомендуется выполнять с помощью команд:

запуск django-приложения (Без БД) вместе с ботом для локальной разработки:
```shell
# Перейти в директорию c кодовой базой проекта src/, где лежит manage.py
cd src/

# Запустить веб-сервер командой
poetry run uvicorn core.asgi:application --reload
```

Базовая команда для запуска БД, миграций, бота и джанго:
```shell
make bot-init
```

запуск бота и контейнера PostgreSQL с существующими данными в БД:
```shell
make bot-existing-db
```

запуск контейнера с PostgreSQL:
```shell
make start-db
```

остановка контейнера с PostgreSQL:
```shell
make stop-db
```

остановка контейнера с PostgreSQL и удаление базы данных:
```shell
make clear-db
```

наполнение PostgreSQL тестовыми данными:
```shell
# Создание тестовых профилей IT-специалистов
make create-itspecialist amount=3
```

```shell
# Создание тестовых профилей рекрутеров
make create-recruiter amount=3
```

```shell
# Создание тестовых пар IT-специалист-рекрутер *временами ругается на уникальность ID
make create-pair amount=3
```

## 4.2. Запуск проекта в Docker <a id="run-docker"></a>

1. Запуск ```Redis``` (работает в режиме ```redis=True```) - убедитесь, что в .env установлено необходимое значение

2. Убедиться, что ```docker compose``` установлен:
   ```docker compose --version```
3. Из папки ```infra/dev/``` запустить ```docker-compose```:
   ```shell
   sudo docker-compose -f docker-compose.stage.yaml up
   ```

# 5. Требования к тестам <a id="test-bot"></a>

#### Запуск тестов
Все тесты запускаются командой:
   ```shell
   pytest
   ```

   Или

   ```shell
   make run_tests
   ```
Выборочно тесты запускаются с указанием выбранного файла:
   ```shell
   pytest test_start.py
   ```

   Или

   ```shell
   make run_unit_tests
   ```

#### Написание тестов
Для написания тестов используется pytest.
Фикстуры хранятся в файле tests/conftest.py
Основные тесты бота хранятся в директории tests.
В зависимости от функционала тестов можно добавлять файлы тестов.
Файлы тестов должны начинаться с "test_".

#### Что необходимо тестировать
Разработчик самостоятельно определяет функционал, который будет покрыт
данными. Но, как правило, рекомендуется тестировать все написанные
самостоятельно основные функции бота, функции отправки и получения сообщений,
функции перенаправления на сторонние или внутренние ресурсы.

#### Рекомендации к написанию кода [Codestyle](docs/codestyle.md)


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/downloads/release/python-3110/
[Python-badge]: https://img.shields.io/badge/python-v3.11-yellow?style=for-the-badge&logo=python

[Poetry-url]: https://python-poetry.org/
[Poetry-badge]: https://img.shields.io/badge/poetry-blue?style=for-the-badge&logo=poetry

[Pre-commit-url]: https://pre-commit.com/
[Pre-commit-badge]: https://img.shields.io/badge/Pre--commit-teal?style=for-the-badge&logo=precommit

[Python-telegram-bot-url]: https://docs.python-telegram-bot.org/en/v20.6/
[Python-telegram-bot-badge]: https://img.shields.io/badge/python--telegram--bot-v20.6-red?style=for-the-badge

[Django-url]: https://docs.djangoproject.com/en/4.2/releases/4.2.6/
[Django-badge]: https://img.shields.io/badge/Django-v4.2.6-008000?logo=django&style=for-the-badge

[Docker-url]: https://www.docker.com/
[Docker-badge]: https://img.shields.io/badge/docker-red?style=for-the-badge&logo=docker

[Postgres-url]: https://www.postgresql.org/
[Postgres-badge]: https://img.shields.io/badge/postgresql-gray?style=for-the-badge&logo=postgresql

[Redis-url]: https://redis.io/
[Redis-badge]: https://img.shields.io/badge/redis-black?style=for-the-badge&logo=redis
