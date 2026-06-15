# vlqdus_mxs (2026)
# ER1AER

from machine import Pin, PWM
import time
import os

# Default settings
freq = 7025000      # Frequency (Hz)
dit = 0.1           # dit duration
useled = True       # Use the ESP32 on-board LED (True or False)
selectedpin = 23    # PWM Pin used for transmitting RF
callsign = "N0CALL" # Default callsign
usecallsign = False # To use the callsign? (True or False)
language = "EN"     # Default language (EN - English; RU - Russian)

SETTINGS_FILENAME = "settings.txt"
LOG_FILENAME = "transmission_log.txt"

# Interface strings (English and Russian)
STRINGS = {
    "RU": {
        "settings_loaded": "Настройки успешно загружены из",
        "settings_file_not_found": "Файл настроек {} не найден. Используются настройки по умолчанию.",
        "settings_load_error": "Ошибка загрузки настроек: {}. Используются настройки по умолчанию.",
        "settings_saved": "Настройки успешно сохранены в",
        "settings_save_error": "Ошибка сохранения настроек: {}",
        "pwm_init_success": "PWM инициализирован на пине {} с частотой: {}",
        "pwm_init_error_pin": "Ошибка инициализации PWM на пине {}: {}. Возможно, неверный номер пина.",
        "pwm_init_error_unknown": "Неизвестная ошибка инициализации PWM: {}",
        "pwm_not_init": "PWM не инициализирован. Невозможно отправить сигнал. Проверьте настройки пина.",
        "transmission_start": "[{}] Передача: {} (~{:.1f} WPM)",
        "transmission_done": "Готово. Время передачи: {:.2f} сек",
        "test_tone_duration": "Тестовый тон: {} сек",
        "test_tone_pwm_not_init": "PWM не инициализирован. Невозможно сгенерировать тон.",
        "settings_header": "\n--- НАСТРОЙКА ПАРАМЕТРОВ ---",
        "current_freq": "Текущая частота: {} Гц. Новая частота (Enter, чтобы оставить): ",
        "freq_positive_error": "Частота должна быть положительным числом. Значение не изменено.",
        "current_wpm": "Текущая WPM: {:.1f}. Новая WPM (Enter, чтобы оставить): ",
        "wpm_positive_error": "WPM должна быть положительным числом. Значение не изменено.",
        "use_led": "Использовать LED для индикации? (y/n), сейчас: {}: ",
        "yes": "Да",
        "no": "Нет",
        "invalid_led_input": "Некорректный ввод для LED. Значение не изменено.",
        "settings_updated": "Обновлено: частота={}, dit={:.3f} сек (примерно {:.1f} WPM), LED={}", # Adjusted
        "value_error_settings": "Ошибка: Введите корректное числовое значение для частоты или WPM.", # Adjusted
        "general_error_settings": "Произошла ошибка при настройке: {}",
        "callsign_header": "\n--- НАСТРОЙКА ПОЗЫВНОГО ---",
        "current_callsign": "Текущий позывной: '{}'. Введите новый (Enter, чтобы оставить): ",
        "use_callsign": "Использовать позывной перед сообщениями? (y/n), сейчас: {}: ",
        "invalid_callsign_use_input": "Некорректный ввод. Использование позывного не изменено.",
        "callsign_updated": "Обновлено: позывной='{}', использовать позывной: {}",
        "enter_text_to_send": "Введите текст для передачи: ",
        "no_text_or_last_text": "Текст для передачи не указан и нет последнего переданного текста.",
        "continuous_tone_pwm_not_init": "PWM не инициализирован. Невозможно включить непрерывный тон.",
        "continuous_tone_on": "Включён непрерывный тон. Нажмите Enter для выключения.",
        "continuous_tone_off": "Тон выключен.",
        "log_write_error": "Ошибка записи лога: {}",
        "transmission_history_header": "\n=== История передач ===",
        "log_empty": "Лог пуст.",
        "log_invalid_format_conversion": "Некорректный формат данных в строке лога (ошибка преобразования): {}",
        "log_invalid_format_fields": "Некорректный формат данных в строке лога (недостаточно полей): {}",
        "log_file_not_found": "Файл лога не найден.",
        "log_read_error": "Произошла ошибка при чтении лога: {}",
        "transmission_history_footer": "======================\n",
        "enter_text_to_repeat": "Введите текст для повтора: ",
        "text_not_entered": "Текст не введён.",
        "repeat_count_prompt": "Сколько раз повторить? ",
        "repeat_count_positive_error": "Количество повторений должно быть положительным числом.",
        "repeat_count_value_error": "Ошибка: введите целое число.",
        "repeating": "Повтор {} из {}",
        "menu_header": "\n=== МЕНЮ ===",
        "menu_send_text": "1. Передать текст",
        "menu_test_tone": "2. Тестовый тон",
        "menu_settings": "3. Настройки (частота/WPM/LED)", # Adjusted
        "menu_repeat_last": "4. Повторить последний переданный текст",
        "menu_continuous_tone": "5. Непрерывный тон (manual key down)",
        "menu_repeat_any": "6. Повторить произвольный текст N раз",
        "menu_exit": "7. Выход",
        "menu_callsign": "8. Настройка позывного",
        "menu_show_history": "9. Показать историю передач",
        "menu_change_language": "L. Сменить язык",
        "menu_choice_prompt": "Выберите режим (1-9, L): ",
        "invalid_input": "Неверный ввод. Попробуйте снова.",
        "repeat_last_no_text": "Нет последнего переданного текста для повтора в текущей сессии.",
        "stopped_by_user": "\nОстановлено пользователем.",
        "pwm_deinitialized": "PWM отключен.",
        "program_finished": "Программа завершена.",
        "current_language": "Текущий язык: {}"
    },
    "EN": {
        "settings_loaded": "Settings successfully loaded from",
        "settings_file_not_found": "Settings file {} not found. Using default settings.",
        "settings_load_error": "Error loading settings: {}. Using default settings.",
        "settings_saved": "Settings successfully saved to",
        "settings_save_error": "Error saving settings: {}",
        "pwm_init_success": "PWM initialized on pin {} with frequency: {}",
        "pwm_init_error_pin": "Error initializing PWM on pin {}: {}. Possibly an invalid pin number.",
        "pwm_init_error_unknown": "Unknown PWM initialization error: {}",
        "pwm_not_init": "PWM not initialized. Cannot send signal. Check pin settings.",
        "transmission_start": "[{}] Transmitting: {} (~{:.1f} WPM)",
        "transmission_done": "Done. Transmission time: {:.2f} sec",
        "test_tone_duration": "Test tone: {} sec",
        "test_tone_pwm_not_init": "PWM not initialized. Cannot generate tone.",
        "settings_header": "\n--- SETTINGS ---",
        "current_freq": "Current frequency: {} Hz. New frequency (Enter to keep): ",
        "freq_positive_error": "Frequency must be a positive number. Value not changed.",
        "current_wpm": "Current WPM: {:.1f}. New WPM (Enter to keep): ",
        "wpm_positive_error": "WPM must be a positive number. Value not changed.",
        "use_led": "Use LED for indication? (y/n), currently: {}: ",
        "yes": "Yes",
        "no": "No",
        "invalid_led_input": "Invalid input for LED. Value not changed.",
        "settings_updated": "Updated: freq={}, dit={:.3f} sec (approx {:.1f} WPM), LED={}", # Adjusted
        "value_error_settings": "Error: Enter a valid numerical value for frequency or WPM.", # Adjusted
        "general_error_settings": "An error occurred during configuration: {}",
        "callsign_header": "\n--- CALLSIGN SETTINGS ---",
        "current_callsign": "Current callsign: '{}'. Enter new (Enter to keep): ",
        "use_callsign": "Use callsign before messages? (y/n), currently: {}: ",
        "invalid_callsign_use_input": "Invalid input. Callsign usage not changed.",
        "callsign_updated": "Updated: callsign='{}', use callsign: {}",
        "enter_text_to_send": "Enter text to transmit: ",
        "no_text_or_last_text": "No text entered for transmission and no last transmitted text.",
        "continuous_tone_pwm_not_init": "PWM not initialized. Cannot turn on continuous tone.",
        "continuous_tone_on": "Continuous tone on. Press Enter to turn off.",
        "continuous_tone_off": "Tone off.",
        "log_write_error": "Error writing log: {}",
        "transmission_history_header": "\n=== Transmission History ===",
        "log_empty": "Log is empty.",
        "log_invalid_format_conversion": "Invalid data format in log line (conversion error): {}",
        "log_invalid_format_fields": "Invalid data format in log line (insufficient fields): {}",
        "log_file_not_found": "Log file not found.",
        "log_read_error": "An error occurred while reading the log: {}",
        "transmission_history_footer": "======================\n",
        "enter_text_to_repeat": "Enter text to repeat: ",
        "text_not_entered": "Text not entered.",
        "repeat_count_prompt": "How many times to repeat? ",
        "repeat_count_positive_error": "Repeat count must be a positive number.",
        "repeat_count_value_error": "Error: Please enter an integer.",
        "repeating": "Repeating {} of {}",
        "menu_header": "\n=== MENU ===",
        "menu_send_text": "1. Transmit text",
        "menu_test_tone": "2. Test tone",
        "menu_settings": "3. Settings (frequency/WPM/LED)", # Adjusted
        "menu_repeat_last": "4. Repeat last transmitted text",
        "menu_continuous_tone": "5. Continuous tone (manual key down)",
        "menu_repeat_any": "6. Repeat any text N times",
        "menu_exit": "7. Exit",
        "menu_callsign": "8. Callsign settings",
        "menu_show_history": "9. Show transmission history",
        "menu_change_language": "L. Change language",
        "menu_choice_prompt": "Select mode (1-9, L): ",
        "invalid_input": "Invalid input. Please try again.",
        "repeat_last_no_text": "No last transmitted text to repeat in current session.",
        "stopped_by_user": "\nStopped by user.",
        "pwm_deinitialized": "PWM deinitialized.",
        "program_finished": "Program finished.",
        "current_language": "Current language: {}"
    }
}

