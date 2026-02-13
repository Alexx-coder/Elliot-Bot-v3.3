import os
import hashlib
import datetime
import time
import random
import string
import re, json
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(SCRIPT_DIR, "elliot_users_3.2.json")

print(f"Бот запущен из папки: {SCRIPT_DIR}")
print(f"Файл базы данных будет: {USERS_FILE}")
print(f"Ты в папке: {Path.cwd()}")

# Загружаем базу данных
try:
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        USER_DATABASE = json.load(f)
except:
    # Если файла нет - создаем пустую базу
    USER_DATABASE = {}
    print("Файл базы данных не найден, создаю новый...")

def simple_check_user(username, password):
    """Просто проверяет пользователя"""
    for user_id, user in USER_DATABASE.items():
        if user['login'] == username:
            # Проверяем пароль
            if user['password'] == password:
                return user_id
            # Или хэшированный пароль
            if user['password'] == hashlib.sha256(password.encode()).hexdigest():
                return user_id
    return None

#Время для функций
time_now = datetime.datetime.now()
year_now = time_now.year
month_now = time_now.month
day_now = time_now.day
hour_now = time_now.hour
minute_now = time_now.minute
second_now = time_now.second

#Доброе утро , Добрый день , Добрый вечер или Доброй ночи
if 5 <= hour_now < 12:
    greeting = "Доброе утро"
elif 12 <= hour_now < 17:
    greeting = "Добрый день"
elif 17 <= hour_now < 23:
    greeting = "Добрый вечер"
else:
    greeting = "Доброй ночи"

#Нормы паролей Elliot_bot
Elliot_pw_worst = "Данный пароль не рекомендуется для использования"
Elliot_pw_middle = "Данный пароль соотвествует минимальным требованиям для постоянного использования"
Elliot_pw_normal = "Данный пароль рекомендуется для постоянного использования"


#Команды для бота
version_bot = "v3.3"
data_version = "13.02.2026"



