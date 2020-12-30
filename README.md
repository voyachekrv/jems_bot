JEMS Bot
------
Telegram-бот для напоминаний в чате проекта JEMS.

###Установка

####Установка окружения
Требуемая версия Python - 3.8 и выше.\
Для установки необходимо убедиться, что в системе установлена система управления пакетами pip.
Проверка осуществляется следующей командой: `pip3 --version`

Установка pip на Ubuntu 20.04:
````shell
$ sudo apt update
$ sudo apt install python3-pip
````

####Установка зависимостей
После загрузки исходников для установки в систему необходимых зависимостей нужно выполнить команду, находясь в директории с исходным кодом бота:
````shell
$ pip3 install -r requirements.txt
````
###Запуск
####Запуск и выключение программы
Запуск производится посредством команды в директории, в которой расположены исходники
````shell
$ python3 main.py
````

При первом запуске программы в консоль необходимо будет ввести API-токен бота, после чего он сохранится в файл переменных окружения:
````dotenv
API_TOKEN=<YOUR_TOKEN_HERE>
````

Для выключения бота необходимо прервать процесс посредством нажатия `Ctrl + C`

####Запуск бота в Telegram

Для запуска бота в чате необходимо добавить его в соответствующий чат по адресу
[**@jems_notification_bot**](https://t.me/jems_notification_bot), после чего активировать бота по команде `/start` - бот начнёт функционировать.\
При повторном запуске бота на сервере необходимо перезапустить бота командой `/start` в чате.

