# Сервис для сбора данных и информирования пользователей.

*Данный продукт был разработан в рамках Онлайн-хакатона #2*

## 1. Проблема
В данный момент в российской интернет-сфере имеются сложности в работе с интернационализированными доменами и почтовыми адресами. Это может стать сложностью для менее продвинутых пользователей, например для пожилых людей, которые не умеют читать и писать по-английски. Тем не менее, они нуждаются в интернет-сервисах наравне с другими пользователями. Наше решение дает возможность использовать удобный для них язык, что позволяет снизить порог входа для пользователей и значительно расширить аудиторию.

## 2. Спецификация
В области интернационализированных доменных имен есть понятие Universal Acceptance. Это список функций, которые должно поддерживать ПО для корректной работы с доменными именами, а именно:
- Принятие
- Проверка
- Хранение
- Обработка
- Отображение

Соответственно нашей целью стояла разработка такого продукта, который будет подходить под все вышеперечисленные требованя.

## 3. Настройка среды
Все необходимые библиотеки хранятся в файле `requirements.txt`. Установить их можно командой `pip install -r requirements.txt`

## 4. Прочие приготовления
Перед запуском сервера можно создать шаблон базы данных, запустив файл `prepare_test_database.py`. Эта программа создаст пробную базу данных, содержащую админа и несколько пользователей.

## 5. Запуск сервера
Основной файл программы лежит в файле `server.py`. Запустив его командой `python server.py` Вы развернете веб-сервер, доступный по адресу `127.0.0.1:5000`. 

## 6. Доступные функции
На данный момент доступны следующии функции и страницы:

### 1) Главная страница с новостной лентой и формой входа
![alt text](https://github.com/mikgorn/hack2dns/blob/master/screenshots/Screenshot_28.png?raw=true)

### 2) Регистрация новых пользователей
![alt text](https://github.com/mikgorn/hack2dns/blob/master/screenshots/Screenshot_28.png?raw=true)

### 3) Личный кабинет с персонализированным расписанием
![alt text](https://github.com/mikgorn/hack2dns/blob/master/screenshots/Screenshot_28.png?raw=true)

### 4) Админская панель управления с функцией рассылки персонализированных сообщений
![alt text](https://github.com/mikgorn/hack2dns/blob/master/screenshots/Screenshot_28.png?raw=true)
