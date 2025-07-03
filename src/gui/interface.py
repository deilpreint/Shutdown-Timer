# gui/interface.py
import tkinter as tk
from tkinter import ttk, messagebox
import logic

def on_entry_focus_in(entry):
    if entry.get() == "0":
        entry.delete(0, tk.END)

def on_entry_focus_out(entry):
    if entry.get() == "":
        entry.insert(0, "0")

def create_app():
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

    root = tk.Tk()
    dark_bg = '#1c1c1e'
    dark_fg = '#f2f2f7'
    accent_green = '#32d74b'
    accent_red = '#ff453a'
    secondary_fg = '#8e8e93'
    root.configure(bg=dark_bg)
    root.title("Shutdown Timer")
    root.iconbitmap('icon.ico')  # Установите путь к значку, если есть
    root.geometry("400x250")
    root.resizable(False, False)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    style = ttk.Style(root)
    style.theme_use('default')

    style.configure('Green.TButton',
                    background=accent_green,
                    foreground='black',
                    font=('Arial', 12, 'bold'),
                    borderwidth=0)
    style.map('Green.TButton',
              background=[('active', '#28cd41')])

    style.configure('Red.TButton',
                    background=accent_red,
                    foreground='black',
                    font=('Arial', 12, 'bold'),
                    borderwidth=0)
    style.map('Red.TButton',
              background=[('active', '#ff3b30')])

    style.configure('TLabel', font=('Arial', 12), background=dark_bg, foreground=dark_fg)
    style.configure('TEntry', padding=5, fieldbackground='#2c2c2e', foreground=dark_fg)

    ttk.Label(root, text="Часы:").grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 5), sticky='ew')
    entry_hours = ttk.Entry(root, width=5)
    entry_hours.insert(0, "0")
    entry_hours.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_hours))
    entry_hours.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_hours))
    entry_hours.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

    ttk.Label(root, text="Минуты:").grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky='ew')
    entry_minutes = ttk.Entry(root, width=5)
    entry_minutes.insert(0, "0")
    entry_minutes.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_minutes))
    entry_minutes.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_minutes))
    entry_minutes.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky='ew')

    btn_schedule = ttk.Button(root, text="Запланировать", style='Green.TButton', command=schedule)
    btn_schedule.grid(row=4, column=0, columnspan=2, pady=20, ipadx=10, ipady=5, sticky='ew')

    btn_cancel = ttk.Button(root, text="Отменить", style='Red.TButton', command=cancel)
    btn_cancel.grid(row=5, column=0, columnspan=2, pady=10, ipadx=10, ipady=5, sticky='ew')

    ttk.Label(root, text="Shutdown Timer © 2025", font=('Arial', 9), foreground=secondary_fg, background=dark_bg).grid(
        row=6, column=0, columnspan=2, pady=(20, 5))

    root.mainloop()
