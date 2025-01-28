import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import random
import threading

# Список случайных сообщений
messages = [
    "Привет! Как дела?",
    "Что нового?",
    "Как твои успехи?",
    "Давно не виделись!",
    "Как погода у тебя?",
    "Чем занимаешься?",
    "Как настроение?",
    "Что планируешь на выходные?",
    "Как работа?",
    "Какие планы на сегодня?",
    "Как семья?",
    "Что интересного?",
    "Как здоровье?",
    "Как твои дела на работе?",
    "Что читаешь?",
    "Какой у тебя план на день?",
    "Как твой проект?",
    "Как твои друзья?",
    "Что смотришь?",
    "Как твой день проходит?"
]

# Глобальные переменные
is_confirmed = False
drivers_initialized = False
driver1 = None
driver2 = None

# Функция для отправки сообщения
def send_message(driver, phone_number, message, log_callback):
    try:
        log_callback(f"Открываю чат с номером: {phone_number}")
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
        
        # Ожидание загрузки поля ввода сообщения
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        
        # Ввод сообщения
        input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        input_box.send_keys(message + Keys.ENTER)
        log_callback(f"Сообщение отправлено на номер: {phone_number}")
    except Exception as e:
        log_callback(f"Ошибка при отправке на номер {phone_number}: {e}")

# Основная функция для запуска переписки
def start_chat(number1, number2, proxy1, proxy2, proxy1_auth, proxy2_auth, log_callback):
    global driver1, driver2, drivers_initialized

    # Создаем уникальные папки для пользовательских данных
    user_data_dir1 = os.path.join(os.getcwd(), "chrome_profile_1")
    user_data_dir2 = os.path.join(os.getcwd(), "chrome_profile_2")

    # Убедимся, что папки существуют
    os.makedirs(user_data_dir1, exist_ok=True)
    os.makedirs(user_data_dir2, exist_ok=True)

    # Инициализация двух драйверов (два окна браузера)
    options1 = webdriver.ChromeOptions()
    options1.add_argument(f"--user-data-dir={user_data_dir1}")  # Уникальная папка для первого драйвера
    options1.add_argument("--no-sandbox")  # Отключает sandbox
    options1.add_argument("--disable-dev-shm-usage")  # Решает проблему с памятью
    options1.add_argument("--remote-debugging-port=9222")  # Указывает порт для отладки
    options1.add_argument("--disable-gpu")  # Отключает GPU

    # Обработка прокси для первого номера
    if proxy1:
        try:
            # Разбираем формат host:port:username:password
            host, port, username, password = proxy1.split(":")
            proxy1 = f"{username}:{password}@{host}:{port}"
            options1.add_argument(f"--proxy-server={proxy1}")  # Прокси для первого номера
        except Exception as e:
            log_callback(f"Ошибка при разборе прокси 1: {e}")

    options2 = webdriver.ChromeOptions()
    options2.add_argument(f"--user-data-dir={user_data_dir2}")  # Уникальная папка для второго драйвера
    options2.add_argument("--no-sandbox")  # Отключает sandbox
    options2.add_argument("--disable-dev-shm-usage")  # Решает проблему с памятью
    options2.add_argument("--remote-debugging-port=9223")  # Указывает порт для отладки
    options2.add_argument("--disable-gpu")  # Отключает GPU

    # Обработка прокси для второго номера
    if proxy2:
        try:
            # Разбираем формат host:port:username:password
            host, port, username, password = proxy2.split(":")
            proxy2 = f"{username}:{password}@{host}:{port}"
            options2.add_argument(f"--proxy-server={proxy2}")  # Прокси для второго номера
        except Exception as e:
            log_callback(f"Ошибка при разборе прокси 2: {e}")

    # Автоматическая загрузка ChromeDriver
    driver_path = ChromeDriverManager().install()

    # Использование Service для указания пути к драйверу
    service1 = Service(executable_path=driver_path)
    service2 = Service(executable_path=driver_path)

    # Инициализация драйверов
    try:
        driver1 = webdriver.Chrome(service=service1, options=options1)
        driver2 = webdriver.Chrome(service=service2, options=options2)
        drivers_initialized = True
    except Exception as e:
        log_callback(f"Ошибка при инициализации драйверов: {e}")
        return

    # Открытие WhatsApp Web в обоих окнах
    try:
        driver1.get("https://web.whatsapp.com")
        driver2.get("https://web.whatsapp.com")
        log_callback("Войди в WhatsApp Web в обоих окнах и нажми 'Подтвердить вход'.")
    except Exception as e:
        log_callback(f"Ошибка при открытии WhatsApp Web: {e}")
        return

    # Ожидание подтверждения входа
    global is_confirmed
    while not is_confirmed:
        time.sleep(1)

    log_callback("Вход подтверждён. Начинаю переписку...")

    # Бесконечная переписка
    try:
        while True:
            # Выбираем случайное сообщение для первого номера
            message1 = random.choice(messages)
            # Первый номер отправляет сообщение второму
            send_message(driver1, number2, message1, log_callback)
            time.sleep(random.randint(5, 15))  # Случайная задержка от 5 до 15 секунд

            # Выбираем случайное сообщение для второго номера
            message2 = random.choice(messages)
            # Второй номер отправляет сообщение первому
            send_message(driver2, number1, message2, log_callback)
            time.sleep(random.randint(5, 15))  # Случайная задержка от 5 до 15 секунд
    except Exception as e:
        log_callback(f"Ошибка: {e}")
    finally:
        # Закрытие браузеров
        if driver1:
            driver1.quit()
        if driver2:
            driver2.quit()
        log_callback("Браузеры закрыты.")

