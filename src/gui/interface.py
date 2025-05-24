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
    root.title("Shutdown Timer")
    root.geometry("450x320")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use('default')

    style.configure('Green.TButton',
                    background='#4CAF50',
                    foreground='white',
                    font=('Arial', 12, 'bold'),
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor='none')
    style.map('Green.TButton',
              background=[('active', '#45a049')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    style.configure('Red.TButton',
                    background='#f44336',
                    foreground='white',
                    font=('Arial', 12, 'bold'),
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor='none')
    style.map('Red.TButton',
              background=[('active', '#d32f2f')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    tk.Label(root, text="Часы:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    entry_hours = tk.Entry(root, width=5, font=('Arial', 12))
    entry_hours.insert(0, "0")
    entry_hours.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_hours))
    entry_hours.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_hours))
    entry_hours.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    tk.Label(root, text="Минуты:", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    entry_minutes = tk.Entry(root, width=5, font=('Arial', 12))
    entry_minutes.insert(0, "0")
    entry_minutes.bind("<FocusIn>", lambda e: on_entry_focus_in(entry_minutes))
    entry_minutes.bind("<FocusOut>", lambda e: on_entry_focus_out(entry_minutes))
    entry_minutes.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    btn_schedule = ttk.Button(root, text="Запланировать", style='Green.TButton', command=schedule)
    btn_schedule.grid(row=2, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

    btn_cancel = ttk.Button(root, text="Отменить", style='Red.TButton', command=cancel)
    btn_cancel.grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

    root.mainloop()

