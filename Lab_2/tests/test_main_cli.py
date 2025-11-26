from unittest.mock import MagicMock
from lab import main

def test_cli_add_and_show_scenario(monkeypatch, capsys):

    """
    Тестирует сценарий: 
    показать всех (пусто), 
    добавить студента
    показать всех снова (студент на месте), 
    выйти
    """

    inputs = [
        "3",
        "4",
        "101",
        "Тестовый",
        "3",
        "0"
    ]
    
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))
    
    monkeypatch.setattr(main.io_utils, 'load_students_from_csv', MagicMock(return_value=[]))
    monkeypatch.setattr(main.io_utils, 'save_students_to_csv', MagicMock())

    main.main()

    captured = capsys.readouterr()
    output = captured.out
    
    assert "Список студентов пуст" in output
    assert "Студент 'Тестовый' с id 101 добавлен" in output
    assert "Student(id=101, name='Тестовый', grades=[])" in output
    assert "Завершение работы программы..." in output