# Функция для подтверждения входа
def confirm_login():
    global is_confirmed
    is_confirmed = True
    log("Вход подтверждён. Начинаю переписку...")

# Функция для запуска программы в отдельном потоке
def start_program():
    number1 = entry_number1.get()
    number2 = entry_number2.get()
    proxy1 = entry_proxy1.get()
    proxy2 = entry_proxy2.get()
    
    # Получаем данные для авторизации на прокси (если указаны)
    proxy1_auth = {
        "username": entry_proxy1_user.get(),
        "password": entry_proxy1_pass.get()
    } if entry_proxy1_user.get() or entry_proxy1_pass.get() else None

    proxy2_auth = {
        "username": entry_proxy2_user.get(),
        "password": entry_proxy2_pass.get()
    } if entry_proxy2_user.get() or entry_proxy2_pass.get() else None

    if not number1 or not number2:
        log("Пожалуйста, введите оба номера.")
        return

    log("Запуск программы...")
    threading.Thread(target=start_chat, args=(number1, number2, proxy1, proxy2, proxy1_auth, proxy2_auth, log), daemon=True).start()

# Функция для вывода логов
def log(message):
    log_area.insert(tk.END, message + "\n")
    log_area.yview(tk.END)

# Функции для копирования и вставки
def copy_text(event=None):
    root.clipboard_clear()
    try:
        text = log_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        root.clipboard_append(text)
    except tk.TclError:
        pass

def paste_text(event=None):
    try:
        text = root.clipboard_get()
        log_area.insert(tk.INSERT, text)
    except tk.TclError:
        pass

def copy_entry_text(event=None):
    root.clipboard_clear()
    try:
        text = entry_number1.selection_get()
        root.clipboard_append(text)
    except tk.TclError:
        pass

def paste_entry_text(event=None):
    try:
        text = root.clipboard_get()
        entry_number1.insert(tk.INSERT, text)
    except tk.TclError:
        pass

# Создание графического интерфейса
root = tk.Tk()
root.title("WhatsApp Прогрев Аккаунтов")
root.geometry("600x600")

# Поля для ввода номеров
tk.Label(root, text="Номер №1:").pack(pady=5)
entry_number1 = tk.Entry(root, width=30)
entry_number1.pack(pady=5)

tk.Label(root, text="ip адрес для прокси для номера №1 :").pack(pady=5)
entry_proxy1 = tk.Entry(root, width=30)
entry_proxy1.pack(pady=5)

tk.Label(root, text="Логин для прокси №1(если закрытый, то вводим логин и пароль) :").pack(pady=5)
entry_proxy1_user = tk.Entry(root, width=30)
entry_proxy1_user.pack(pady=5)

tk.Label(root, text="Пароль для прокси №1:").pack(pady=5)
entry_proxy1_pass = tk.Entry(root, width=30, show="*")
entry_proxy1_pass.pack(pady=5)

tk.Label(root, text="Номер №2:").pack(pady=5)
entry_number2 = tk.Entry(root, width=30)
entry_number2.pack(pady=5)

tk.Label(root, text="Прокси для номера №2 :").pack(pady=5)
entry_proxy2 = tk.Entry(root, width=30)
entry_proxy2.pack(pady=5)

tk.Label(root, text="Логин для прокси №2(если закрытый, то вводим логин и пароль) :").pack(pady=5)
entry_proxy2_user = tk.Entry(root, width=30)
entry_proxy2_user.pack(pady=5)

tk.Label(root, text="Пароль для прокси №2:").pack(pady=5)
entry_proxy2_pass = tk.Entry(root, width=30, show="*")
entry_proxy2_pass.pack(pady=5)

# Кнопка для запуска программы
start_button = tk.Button(root, text="Запустить программу", command=start_program)
start_button.pack(pady=10)

# Кнопка для подтверждения входа
confirm_button = tk.Button(root, text="Подтвердить вход", command=confirm_login)
confirm_button.pack(pady=10)

# Текстовое поле для логов
log_area = scrolledtext.ScrolledText(root, width=70, height=15)
log_area.pack(pady=10)

# Привязка горячих клавиш
log_area.bind("<Control-c>", copy_text)  # Копирование (Ctrl+C)
log_area.bind("<Control-v>", paste_text)  # Вставка (Ctrl+V)
entry_number1.bind("<Control-c>", copy_entry_text)  # Копирование (Ctrl+C)
entry_number1.bind("<Control-v>", paste_entry_text)  # Вставка (Ctrl+V)

# Запуск основного цикла GUI
root.mainloop()