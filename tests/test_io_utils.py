import pytest
import csv
from lab import io_utils
from lab.models import Student

def test_csv_roundtrip(sample_students, tmp_path):

    """
    Тест сохраняем студентов в CSV, а затем загружаем
    """

    filepath = tmp_path / "students.csv"
    
    io_utils.save_students_to_csv(filepath, sample_students)
    
    loaded_students = io_utils.load_students_from_csv(filepath)
    
    loaded_students.sort(key=lambda s: s.student_id)
    sample_students.sort(key=lambda s: s.student_id)
    
    assert len(loaded_students) == len(sample_students)
    for original, loaded in zip(sample_students, loaded_students):
        assert original.student_id == loaded.student_id
        assert original.name == loaded.name
        assert original.grades == loaded.grades

def test_load_with_validation_errors(tmp_path, capsys):
    
    """
    Тест загрузки csv файла с некорректными данными
    """
    
    csv_content = (
        "id,name,grade1,grade2\n"
        "1,Иванов,80,90\n"
        "2,Петров,101,88\n"
        "invalid_id,Сидоров,70,75\n"
        "4,,60,65\n"
        "1,Смирнов,77,88\n"
        "5,Кузнецов,80,\n"
    )
    filepath = tmp_path / "bad_data.csv"
    filepath.write_text(csv_content, encoding='utf-8')

    students = io_utils.load_students_from_csv(filepath)
    
    assert len(students) == 2
    assert students[0].student_id == 1
    assert students[1].student_id == 5
    assert students[1].grades == [80]
    
    captured = capsys.readouterr()
    assert "строка 4" in captured.out and "id должен быть целым числом" in captured.out
    assert "строка 5" in captured.out and "имя не может быть пустым" in captured.out
    assert "строка 6" in captured.out and "дубликат id 1" in captured.out

def test_export_top_students(sample_students, tmp_path):
    
    """Тест экспорта N лучших студентов"""
    
    filepath = tmp_path / "top_students.csv"
    N = 2
    
    io_utils.export_top_students_to_csv(filepath, sample_students, N)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'name', 'average', 'grades']
        
        rows = list(reader)
        assert len(rows) == N
        assert rows[1][0] == '1'