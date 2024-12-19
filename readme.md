# ServiceDesk

## Описание проекта
ServiceDesk — это приложение, предназначенное для работы с пользовательскими обращениями. Оно позволяет пользователям отправлять сообщения по электронной почте, а операторам — управлять этими обращениями через API.

## Стек технологий
- **Backend**: FastAPI
- **База данных**: PostgreSQL

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/davidradetskiy/foxford.git
   cd foxford
   ```

2. Запустите docker-comopose:
   ```bash
   docker-compose up --build
   ```
3. Откройте браузер и перейдите по адресу:
    ```bash
    http://localhost:8000/docs
    ```

## Использование

### Моменты
    при старте приложения создается пользователи с кодом 0000 и 1111
    это условные наши операторы
    код нужен для отправки сообщений и закрытия тикета, услованая авторизация(б-безопасность)

    при отправке сообщения на email testtfoxford@yandex.ru, создается обращение в базе данных
    и автоматически отправляется ответ пользователю
    даже если сообщение попадет в спам, то оно все равно будет создано в базе данных(воу полегче)

    опрашиваем почту каждые 30 секунд, на проверку новых сообщений

### Тесты
    тесты не писал, т.к нет времени

PS: если смотря на код и архитектуру у вас появляются негативные эмоции и вам плохо станет, то это нормально,
я писал проект в перерыве между работой(времени по минимуму)