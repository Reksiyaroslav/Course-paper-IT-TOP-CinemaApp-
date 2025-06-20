# Course-paper-IT-TOP-CinemaApp-
Создание сайта на html/css и python Litestar
Создана работа для  курсовой работы .
2 cd CinimaApp
3.Создайте и активируйте виртуальное окружение:
python -m venv .venv
.venv\Scripts\activate   
4. Установка зависимости 
pip install -r requirements.txt



1.Создайте файл .env на основе .env.example и укажите необходимые переменные окружения.
2. Создание образа на в docker:
docker compose build
3.Запустите приложение:

uvicorn app.run:app --host 0.0.0.0 --port 90
или litestar run .
После перехода по ссылке добавляете /schema , а  если нужны ручки добавте после schema swagger

Если не хотите делать docker то можно изменить env:
PG_PASSWORD=youpassword
PG_DATABASE = youdb 
и выполните 3 пункт должно будет работ проект.   