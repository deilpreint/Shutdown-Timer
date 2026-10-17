import ctypes
import subprocess
import sys

IS_WINDOWS = sys.platform == "win32"

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
CREATE_NO_WINDOW = 0x08000000

ERR_ALREADY_SCHEDULED = 1190
ERR_NOTHING_TO_CANCEL = 1116

MAX_SECONDS = 315360000


class ShutdownError(Exception):
    """Ошибка с понятным для пользователя текстом."""

def parse_time(hours_text, minutes_text):
    try:
        hours = int(hours_text.strip() or 0)
        minutes = int(minutes_text.strip() or 0)
    except ValueError:
        raise ShutdownError("Введите числа, без букв и знаков")

    if hours < 0 or minutes < 0:
        raise ShutdownError("Время не может быть отрицательным")

    total = hours * 3600 + minutes * 60
    if total <= 0:
        raise ShutdownError("Укажите время больше нуля")
    if total > MAX_SECONDS:
        raise ShutdownError("Слишком большое время")
    return total


def _run_shutdown(*args):
    flags = CREATE_NO_WINDOW if IS_WINDOWS else 0
    try:
        result = subprocess.run(["shutdown", *args], capture_output=True, creationflags=flags)
    except FileNotFoundError:
        raise ShutdownError("Команда shutdown не найдена. Программа работает только в Windows")
    return result.returncode


def prevent_sleep():
    if IS_WINDOWS:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def allow_sleep():
    if IS_WINDOWS:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def schedule_shutdown(seconds):
    code = _run_shutdown("/s", "/t", str(seconds))
    if code == ERR_ALREADY_SCHEDULED:
        raise ShutdownError("Выключение уже запланировано. Сначала отмените его")
    if code != 0:
        raise ShutdownError(f"Не удалось запланировать выключение (код {code})")
    prevent_sleep()


def cancel_shutdown():
    code = _run_shutdown("/a")
    if code not in (0, ERR_NOTHING_TO_CANCEL):
        raise ShutdownError(f"Не удалось отменить выключение (код {code})")
    allow_sleep()
