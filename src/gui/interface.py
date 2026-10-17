import math
import time
from tkinter import messagebox

import customtkinter as ctk

import logic

BG = "#1c1c1e"
CARD = "#2c2c2e"
CARD_HOVER = "#3a3a3c"
TEXT = "#f2f2f7"
GRAY = "#8e8e93"
GREEN, GREEN_HOVER = "#32d74b", "#28cd41"
RED, RED_HOVER = "#ff453a", "#ff3b30"

FONT = "Segoe UI"
PRESETS = [("15 мин", 15), ("30 мин", 30), ("1 час", 60), ("2 часа", 120)]


def font(size, weight="normal"):
    return ctk.CTkFont(family=FONT, size=size, weight=weight)


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG)
        self.title("Shutdown Timer")
        self.geometry("360x470")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, minsize=42)

        self.end_time = None
        self.tick_job = None

        self._build()
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def _build(self):
        ctk.CTkLabel(self, text="Выключить через", font=font(15), text_color=GRAY).grid(
            row=0, column=0, pady=(34, 10))

        self.display = ctk.CTkFrame(self, fg_color="transparent", width=320, height=90)
        self.display.grid(row=1, column=0)
        self.display.grid_propagate(False)
        self.display.columnconfigure(0, weight=1)

        self.inputs = ctk.CTkFrame(self.display, fg_color="transparent")
        self.hours = self._entry(self.inputs, 0)
        ctk.CTkLabel(self.inputs, text="ч", font=font(18), text_color=GRAY).grid(row=0, column=1, padx=(6, 18))
        self.minutes = self._entry(self.inputs, 2)
        ctk.CTkLabel(self.inputs, text="мин", font=font(18), text_color=GRAY).grid(row=0, column=3, padx=(6, 0))
        self.inputs.grid(row=0, column=0, pady=10)

        self.countdown = ctk.CTkLabel(self.display, text="00:00:00", font=font(54, "bold"), text_color=TEXT)

        self.presets = ctk.CTkFrame(self, fg_color="transparent")
        self.presets.grid(row=2, column=0, pady=(10, 0))
        for i, (label, total_minutes) in enumerate(PRESETS):
            ctk.CTkButton(
                self.presets, text=label, width=66, height=32, corner_radius=10,
                font=font(13), fg_color=CARD, hover_color=CARD_HOVER, text_color=TEXT,
                command=lambda m=total_minutes: self._apply_preset(m),
            ).grid(row=0, column=i, padx=4)

        self.status = ctk.CTkLabel(self, text="", font=font(14), text_color=GRAY,
                                   wraplength=300, height=44)
        self.status.grid(row=3, column=0, pady=(22, 8))

        self.button = ctk.CTkButton(
            self, text="Запустить", height=54, width=300, corner_radius=14,
            font=font(17, "bold"), text_color="black",
            fg_color=GREEN, hover_color=GREEN_HOVER, command=self._toggle,
        )
        self.button.grid(row=4, column=0, pady=(0, 24))

    def _entry(self, parent, column):
        entry = ctk.CTkEntry(
            parent, width=92, height=64, justify="center", font=font(32, "bold"),
            fg_color=CARD, border_width=0, corner_radius=14, text_color=TEXT,
            placeholder_text="0", placeholder_text_color=GRAY,
        )
        entry.grid(row=0, column=column)
        return entry


    def _show_running(self):
        self.inputs.grid_remove()
        self.presets.grid_remove()
        self.countdown.grid(row=0, column=0, pady=10)
        self.button.configure(text="Отменить", fg_color=RED, hover_color=RED_HOVER)
        at = time.strftime("%H:%M", time.localtime(self.end_time))
        self._set_status(f"Компьютер выключится в {at}\nСон отключён, пока идёт отсчёт")

    def _show_idle(self, message="", color=GRAY):
        self.countdown.grid_remove()
        self.inputs.grid(row=0, column=0, pady=10)
        self.presets.grid()
        self.button.configure(text="Запустить", fg_color=GREEN, hover_color=GREEN_HOVER)
        self._set_status(message, color)

    def _set_status(self, text, color=GRAY):
        self.status.configure(text=text, text_color=color)


    def _apply_preset(self, total_minutes):
        hours, minutes = divmod(total_minutes, 60)
        for entry, value in ((self.hours, hours), (self.minutes, minutes)):
            entry.delete(0, "end")
            if value:
                entry.insert(0, str(value))

    def _toggle(self):
        if self.end_time is None:
            self._start()
        else:
            self._cancel()

    def _start(self):
        try:
            seconds = logic.parse_time(self.hours.get(), self.minutes.get())
            logic.schedule_shutdown(seconds)
        except logic.ShutdownError as error:
            self._set_status(str(error), RED)
            return
        self.end_time = time.time() + seconds
        self._show_running()
        self._tick()

    def _cancel(self):
        try:
            logic.cancel_shutdown()
        except logic.ShutdownError as error:
            self._set_status(str(error), RED)
            return
        self._stop_timer()
        self._show_idle("Выключение отменено")

    def _stop_timer(self):
        self.end_time = None
        if self.tick_job is not None:
            self.after_cancel(self.tick_job)
            self.tick_job = None

    def _tick(self):
        remaining = self.end_time - time.time()
        if remaining <= 0:
            self._stop_timer()
            logic.allow_sleep()
            self._show_idle("Время вышло, выключаем компьютер…")
            return
        left = math.ceil(remaining)
        hours, rest = divmod(left, 3600)
        minutes, seconds = divmod(rest, 60)
        self.countdown.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tick_job = self.after(250, self._tick)

    def _on_close(self):
        if self.end_time is not None:
            ok = messagebox.askyesno(
                "Таймер идёт",
                "Выключение останется запланированным, но без программы компьютер "
                "сможет уйти в сон, и отсчёт остановится.\n\nВсё равно закрыть?",
            )
            if not ok:
                return
        logic.allow_sleep()
        self.destroy()


def create_app():
    ctk.set_appearance_mode("dark")
    App().mainloop()