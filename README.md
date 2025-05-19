1. Клонируйте репозиторий:
   # https://github.com/Said-Ahmed/exchange.git
   
2. Создайте и активируйте виртуального окружения
   # python -m venv venv
  
   # Linux/MacOS
   # source venv/bin/activate
  
   # Windows
   # .\venv\Scripts\activate

3. Установите зависимости
  # pip install -r requirements.txt

4. Перейдите в директорию src проекта
   # cd src

5. Произведиет миграции
   # python manage.py makemigrations
   # python manage.py migrate

6. Выполните тесты
   # Тесты приложения ads
   # pytest ads/tests.py -v

   # Тесты приложения proposals
   # pytest proposals/tests.py -v

8. Запустите сервер
   # python manage.py runserver