# Components
led = Pin(2, Pin.OUT)
led.value(0)
pwm = None # PWM will be initialized only once

# Morse code alphabet
morse_code = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    '.': '.-.-.-',    ',': '--..--',    '?': '..--..',
    '\'': '.----.',    '!': '-.-.--',    '/': '-..-.',
    '(': '-.--.',     ')': '-.--.-',    '&': '.-...',
    ':': '---...',    ';': '-.-.-.',    '=': '-...-',
    '+': '.-.-.',     '-': '-....-',    '_': '..--.-',
    '"': '.-..-.',    '$': '...-..-',   '@': '.--.-.',
    ' ': ' '
}

def get_string(key):
    """Возвращает строку на текущем языке."""
    global language
    if language not in STRINGS:
        language = "EN"
    return STRINGS[language].get(key, f"MISSING_STRING_{key}")

# Settings

def load_settings():
    """Загружает настройки из файла settings.txt."""
    global freq, dit, useled, callsign, usecallsign, language
    try:
        with open(SETTINGS_FILENAME, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                if key == 'freq':
                    freq = int(value)
                elif key == 'dit':
                    dit = float(value)
                elif key == 'useled':
                    useled = value.lower() == 'true'
                elif key == 'callsign':
                    callsign = value
                elif key == 'usecallsign':
                    usecallsign = value.lower() == 'true'
                elif key == 'language':
                    if value in STRINGS:
                        language = value
        print(get_string("settings_loaded"), SETTINGS_FILENAME)
    except OSError:
        print(get_string("settings_file_not_found").format(SETTINGS_FILENAME))
        save_settings()
    except Exception as e:
        print(get_string("settings_load_error").format(e))
        save_settings()

def save_settings():
    """Сохраняет текущие настройки в файл settings.txt."""
    global freq, dit, useled, callsign, usecallsign, language
    try:
        with open(SETTINGS_FILENAME, 'w') as f:
            f.write(f"freq={freq}\n")
            f.write(f"dit={dit}\n")
            f.write(f"useled={useled}\n")
            f.write(f"callsign={callsign}\n")
            f.write(f"usecallsign={usecallsign}\n")
            f.write(f"language={language}\n")
        print(get_string("settings_saved"), SETTINGS_FILENAME)
    except Exception as e:
        print(get_string("settings_save_error").format(e))


# Useful functions

def calculate_wpm(dit_seconds):
    """Вычисляет слова в минуту (WPM) на основе длительности точки."""
    return 1.2 / dit_seconds

def cw_send_text(text, dit=0.1):
    """Отправляет заданный текст кодом Морзе."""
    global callsign, usecallsign, pwm

    if pwm is None:
        print(get_string("pwm_not_init"))
        return

    if usecallsign and callsign.strip():
        text = f"[{callsign}] {text}"

    wpm = calculate_wpm(dit)
    print(get_string("transmission_start").format(time.localtime(), text, wpm))
    start_time = time.ticks_ms()

    for letter in text.upper():
        code = morse_code.get(letter, '')
        for char in code:
            if char == '.':
                pwm.duty(512)
                if useled:
                    led.value(1)
                time.sleep(dit)
                pwm.duty(0)
                if useled:
                    led.value(0)
            elif char == '-':
                pwm.duty(512)
                if useled:
                    led.value(1)
                time.sleep(3 * dit)
                pwm.duty(0)
                if useled:
                    led.value(0)
            else: # Space between symbols
                time.sleep(dit)
            time.sleep(dit) 
        time.sleep(3 * dit) # Space between letters

    total_time = (time.ticks_ms() - start_time) / 1000
    print(get_string("transmission_done").format(total_time))

    log_transmission_to_file(text, total_time, wpm)

# Test Tone generator
def test_tone(duration=2):
    """Генерирует тестовый тон на заданную длительность."""
    global pwm
    if pwm is None:
        print(get_string("test_tone_pwm_not_init"))
        return
    print(get_string("test_tone_duration").format(duration))
    pwm.duty(512)
    time.sleep(duration)
    pwm.duty(0)

def configure_settings():
    """Позволяет пользователю настроить частоту, WPM и использование LED. Пин не изменяется."""
    global freq, dit, useled, pwm, selectedpin

    # Disabling PWM in the settings page, to remove any pwm interference tones
    if pwm:
        pwm.duty(0)

    print(get_string("settings_header"))
    try:
        new_freq_str = input(get_string("current_freq").format(freq))
        if new_freq_str.strip():
            new_freq = int(new_freq_str)
            if new_freq > 0:
                freq = new_freq
            else:
                print(get_string("freq_positive_error"))

        current_wpm = calculate_wpm(dit)
        new_wpm_str = input(get_string("current_wpm").format(current_wpm))
        if new_wpm_str.strip():
            new_wpm = float(new_wpm_str)
            if new_wpm > 0:
                dit = 1.2 / new_wpm
            else:
                print(get_string("wpm_positive_error"))

        new_useled_str = input(get_string("use_led").format(get_string("yes") if useled else get_string("no"))).lower()
        if new_useled_str == 'y':
            useled = True
        elif new_useled_str == 'n':
            useled = False
        else:
            print(get_string("invalid_led_input"))

        # Updating the PWM frequency, without re-initializing PWM
        if pwm and pwm.freq() != freq:
            try:
                pwm.freq(freq)
                print(get_string("pwm_init_success").format(selectedpin, pwm.freq()))
            except Exception as e:
                print(get_string("pwm_init_error_unknown").format(e))


        print(get_string("settings_updated").format(freq, dit, calculate_wpm(dit), useled))
        save_settings()
    except ValueError:
        print(get_string("value_error_settings"))
    except Exception as e:
        print(get_string("general_error_settings").format(e))

# Callsign configuration
def configure_callsign():
    """Позволяет пользователю настроить позывной и его использование."""
    global callsign, usecallsign
    print(get_string("callsign_header"))
    new_callsign = input(get_string("current_callsign").format(callsign))
    if new_callsign.strip():
        callsign = new_callsign.strip()

    use_input = input(get_string("use_callsign").format(get_string("yes") if usecallsign else get_string("no"))).lower()
    if use_input == 'y':
        usecallsign = True
    elif use_input == 'n':
        usecallsign = False
    else:
        print(get_string("invalid_callsign_use_input"))
    print(get_string("callsign_updated").format(callsign, get_string("yes") if usecallsign else get_string("no")))
    save_settings()

def change_language_setting():
    """Позволяет пользователю изменить язык интерфейса."""
    global language
    print(get_string("current_language").format(language))
    print("Available languages: RU, EN")
    new_lang = input("Enter new language code (RU/EN): ").upper()
    if new_lang in STRINGS:
        language = new_lang
        save_settings()
        print(get_string("current_language").format(language))
    else:
        print(get_string("invalid_input"))

last_text = ""

def input_and_send():
    """Запрашивает текст у пользователя и отправляет его."""
    global last_text
    user_text = input(get_string("enter_text_to_send"))
    if user_text.strip():
        last_text = user_text
    elif not last_text:
        print(get_string("no_text_or_last_text"))
        return
    cw_send_text(last_text, dit)

def continuous_tone():
    """Включает непрерывный тон до нажатия Enter."""
    global pwm
    if pwm is None:
        print(get_string("continuous_tone_pwm_not_init"))
        return
    print(get_string("continuous_tone_on"))
    pwm.duty(512)
    input()
    pwm.duty(0)
    print(get_string("continuous_tone_off"))

def log_transmission_to_file(text, duration, wpm):
    """Записывает информацию о передаче в файл лога."""
    try:
        with open(LOG_FILENAME, "a") as f:
            timestamp = int(time.time())
            f.write(f"{timestamp},{text},~{wpm:.1f}WPM,{duration:.2f}\n")
    except Exception as e:
        print(get_string("log_write_error").format(e))

def read_log_file():
    """Читает и выводит последние 10 записей из файла лога."""
    print(get_string("transmission_history_header"))
    try:
        with open(LOG_FILENAME, "r") as f:
            lines = f.readlines()
            if not lines:
                print(get_string("log_empty"))
                return
            for line in lines[-10:]: 
                parts = line.strip().split(",", 3)
                if len(parts) == 4:
                    timestamp_str, text_logged, wpm_str, duration_str = parts
                    try:
                        timestamp = int(timestamp_str)
                        t = time.localtime(timestamp)

                        time_str = f"{t[2]:02d}.{t[1]:02d}.{t[0]} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

                        duration_unit = get_string('transmission_done').split(' ')[-1].strip('.')
                        print(f"{time_str} - '{text_logged}' ({wpm_str}, {duration_str} {duration_unit})")
                    except ValueError:
                        print(get_string("log_invalid_format_conversion").format(line.strip()))
                else:
                    print(get_string("log_invalid_format_fields").format(line.strip()))
    except OSError:
        print(get_string("log_file_not_found"))
    except Exception as e:
        print(get_string("log_read_error").format(e))
    print(get_string("transmission_history_footer"))

def repeat_transmission():
    """Позволяет повторить произвольный текст N раз."""
    user_text_to_repeat = input(get_string("enter_text_to_repeat"))
    if not user_text_to_repeat.strip():
        print(get_string("text_not_entered"))
        return
    try:
        count = int(input(get_string("repeat_count_prompt")))
        if count <= 0:
            print(get_string("repeat_count_positive_error"))
            return
    except ValueError:
        print(get_string("repeat_count_value_error"))
        return

    for i in range(count):
        print(get_string("repeating").format(i+1, count))
        cw_send_text(user_text_to_repeat, dit)
        time.sleep(dit * 7) # Small pause between TX repeats

def main_menu():
    """Главное меню программы."""
    global last_text
    while True:
        print(get_string("menu_header"))
        print(get_string("menu_send_text"))
        print(get_string("menu_test_tone"))
        print(get_string("menu_settings"))
        print(get_string("menu_repeat_last"))
        print(get_string("menu_continuous_tone"))
        print(get_string("menu_repeat_any"))
        print(get_string("menu_exit"))
        print(get_string("menu_callsign"))
        print(get_string("menu_show_history"))
        print(get_string("menu_change_language"))
        choice = input(get_string("menu_choice_prompt")).lower()

        if choice == '1':
            input_and_send()
        elif choice == '2':
            test_tone()
        elif choice == '3':
            configure_settings()
        elif choice == '4':
            if last_text:
                print(f"{get_string('repeat_last_no_text').split('.')[0]}: '{last_text}'")
                cw_send_text(last_text, dit)
            else:
                print(get_string("repeat_last_no_text"))
        elif choice == '5':
            continuous_tone()
        elif choice == '6':
            repeat_transmission()
        elif choice == '7':
            break
        elif choice == '8':
            configure_callsign()
        elif choice == '9':
            read_log_file()
        elif choice == 'l':
            change_language_setting()
        else:
            print(get_string("invalid_input"))

# Program startup
if __name__ == '__main__':
    load_settings()

    try:
        pwm = PWM(Pin(selectedpin))
        pwm.freq(freq)
        pwm.duty(0)
        print(get_string("pwm_init_success").format(selectedpin, pwm.freq()))
    except ValueError as e:
        print(get_string("pwm_init_error_pin").format(selectedpin, e))
        pwm = None
    except Exception as e:
        print(get_string("pwm_init_error_unknown").format(e))
        pwm = None

    try:
        main_menu()
    except KeyboardInterrupt:
        print(get_string("stopped_by_user"))
    finally:
        if pwm:
            pwm.deinit() # PWM de-initializaton at exit
            print(get_string("pwm_deinitialized"))
        print(get_string("program_finished"))

