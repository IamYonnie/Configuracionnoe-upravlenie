@echo off
echo ========================================
echo    ТЕСТИРОВАНИЕ ЭМУЛЯТОРА
echo ========================================
echo.

echo 1. Тест с параметрами командной строки:
python terminal_emulator.py --vfs-path "./test_vfs" --startup-script "./scripts/test1.txt"

echo.
echo Тест завершен!
pause