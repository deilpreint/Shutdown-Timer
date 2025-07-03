import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import logic

current_theme = "light"

def create_app():
    global root
    root = tk.Tk()
    root.title("Shutdown Timer")
    root.geometry("480x300")
    root.resizable(False, False)

    apply_theme("light")

    icon_path = os.path.join(os.path.dirname(__file__), "settings.png")
    try:
        settings_icon = Image.open(icon_path).resize((24, 24))
        settings_photo = ImageTk.PhotoImage(settings_icon)
    except Exception as e:
        print("Ошибка загрузки иконки:", e)
        settings_photo = None

    settings_btn = tk.Button(root, image=settings_photo, command=open_settings,
                             bd=0, bg=root["bg"], activebackground="#eeeeee")
    settings_btn.image = settings_photo
    settings_btn.place(x=440, y=10)

    tk.Label(root, text="Часы:", font=('Arial', 12)).place(x=30, y=40)
    global entry_hours
    entry_hours = tk.Entry(root, width=5, font=('Arial', 12))
    entry_hours.insert(0, "0")
    entry_hours.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_hours))
    entry_hours.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_hours))
    entry_hours.place(x=100, y=40)

    tk.Label(root, text="Минуты:", font=('Arial', 12)).place(x=30, y=80)
    global entry_minutes
    entry_minutes = tk.Entry(root, width=5, font=('Arial', 12))
    entry_minutes.insert(0, "0")
    entry_minutes.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_minutes))
    entry_minutes.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_minutes))
    entry_minutes.place(x=100, y=80)

    btn_schedule = ttk.Button(root, text="Запланировать", command=schedule)
    btn_schedule.place(x=50, y=150, width=150, height=40)

    btn_cancel = ttk.Button(root, text="Отменить", command=cancel)
    btn_cancel.place(x=250, y=150, width=150, height=40)

    root.mainloop()

def apply_theme(theme):
    global current_theme
    current_theme = theme

    bg = "#ffffff" if theme == "light" else "#2e2e2e"
    fg = "#000000" if theme == "light" else "#ffffff"

    if "root" in globals():
        root.configure(bg=bg)
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Entry):
                widget.configure(bg=bg, fg=fg, insertbackground=fg)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton',
                    font=('Arial', 12, 'bold'),
                    foreground=fg,
                    background='#4CAF50' if theme == "light" else '#555',
                    borderwidth=0)
    style.map('TButton',
              background=[('active', '#45a049' if theme == 'light' else '#333')])

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.geometry("300x150")
    settings_window.configure(bg="#ffffff" if current_theme == "light" else "#2e2e2e")

    def toggle_theme():
        new_theme = "dark" if current_theme == "light" else "light"
        apply_theme(new_theme)
        theme_button.config(text=f"Тема: {'Тёмная' if new_theme == 'dark' else 'Светлая'}")
        settings_window.configure(bg="#ffffff" if new_theme == "light" else "#2e2e2e")

    theme_button = tk.Button(settings_window,
                             text=f"Тема: {'Тёмная' if current_theme == 'dark' else 'Светлая'}",
                             command=toggle_theme,
                             font=('Arial', 12),
                             bg="#dddddd" if current_theme == "light" else "#444444",
                             fg="#000000" if current_theme == "light" else "#ffffff")
    theme_button.pack(pady=40)

def on_entry_focus_in(entry):
    if entry.get() == "0":
        entry.delete(0, tk.END)

def on_entry_focus_out(entry):
    if entry.get() == "":
        entry.insert(0, "0")

def schedule():
    try:
        hours = int(entry_hours.get())
        minutes = int(entry_minutes.get())
        logic.schedule_shutdown(hours, minutes)
        messagebox.showinfo("Успех", f"Выключение запланировано через {hours} ч {minutes} мин.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def cancel():
    logic.cancel_shutdown()
    messagebox.showinfo("Отмена", "Выключение отменено.")
