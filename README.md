# Web-server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Данный проект - это асинхронный веб-сервер.

## О проекте
Асинхронный веб-сервер на Python с функциями: проксирование, виртуальные хосты, автоматическая индексация файлов в каталоге и логирование запросов в формате nginx/apache. Создан на asyncio для высокой производительности.




### Основные возможности
* Автоматическая индексация файлов
* Асинхронность
* Proxy pass
* Виртуальные серверы
* Логирование запросов в стиле Nginx/Apache
* SSL


<details>
<ol>
    <li><a href="#о-проекте">О проекте</a></li>
    <li><a href="#установка">Установка</a></li>
    <li><a href="#использование">Использование</a></li>
    <li><a href="#конфигурация">Конфигурация</a></li>
    <li><a href="#лицензия">Лицензия</a></li>
    <li><a href="#контакты">Контакты</a></li>
  </ol>
</details>


## Установка
Для запуска проекта вам понадобятся:
* Python 3.9+
* pip

Следуйте этим шагам для установки:

1. Клонируйте репозиторий
    ```bash
    git clone https://github.com/s1nator/web-server-university_project-.git
    ```
2. Перейдите в папку проекта
   ```bash
   cd web-server-university_project-
   ```
3. Установите зависимости
   ```bash
   pip install -r requirements.txt
   ```
   
## Использование
```bash
  python3 web_server.py
```

## Конфигурация

Проект настраивается через файл `config.yaml`. Пример файла и описание параметров:

```yaml
# config.yaml
# все данные для веб-сервера
database:
  # хост на котором будет располагаться веб-сервер
  host: 
  # порт на котором будет располагаться веб-сервер
  port: 
  # хост для подключения к другому серверу через веб-сервер
  proxy_pass_host: 
  # порт для подключения к другому серверу через веб-сервер
  proxy_pass_port:
  # путь к рабочей директории веб-сервера
  working_dir: 
  # дата удаления журнала логов
  date_logs_delete: 
```

## Лицензия

Распространяется под лицензией MIT. Смотрите `LICENSE.txt` для получения дополнительной информации.

## Контакты

s1nator - [@s1nator](https://github.com/s1nator) - denisbrevnov2006@gmail.com

Ссылка на проект: [https://github.com/s1nator/web-server-university_project-#](https://github.com/s1nator/web-server-university_project-#)

