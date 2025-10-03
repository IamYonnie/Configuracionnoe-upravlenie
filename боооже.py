import tkinter as tk
from tkinter import scrolledtext
import os
import socket


class SimpleTerminalEmulator:
    def __init__(self, root):
        self.root = root

        # Заголовок окна
        username = 'Gorovenko'
        self.root.title(f"Эмулятор - {username}@hostname")

        self.current_dir = os.getcwd()
        self.create_interface()

    def create_interface(self):
        # Область вывода
        self.output = scrolledtext.ScrolledText(
            self.root,
            bg='white',
            fg='hot pink',
            font=('Courier New', 12)
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.config(state='disabled')

        # Фрейм ввода
        input_frame = tk.Frame(self.root, bg='white')
        input_frame.pack(fill=tk.X)

        # Приглашение
        self.prompt = tk.Label(
            input_frame,
            text="Gorovenko:~ ",
            bg='white',
            fg='hot pink',
            font=('Courier New', 12)
        )
        self.prompt.pack(side=tk.LEFT)

        # Поле ввода
        self.entry = tk.Entry(
            input_frame,
            bg='white',
            fg='hot pink',
            font=('Courier New', 12)
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.process_command)
        self.entry.focus()

    def process_command(self, event):
        command_text = self.entry.get()
        self.entry.delete(0, tk.END)

        # Выводим команду
        self.print_text(f"Gorovenko:~ {command_text}")

        # Парсер команд
        parts = command_text.strip().split()
        if not parts:
            return

        command = parts[0]
        args = parts[1:]

        # Обработка команд
        if command == "exit":
            self.root.quit()
        elif command == "ls":
            self.print_text(f"ls command with args: {args}")
        elif command == "cd":
            self.print_text(f"cd command with args: {args}")
        else:
            self.print_text(f"Ошибка: команда '{command}' не найдена")

    def print_text(self, text):
        self.output.config(state='normal')
        self.output.insert(tk.END, text + '\n')
        self.output.see(tk.END)
        self.output.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    app = SimpleTerminalEmulator(root)
    root.mainloop()