def hash_password(password):
    """
    Простое хэширование для учебного проекта.
    В реальном проекте используй:              
    import secrets
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest()
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email_user):
    """Простая проверка email"""
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email_user))

# Класс Ошибок для бота
class ElliotBotError(Exception):
    def __init__(self, message="Возникла ошибка"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[ElliotBot Error] {self.message}"


class InvalidCommandError(ElliotBotError):
    def __init__(self, command):
        super().__init__(f"Неизвестная команда боту команда: '{command}'")


class NotFoundFunctionError(ElliotBotError):
    def __init__(self, function_num):
        super().__init__(f"Функция {function_num} не найдена")


class ValidationError(ElliotBotError):
    def __init__(self, value, expected):
        super().__init__(f"Написано некорректно: '{value}'. Ожидалось : {expected}")


class MathError(ElliotBotError):
    def __init__(self, operation, details=""):
        message = f"Возникла ошибка в математической операции '{operation}'"
        if details:
            message += f": {details}"
        super().__init__(message)



def save_user(user_id, login, password, is_admin=False):
    global USER_DATABASE
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    # Хэшируем пароль перед сохранением
    hashed_password = hash_password(password)
    
    users[user_id] = {
        "login": login,
        "password": hashed_password,
        "commands": {},
        "admin": is_admin
    }
    
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    USER_DATABASE = users
    
    print(f"Пользователь {login} сохранён с ID: {user_id}")

def get_new_user_name_id():
    global USER_DATABASE
    return str(len(USER_DATABASE) + 1)

def login_user():
    global USER_DATABASE
    
    if not USER_DATABASE:
        print("В базе данных не найдено. Сначала зарегистрируйтесь.")
        return None
    
    print(" ВХОД В СИСТЕМУ ")
    
    for попытка in range(3):
        print(f"Попытка {попытка + 1} из 3")
        введенный_логин = input("Логин: ")
        password_user_name = input("Пароль: ")
        
        # Хэшируем введенный пароль для сравнения
        hashed_password = hash_password(password_user_name)
        
        for user_id, user_data in USER_DATABASE.items():
            if user_data["login"] == введенный_логин and user_data["password"] == hashed_password:
                print(f"Успешный вход!\n{greeting}, {введенный_логин}!")
                
                if user_data.get("admin"):
                    print("Вы вошли как Администратор Бота")
                else:  
                    print("Вы вошли как обычный пользователь")
                
                return {
                    "id": user_id,
                    "login": введенный_логин,
                    "is_admin": user_data.get("admin", False)
                }
        
        print("Неверный логин или пароль!")
    
    print("Слишком много неудачных попыток.")
    return None



# Основной код
print("Привет, я Бот Эллиот")

while True:
    print("ВХОД / РЕГИСТРАЦИЯ")
    print("1 - Вход в аккаунт")
    print("2 - Регистрация")
    print("3 - Выход")
    
    try:
        выбор = input("Выберите (1-3): ").strip()
        
        if выбор not in ["1", "2", "3"]:
            raise NotFoundFunctionError(выбор)
        
        if выбор == "1":
            user_data = login_user()
            if user_data:
                user_name = user_data["login"]
                user_name_id = user_data["id"]
                is_admin = user_data["is_admin"]
                
                сейчас = datetime.datetime.now()
                print(f"\nСегодня {сейчас.day}.{сейчас.month}.{сейчас.year}. \nДанный день идёт уже {сейчас.hour:02}:{сейчас.minute:02}:{сейчас.second:02}")
                
                if сейчас.month == 12 and сейчас.day == 31:
                    print(f"Поздравляю вас с Новым Годом {user_name}!") 
                else:
                    next_year = сейчас.year + 1
                    new_year = datetime.datetime(next_year, 1, 1)
                    time_left = new_year - сейчас

                    days_left = time_left.days
                    hours_left = time_left.seconds // 3600
                    minutes_left = (time_left.seconds % 3600) // 60
                    seconds_left = time_left.seconds % 60

                    print(f"До Нового года осталось: {days_left} дней, {hours_left} часов, {minutes_left} минут, {seconds_left} секунд")

                    if month_now == 12:
                       if day_now == 31:
                        print("С новым годом!")
                        print(f"От Alexx-coder или alex: Привет {user_name}! Хочу тебя поздравить с Новым годом!")
                       elif day_now == 30: 
                        print("Завтра последний день в году!")
                       elif day_now == 29:
                           print("Завтра предпоследний день!")
                       elif day_now >= 20:
                        print("Скоро Новый год!")
                break
            else:
                print("Вход не удался. Попробуйте снова или зарегистрируйтесь.")
        elif выбор == "2":
            print("РЕГИСТРАЦИЯ")
            print("Создайте имя пользователю:")
            user_name = input('>')

            while True:
               print("Теперь пароль пользователю:")
               password_user_name = input('>')
               print("\n")

               if len(password_user_name) <= 5:
                 print("Пароль короткий, надо придерживаться минимум норме Elliot_pw_worst!")
                 print("О нормах паролях в README.md(Примечания)")    
                 print("Придется вам ввести более длинный пароль(минимум 6 символов)...")    
                 continue
               if len(password_user_name) >= 6 and len(password_user_name) <= 7:
                 print(f"{Elliot_pw_worst}")
                 print("О нормах паролях в README.md(Примечания)")
                 break
               elif len(password_user_name) >= 8 and len(password_user_name) <= 9:
                 print(f"{Elliot_pw_middle}")
                 print("О нормах паролях в README.md(Примечания)")
                 break
               elif len(password_user_name) >= 10:
                 print(f"{Elliot_pw_normal}")
                 print("О нормах паролях в README.md(Примечания)")
                 break

            print("\n")


            user_name_id = get_new_user_name_id()
            save_user(user_name_id, user_name, password_user_name)
            
            print(f"Вы зарегистрировались, теперь {user_name} вы есть в Бот Эллиоте")
            print(f"Ваш уникальный айди: {user_name_id}")
            
            user_data = {
                "id": user_name_id,
                "login": user_name,
                "is_admin": False
            }
            is_admin = False
            break
        
        elif выбор == "3":
            print("До свидания!")
            exit()
    
    except NotFoundFunctionError as elliot_bot_registr:
        print(f"Ошибка: {elliot_bot_registr}")
        print("Пожалуйста, выберите 1, 2 или 3")



функции_бота = {
    "1": {
        "название": "Математика",
        "описание": "Ответы на математические вопросы"
    },
    "2": {
        "название": "Python помощь",
        "описание": "Помощь с кодом(Python)"
    },
    "3": {
        "название": "Фишки ПК",
        "описание": "Фишки для компьютера/ноутбука"
    },
    "4": {
        "название": "Командная строка",
        "описание": "Фишки с командной строкой"
    },
    "5": {
        "название": "Установка ОС",
        "описание": "Установка Windows/Linux"
    },
    "6":{
        "название": "Генератор паролей",
        "описание": "Генерирует разные пароли"
    },
    "7":{
        "название": "Параметры",
        "описание": "Данные пользователя и настройки аккаунта"
    },
    "8":{
        "название": "Свзяь с разработчиком",
        "описание": "Контакты и обратня связь"
    },
    "9":{
        "название": "Команды",
        "описание": "Разные команды для бота(/)"
    },
    "10":{
        "название": "Терминал",
        "описание": "Возможность написания команд для бота(/)"
    },
    "11":{
        "название": "Проверка",
        "описание": "Проверка почт и номеров телефонов"

    }

    
}

while True:
    try:
        рассказать_о_функциях = input("Рассказать о моих функциях (да/нет): ").strip().lower()
        
        if рассказать_о_функциях not in ['да', 'нет']:
            raise ValidationError(рассказать_о_функциях, "'да' или 'нет'")
        
        break
        
    except ValidationError as elliot_bot_error_1:
        print(f" {elliot_bot_error_1}")
        print("Пожалуйста, введите 'да' или 'нет'")

if рассказать_о_функциях == "нет":
    print("Тогда ладно")
    print("Но знай: я могу рассказать о функциях")

elif рассказать_о_функциях == "да":
    print("Сейчас же расскажу!")
    print("Вот мои функции:")
    for номер, данные in функции_бота.items():
        print(f"{номер}- {данные['описание']}")

while True:
    try:
        выбрать_функцию = input("Выбрать функцию 1-11: ")

        if выбрать_функцию == "1":
            print("Математика:")

            def получить_число(запрос):
                while True:
                    try:
                        ввести_число = input(запрос).strip()
                        if '.' in ввести_число:
                            return float(ввести_число)
                        else:
                            return int(ввести_число)
                    except:
                        print("Надо ввести число! Попробуйте снова:")

            while True:
                print("Выберите операцию:")
                print("1- Сложение")
                print("2- Вычитание")
                print("3- Умножение")
                print("4- Деление")
                print("5- Ничего: выход из функции")

                try:
                    математическая_операция = input("Выбирай: (1-5):").strip()

                    if математическая_операция == "5":
                        print("Выхожу из данной функции")
                        break

                    if математическая_операция not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(математическая_операция)

                    число_1 = получить_число("Это первое число: ")
                    число_2 = получить_число("Это второе число: ")

                    if математическая_операция == "1":
                        результат = число_1 + число_2
                        знак = "+"
                    elif математическая_операция == "2":
                        результат = число_1 - число_2
                        знак = "-"
                    elif математическая_операция == "3":
                        результат = число_1 * число_2
                        знак = "*"
                    elif математическая_операция == "4":
                        if число_2 == 0:
                            raise MathError("Делить на ноль нельзя!")
                        результат = число_1 / число_2
                        знак = "÷"

                    print(f"Результат: {число_1} {знак} {число_2} = {результат}")

                    while True:
                        ещё_раз_посчитать = input("Хотите ещё раз посчитаю? (да/нет): ").strip().lower()
                        if ещё_раз_посчитать in ["да", "нет"]:
                            break
                        print("Напиши 'да' или 'нет'")

                    if ещё_раз_посчитать == "нет":
                        print("Заканчиваю данную функцию")
                        break

                except NotFoundFunctionError as elliot_bot_error_1:
                    print(f"Ошибка: {elliot_bot_error_1}")
                except MathError as elliot_bot_error_1:
                    print(f" {elliot_bot_error_1}")
                except Exception as elliot_bot_error_1:
                    print(f"Что-то пошло не так: {elliot_bot_error_1}")

        elif выбрать_функцию == "2":
            print("Помощь с кодом(Python):")

            while True:
                print("Выбирай:")
                print("1- Основы Python")
                print("2- Примеры кода")
                print("3- Ошибки новичков")
                print("4- Советы")
                print("5- Ничего:выход из функции")

                try:
                    выбор_py = input("Твой выбор (1-5):").strip()

                    if выбор_py == "5":
                        print("Выхожу из функции")
                        break

                    if выбор_py not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_py)

                    if выбор_py == "1":
                        print("Основы Python ")
                        print("Переменные:")
                        print("x = 10")
                        print('имя = "Алекс"')
                        print("список = [1, 2, 3]")
                        print("Условия:")
                        print("if возраст >= 18:")
                        print("    print('Взрослый')")
                        print("else:")
                        print("    print('Ребёнок')")
                        print("Циклы:")
                        print("for i in range(3):")
                        print("    print(i)")
                        print("Функции:")
                        print("def приветствие(имя):")
                        print('    print(f"Привет, {имя}!")')
                        print('приветствие("Алекс")')

                    elif выбор_py == "2":
                        print("Примеры кода ")
                        print("Работа со списком:")
                        print("числа = [5, 2, 8, 1]")
                        print('print(f"Список: {числа}")')
                        print('print(f"Сумма: {sum(числа)}")')
                        print('print(f"Отсортированный: {sorted(числа)}")')
                        print("Чтение файла:")
                        print("with open('test.txt', 'w') as f:")
                        print('    f.write("Привет, мир!")')
                        print("with open('test.txt', 'r') as f:")
                        print("    содержимое = f.read()")
                        print("    print(содержимое)")

                    elif выбор_py == "3":
                        print("Ошибки новичков ")
                        print("1. Забыл двоеточие:")
                        print("   if x > 5  # ОШИБКА")
                        print("   if x > 5:  # ПРАВИЛЬНО")
                        print("2. Неправильные отступы:")
                        print("   if x > 5:")
                        print("   print('Привет')  # ОШИБКА")
                        print("   if x > 5:")
                        print("       print('Привет')  # ПРАВИЛЬНО")
                        print("3. Деление на ноль:")
                        print("   print(10 / 0)  # ОШИБКА")
                        print("   if b != 0:")
                        print("       print(a / b)  # ПРАВИЛЬНО")

                    elif выбор_py == "4":
                        print("Советы ")
                        print("1. Комментируй код:")
                        print("   # Это помогает понять код")
                        print("   x = 5  # количество попыток")
                        print("2. Используй понятные имена:")
                        print("   плохо: a = 10")
                        print("   хорошо: возраст = 10")
                        print("3. Проверяй по частям:")
                        print("   Не пиши всю программу сразу")
                        print("   Проверяй каждую часть отдельно")
                        print("4.Читай ошибки:")
                        print("   Python сам говорит где ошибка")

                    input("Нажмите Enter чтобы продолжить...")

                except NotFoundFunctionError as elliot_bot_error_2:
                    print(f"Ошибка: {elliot_bot_error_2}")
                    print("Выбери 1, 2, 3 или 4")

                while True:
                    ещё = input("Ещё про Python? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")

                if ещё == "нет":
                    print("Выхожу из помощи по Python...")
                    break

        elif выбрать_функцию == "3":
            print("/nФишки для ПК/Ноутбука:")

            while True:
                print("Что вы выберите?")
                print("1- Ускорение Windows")
                print("2- Горячие клавиши")
                print("3- Очистка системы")
                print("4- Безопасность пользователя")
                print("5- Ничего: выход из функции")

                try:
                    выбор_фишек = input("Выберите: 1-5:")

                    if выбор_фишек == "5":
                        print("Выхожу из данной функции")
                        break

                    if выбор_фишек not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_фишек)
                    
                    if выбор_фишек == "1":
                        print("Ускорение Windows ")
                        print("1./nОтключи ненужные службы:")
                        print("   Win+R → services.msc")
                        print("   Отключи:")
                        print("   - Windows Search")
                        print("   - Xbox Live Auth Manager")
                        print("   - Printer Spooler (если нет принтера)")
                        
                        print("2.Автозагрузка:")
                        print("   Ctrl+Shift+Esc → Автозагрузка")
                        print("   Отключи ненужные программы")
                        
                        print("3.Визуальные эффекты:")
                        print("   Win+Pause → Доп. параметры")
                        print("   Быстродействие → Параметры")
                        print("   Выбери 'Обеспечить лучший быстродействие'")
                    
                    elif выбор_фишек == "2":
                        print("Горячие клавиши ")
                        print("Win + D - Рабочий стол")
                        print("Win + E - Проводник")
                        print("Win + L - Заблокировать ПК")
                        print("Win + Shift + S - Скриншот области")
                        print("Ctrl + Shift + Esc - Диспетчер задач")
                        print("Alt + Tab - Переключение окон")
                        print("Win + Tab - Предпросмотр окон")
                        print("Ctrl + C / V - Копировать/Вставить")
                        print("Ctrl + Z - Отменить")
                        print("Ctrl + Shift + N - Новая папка")
                    
                    elif выбор_фишек == "3":
                        print("Очистка системы ")
                        print("1.Очистка диска:")
                        print("   Win+R → cleanmgr → Enter")
                        print("   Выбери диск C:")
                        print("   Отметь все галочки → ОК")
                        
                        print("2.Удаление временных файлов:")
                        print("   Win+R → %temp% → Enter")
                        print("   Ctrl+A → Delete")
                        
                        print("3nОчистка кэша:")
                        print("   Браузер Chrome:")
                        print("   Ctrl+Shift+Delete → Выбери 'Все время'")
                        print("   Отметь: Кэш, Куки → Удалить")
                        
                        print("4.CCleaner (программа):")
                        print("   Бесплатная версия")
                        print("   Сканировать → Очистить")
                    
                    elif выбор_фишек == "4":
                        print("Безопасность ")
                        print("1./nАнтивирус:")
                        print("   Windows Defender (встроенный)")
                        print("   Или: Kaspersky Free, Avast Free")
                        
                        print("2.Брандмауэр:")
                        print("   Панель управления → Брандмауэр")
                        print("   Включи входящие/исходящие правила")
                        
                        print("3.Обновления:")
                        print("   Win+I → Обновление и безопасность")
                        print("   Проверь наличие обновлений")
                        
                        print("4.Резервное копирование:")
                        print("   Win+I → Обновление → Резервное копирование")
                        print("   Добавь диск → Включи")
                        
                        print("5.Пароли:")
                        print("   Используй менеджер паролей:")
                        print("   - Bitwarden (бесплатный)")
                        print("   - LastPass (бесплатный)")
                        print("   Не используй один пароль везде!")
                    
                    input("Нажми Enter чтобы продолжить...")
                    
                except NotFoundFunctionError as elliot_bot_error_3:
                    print(f"Ошибка: {elliot_bot_error_3}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё советы по компьютеру? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Заканчиваю компьютерные советы...")
                    break

        elif выбрать_функцию == "4":
            print("Фишки с командной строкой:")

            while True:
                print("Что интересует?")
                print("1- Windows CMD")
                print("2- PowerShell")
                print("3- Linux/Mac Terminal")
                print("4- Полезные команды")
                print("5- Ничего: выход из функции")
                
                try:
                    выбор_фишек__с_командной_строкой = input("Твой выбор (1-5): ").strip()
                    
                    if выбор_фишек__с_командной_строкой == "5":
                        print("Выхожу из командной строки...")
                        break
                    
                    if выбор_фишек__с_командной_строкой not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_фишек__с_командной_строкой)
                    
                    if выбор_фишек__с_командной_строкой == "1":
                        print("WINDOWS CMD ")
                        print("Основные команды:")
                        print("dir           - список файлов в папке")
                        print("cd folder     - войти в папку")
                        print("cd ..         - выйти на уровень выше")
                        print("mkdir folder  - создать папку")
                        print("rmdir folder  - удалить папку")
                        print("del file.txt  - удалить файл")
                        print("copy a.txt b.txt - копировать файл")
                        print("move a.txt folder/ - переместить файл")
                        print("type file.txt - показать содержимое файла")
                        print("cls           - очистить экран")
                        print("help          - помощь по командам")
                        print("Сетевые команды:")
                        print("ipconfig      - информация о сети")
                        print("ping google.com - проверить соединение")
                        print("tracert google.com - путь до сайта")
                        print("netstat -an   - активные соединения")
                    
                    elif выбор_фишек__с_командной_строкой == "2":
                        print("POWERSHELL ")
                        print("Основные команды:")
                        print("Get-ChildItem       - список файлов (как dir)")
                        print("Set-Location folder - войти в папку")
                        print("New-Item folder -Type Directory - создать папку")
                        print("Remove-Item file.txt - удалить файл")
                        print("Copy-Item src dst - копировать")
                        print("Move-Item src dst - переместить")
                        print("Get-Content file.txt - показать содержимое")
                        print("Clear-Host       - очистить экран")
                        print("Get-Help команда - помощь по команде")
                        print("Полезные фишки:")
                        print("Get-Process | Where CPU -gt 50")
                        print("  # процессы с нагрузкой CPU > 50%")
                        print("Get-Service | Select Name, Status")
                        print("  # список всех служб")
                        print("Get-EventLog -LogName System -Newest 10")
                        print("  # последние 10 событий из лога")
                    
                    elif выбор_фишек__с_командной_строкой == "3":
                        print("LINUX/MAC TERMINAL ")
                        print("Основные команды:")
                        print("ls          - список файлов")
                        print("cd folder   - войти в папку")
                        print("cd ..       - выйти на уровень выше")
                        print("mkdir folder - создать папку")
                        print("rm file.txt - удалить файл")
                        print("rm -rf folder/ - удалить папку с файлами")
                        print("cp src dst  - копировать")
                        print("mv src dst  - переместить/переименовать")
                        print("cat file.txt - показать содержимое файла")
                        print("clear       - очистить экран")
                        print("man команда - справка по команде")
                        print("Полезные команды:")
                        print("sudo        - выполнить как администратор")
                        print("pwd         - текущая папка")
                        print("whoami      - текущий пользователь")
                        print("ps aux      - запущенные процессы")
                        print("top         - мониторинг системы")
                        print("grep текст файл - поиск текста в файле")
                        print("chmod +x script.sh - сделать файл исполняемым")
                    
                    elif выбор_фишек__с_командной_строкой == "4":
                        print("ПОЛЕЗНЫЕ КОМАНДЫ ")
                        print("1. Проверка диска:")
                        print("   Windows: chkdsk C:")
                        print("   Linux: df -h")
                        print("2. Поиск файлов:")
                        print("   Windows: dir /s *.txt")
                        print("   Linux: find / -name \"*.txt\"")
                        print("3. Архивация:")
                        print("   Windows: tar -cvf archive.tar folder/")
                        print("   Linux: tar -xvf archive.tar")
                        print("4. Сеть:")
                        print("   nslookup google.com - DNS запрос")
                        print("   netstat -r         - таблица маршрутизации")
                        print("5. Система:")
                        print("   Windows: systeminfo")
                        print("   Linux: uname -a")
                        print("   Mac: sw_vers")
                        print("6. Бэкап важных файлов:")
                        print("   Windows: xcopy C:\\docs D:\\backup\\ /E /H /C /I")
                        print("   Linux: cp -r ~/docs /backup/")
                    
                    input("Нажми Enter чтобы продолжить...")
                    
                except NotFoundFunctionError as elliot_bot_error_4:
                    print(f"Ошибка: {elliot_bot_error_4}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё про командную строку? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Выхожу из командной строки...")
                    break

        elif выбрать_функцию == "5":
            print("Установка windows/linux:")

            while True:
                print("Что нужно?")
                print("1- Установка Windows")
                print("2- Установка Linux")
                print("3- Создание загрузочной флешки")
                print("4- Драйверы и настройка")
                print("5- Ничего: выход из функции")
                
                try:
                    выбор_что_нужно_для_системы = input("Твой выбор (1-5): ").strip()
                    
                    if выбор_что_нужно_для_системы == "5":
                        print("Выхожу из установки ОС...")
                        break
                    
                    if выбор_что_нужно_для_системы not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_что_нужно_для_системы)
                    
                    if выбор_что_нужно_для_системы == "1":
                        print("УСТАНОВКА WINDOWS ")
                        print("1. Скачай Media Creation Tool")
                        print("2. Создай загрузочную флешку")
                        print("3. Перезагрузи ПК, зайди в Boot Menu")
                        print("4. Выбери флешку")
                        print("5. Следуй инструкциям")
                        print("6. Форматируй диск, устанавливай")
                        print("7. Установи драйверы")
                        print("8. Обнови Windows")
                    
                    elif выбор_что_нужно_для_системы == "2":
                        print("УСТАНОВКА LINUX UBUNTU ")
                        print("1. Скачай Ubuntu с ubuntu.com")
                        print("2. Используй Rufus для записи на флешку")
                        print("3. Перезагрузи, зайди в Boot Menu")
                        print("4. Выбери флешку")
                        print("5. Выбери 'Try Ubuntu' или 'Install'")
                        print("6. Следуй инструкциям")
                        print("7. После установки:")
                        print("   sudo apt update")
                        print("   sudo apt upgrade")
                        print("   sudo apt install software-properties-common")
                    
                    elif выбор_что_нужно_для_системы == "3":
                        print("ЗАГРУЗОЧНАЯ ФЛЕШКА ")
                        print("1. Скачай образ ОС (.iso)")
                        print("2. Скачай Rufus (Windows) или balenaEtcher")
                        print("3. Подключи флешку 8+ GB")
                        print("4. В Rufus выбери флешку и образ")
                        print("5. Нажми Start (данные удалятся!)")
                        print("6. Жди 5-30 минут")
                        print("7. Готово!")
                    
                    elif выбор_что_нужно_для_системы == "4":
                        print("ДРАЙВЕРЫ И НАСТРОЙКА ")
                        print("1. Видеокарта: сайт NVIDIA/AMD/Intel")
                        print("2. Материнская плата: сайт производителя")
                        print("3. Или используй DriverPack Solution")
                        print("4. Обязательные программы:")
                        print("   - Браузер (Chrome/Firefox)")
                        print("   - Антивирус")
                        print("   - Архиватор (7-Zip)")
                        print("   - Офис (Office/LibreOffice)")
                        print("   - Медиаплеер (VLC)")
                    
                    input("Нажми Enter чтобы продолжить...")               
                    
                except NotFoundFunctionError as elliot_bot_error_5:
                    print(f"Ошибка: {elliot_bot_error_5}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё про установку ОС? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Выхожу из установки ОС...")
                    break

        elif выбрать_функцию == "6":
                    print("Генератор паролей")

                    def generated_password():
                      chars =  string.ascii_letters + string.digits 
                      password = ''.join(random.choice(chars) for _ in range(10))
                      return password
                    
                    print("Ваш пароль сгенерирован:" , generated_password())
                    print("Данный сгенерированый пароль соотвествует норме Elliot_pw_normal")
                    print("О нормах паролях в README.md(Примечания)")

                    while True:
                      ещё = input("Сгенерировать пароль ещё раз: (да/нет): ").strip().lower()
                      if ещё == "да":
                        print("Новый пароль сгенерирован:", generated_password())
                        print("Данный сгенерированый пароль соотвествует норме Elliot_pw_normal")
                        print("О нормах паролях в README.md(Примечания)")

                      elif ещё == "нет":
                        print("Выхожу из данной функции")
                        break
                      

        elif выбрать_функцию == "7":
            print("Параметры:")

            print("\n")
            print(f"Логин Пользователя: {user_name}")
            print(f"ID Пользователя: {user_name_id}")
            print(f"Статус пользователя: {'Администратор' if is_admin else 'Пользователь'}")
            print(f"Дата входа: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} ")
        
        
        elif выбрать_функцию == "8":
            print("Связь с разработчиком:")

            print("\n")

            email_parts = [ #Шифр почты 
                "alexx",
                "-coder",
                "@",
                "internet",
                ".ru"
            ]

            email = "".join(email_parts)

            print("Разработчик: Alexx-coder")
            print(f"Почта: {email}")
            print("GitHub: Alexx-coder или просто alex")

            print("Пиши на почту только по делу!")

        elif выбрать_функцию == "9":
            print("Команды:")

            print("\n")
            print("/help - помошь с командами")
            print("/version_bot - какая версия у данного бота")
            print("/data_version - дата выхода данной версии")
            print("/time - текущее время")
            print("/data - текущая дата")
            print("/my_account_info - информация аккаунта пользователя")
            print("/addition - узнать,существует ли дополнеие к этой версии")
            print("/christmas - новогодние функции")
            print("/whoami - кто я?")
            print("/exit_command - выход из функции")
            


        elif выбрать_функцию == "10":
            print("Терминал:")

            print("\n")
            print("Список всех команд из функции 9")
            print("Команды:")
            print("/help - помошь с командами")
            print("/version_bot - какая версия у данного бота")
            print("/data_version - дата выхода данной версии")
            print("/time - текущее время")
            print("/data - текущая дата")
            print("/my_account_info - информация аккаунта пользователя")
            print("/addition - узнать,существует ли дополнеие к этой версии")
            print("/christmas - новогодние функции")
            print("/whoami - кто я?")
            print("/exit_command - выход из функции")



            print("\n")

            while True:
                написать_команду = input("\nВведите нужную вам команду ")
                if написать_команду == "/help":
                  print("Команды:")
                  print("/help - помошь с командами")
                  print("/version_bot - какая версия у данного бота")
                  print("/data_version - дата выхода данной версии")
                  print("/time - текущее время")
                  print("/data - текущая дата")
                  print("/my_account_info - информация аккаунта пользователя")
                  print("/addition - узнать,существует ли дополнеие к этой версии")
                  print("/christmas - новогодние функции")
                  print("/whoami - кто я?")
                  print("/exit_command - выход из функции")


                elif написать_команду == "/version_bot":
                  print(f"Версия бота которую используете на данный момент: {version_bot}")

                elif написать_команду == "/data_version":
                  print(f"Когда был выход данной версии бота: {data_version}")
                elif написать_команду == "/time":
                  time_now = datetime.datetime.now()
                  print(f"Текущее время: {hour_now:02}:{minute_now:02}:{second_now:02}")
                elif написать_команду == "/data":
                  time_now = datetime.datetime.now()
                  print(f"Текущая дата: {day_now}.{month_now}.{year_now}")
                elif написать_команду == "/my_account_info":
                  print("Данные о пользователе:")
                  print(f"Логин аккаунта: {user_name}")
                  print(f"ID аккаунта: {user_name_id}")
                  print(f"Статус пользователя: {'Администратор' if is_admin else 'Пользователь'}")
                  print(f"Дата входа: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} ")
                elif написать_команду == "/addition":
                    print("Не существуют дополнения к данной версии!")

                elif написать_команду == "/whoami":
                    print(f"Вы: {user_name}")
                    
                elif написать_команду == "/exit_command":
                  print("Выхожу из данной функции")
                  break


        elif выбрать_функцию == "11":
           print("Проверка:")
           print("\n")
    
           while True:
              print("Что нужно?")
              print("1- Проверка почт")
              print("2- Проверка номеров телефонов (русские номера)")
              print("3- Выход из функции")
        
              выбор_проверок = input("Твой выбор (1-3): ").strip()
        
              if выбор_проверок == "1":
                user_email_check = input("Введите почту для проверки: ")
                
                if validate_email(user_email_check):
                    print("Email корректный")
                else:
                    print("Email некорекктный")

            
              elif выбор_проверок == "2":
                print("Введите номер телефона для проверки")
                print("Формат: +7-XXX-XXX-XX-XX")
                proverka_number = input('>')
            
                pattern = re.compile(r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}")
            
                if pattern.match(proverka_number):
                  print("Номер записан правильно!")
                else:
                  print("Номер записан не правильно!")
        
              elif выбор_проверок == "3":
                print("Выхожу из функции проверки")
                break
        
              else:
                   print("Неверный выбор! Введите 1, 2 или 3")
                   continue
        
        # Спросим, хочет ли проверить ещё что-то
        while True:
            ещё = input("\nВыбрать ещё что-то? (да/нет): ").strip().lower()
            if ещё in ["да", "нет"]:
                break

            print("Введите 'да' или 'нет'")
        
        if ещё == "нет":
            print("Выхожу из данной функции")
            break
            

    except NotFoundFunctionError as elliot_bot_0:
        print(f"Ошибка: {elliot_bot_0}")
        print("Не найдено! Введите 1-11")


# Данный проект и версия проекта создана Alexx-coder или alex
# Данный проект лицензирован под MIT LICENSE - см. файл LICENSE
# Примечания - см. файл README.md
