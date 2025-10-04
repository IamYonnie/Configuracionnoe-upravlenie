import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import socket
import sys
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


class SimpleTerminalEmulator:
    def __init__(self, root, vfs_path=None, startup_script=None, config_file=None):
        self.root = root
        self.debug_mode = True

        self.config = {
            'vfs_path': vfs_path,
            'startup_script': startup_script,
            'config_file': config_file
        }

        self.load_configuration()

        self.debug_print("=== ДЕБАГ ИНФОРМАЦИЯ ===")
        self.debug_print(f"Параметры командной строки:")
        self.debug_print(f"  VFS путь: {vfs_path}")
        self.debug_print(f"  Стартовый скрипт: {startup_script}")
        self.debug_print(f"  Конфиг файл: {config_file}")
        self.debug_print(f"Финальная конфигурация:")
        self.debug_print(f"  VFS путь: {self.config['vfs_path']}")
        self.debug_print(f"  Стартовый скрипт: {self.config['startup_script']}")
        self.debug_print("========================")

        self.init_vfs()
        self.create_interface()

        if self.config['startup_script']:
            self.execute_startup_script()

    def load_configuration(self):
        config_file = self.config['config_file']

        if config_file and os.path.exists(config_file):
            try:
                self.debug_print(f"Загрузка конфигурации из файла: {config_file}")
                tree = ET.parse(config_file)
                root = tree.getroot()

                vfs_from_file = root.find('vfs_path')
                script_from_file = root.find('startup_script')

                if vfs_from_file is not None and vfs_from_file.text:
                    self.config['vfs_path'] = vfs_from_file.text
                    self.debug_print(f"VFS путь из конфига: {vfs_from_file.text}")

                if script_from_file is not None and script_from_file.text:
                    self.config['startup_script'] = script_from_file.text
                    self.debug_print(f"Скрипт из конфига: {script_from_file.text}")

            except Exception as e:
                self.debug_print(f"Ошибка загрузки конфига: {e}")

    def init_vfs(self):
        vfs_path = self.config['vfs_path']
        if vfs_path:
            try:
                os.makedirs(vfs_path, exist_ok=True)
                self.debug_print(f"VFS инициализирована: {vfs_path}")

                base_dirs = ['home', 'bin', 'etc', 'tmp']
                for dir_name in base_dirs:
                    dir_path = os.path.join(vfs_path, dir_name)
                    os.makedirs(dir_path, exist_ok=True)

            except Exception as e:
                self.debug_print(f"Ошибка инициализации VFS: {e}")

    def create_interface(self):
        username = 'Gorovenko'
        self.root.title(f"Эмулятор - {username}")
        self.root.geometry("800x600")

        self.output = scrolledtext.ScrolledText(
            self.root,
            bg='white',
            fg='pink',
            font=('Courier New', 12)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.output.config(state='disabled')

        input_frame = tk.Frame(self.root, bg='white')
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt = tk.Label(
            input_frame,
            text="Gorovenko:~ ",
            bg='white',
            fg='pink',
            font=('Courier New', 12)
        )
        self.prompt.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            input_frame,
            bg='white',
            fg='pink',
            font=('Courier New', 12),
            width=80
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.process_command)
        self.entry.focus()

        self.print_text("=== Продвинутый эмулятор терминала ===")
        self.print_text("Доступные команды: ls, cd, run, vfs_info, exit")

    def debug_print(self, message):
        if self.debug_mode:
            print(f"[DEBUG] {message}")

    def print_text(self, text):
        self.output.config(state='normal')
        self.output.insert(tk.END, text + '\n')
        self.output.see(tk.END)
        self.output.config(state='disabled')

    def execute_startup_script(self):
        script_path = self.config['startup_script']
        if script_path and os.path.exists(script_path):
            self.print_text(f"=== Выполнение стартового скрипта: {script_path} ===")
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    command = line.strip()
                    if command and not command.startswith('#'):
                        self.print_text(f"[Скрипт строка {line_num}] {command}")
                        success = self.execute_script_command(command)
                        if not success:
                            self.print_text(f"ОШИБКА: Скрипт остановлен на строке {line_num}")
                            break

            except Exception as e:
                self.print_text(f"Ошибка выполнения скрипта: {e}")
        else:
            self.print_text(f"Стартовый скрипт не найден: {script_path}")

    def execute_script_command(self, command):
        parts = command.strip().split()
        if not parts:
            return True

        cmd = parts[0]
        args = parts[1:]

        try:
            if cmd == "ls":
                self.print_text(f"ls: аргументы - {args}")
                return True
            elif cmd == "cd":
                self.print_text(f"cd: переход в {args[0] if args else 'home'}")
                return True
            elif cmd == "run":
                if args:
                    self.print_text(f"run: выполнение команды ОС: {' '.join(args)}")
                    return True
                else:
                    self.print_text("ОШИБКА: run требует аргументы")
                    return False
            elif cmd == "vfs_info":
                vfs_path = self.config['vfs_path'] or "Не задан"
                self.print_text(f"VFS путь: {vfs_path}")
                return True
            elif cmd == "error_test":
                self.print_text("Тестовая ошибка")
                return False
            else:
                self.print_text(f"Неизвестная команда в скрипте: {cmd}")
                return False
        except Exception as e:
            self.print_text(f"Ошибка выполнения '{command}': {e}")
            return False

    def process_command(self, event):
        command_text = self.entry.get()
        self.entry.delete(0, tk.END)

        self.print_text(f"Gorovenko:~ {command_text}")

        parts = command_text.strip().split()
        if not parts:
            return

        command = parts[0]
        args = parts[1:]

        if command == "exit":
            self.root.quit()
        elif command == "ls":
            self.print_text(f"ls: аргументы - {args}")
        elif command == "cd":
            self.print_text(f"cd: аргументы - {args}")
        elif command == "vfs_info":
            vfs_path = self.config['vfs_path'] or "Не задан"
            script_path = self.config['startup_script'] or "Не задан"
            self.print_text(f"Информация о конфигурации:")
            self.print_text(f"  VFS путь: {vfs_path}")
            self.print_text(f"  Стартовый скрипт: {script_path}")
        elif command == "run":
            if args:
                self.print_text(f"Выполнение команды ОС: {' '.join(args)}")
            else:
                self.print_text("Ошибка: команда run требует аргументы")
        else:
            self.print_text(f"Ошибка: команда '{command}' не найдена")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Эмулятор терминала')
    parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
    parser.add_argument('--startup-script', help='Путь к стартовому скрипту')
    parser.add_argument('--config-file', help='Путь к конфигурационному файлу')

    return parser.parse_args()


def main():
    args = parse_arguments()

    root = tk.Tk()
    app = SimpleTerminalEmulator(
        root,
        vfs_path=args.vfs_path,
        startup_script=args.startup_script,
        config_file=args.config_file
    )
    root.mainloop()


if __name__ == "__main__":
    main()