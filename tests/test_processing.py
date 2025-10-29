import pytest
from lab import processing
from lab.errors import (
    DuplicateStudentIdError,
    StudentNotFoundError,
    InvalidSortKeyError,
    DataValidationError
)

def test_find_student_by_id(sample_students):
    
    """Тест поиска существующего и несуществующего студента"""
    
    assert processing.find_student_by_id(sample_students, 1) is not None
    assert processing.find_student_by_id(sample_students, 99) is None

def test_add_student(sample_students):
    
    """Тест успешного добавления студента"""
    
    processing.add_student(sample_students, "Новый", 4)
    assert len(sample_students) == 4
    assert processing.find_student_by_id(sample_students, 4).name == "Новый"

def test_add_student_with_duplicate_id_raises_error(sample_students):
    
    """Тест добавления студента с существующим ID"""
    
    with pytest.raises(DuplicateStudentIdError):
        processing.add_student(sample_students, "Дубликат", 1)

def test_remove_student(sample_students):
    
    """Тест удаления студента"""
    
    processing.remove_student(sample_students, 1)
    assert len(sample_students) == 2
    assert processing.find_student_by_id(sample_students, 1) is None

def test_remove_nonexistent_student_raises_error(sample_students):
    
    """Тест удаления несуществующего студента"""
    
    with pytest.raises(StudentNotFoundError):
        processing.remove_student(sample_students, 99)

def test_update_grades(sample_students):
    
    """Тест обновления оценок существующего студента"""
    
    processing.update_grades(1, [100, 100, 100], sample_students)
    student = processing.find_student_by_id(sample_students, 1)
    assert student.grades == [100, 100, 100]

def test_update_grades_invalid_grade_raises_error(sample_students):
    
    """Тест обновления на невалидные оценки"""
    
    with pytest.raises(DataValidationError):
        processing.update_grades(1, [101], sample_students)


def test_statistics(sample_students):
    
    """Тест на корректность полной статистики"""
    
    stats = processing.get_full_statistics(sample_students)
    assert stats["count"] == 3
    assert stats["overall_average"] == pytest.approx(73.67, abs=0.01)    
    assert stats["best_student"].student_id == 3
    assert stats["worst_student"].student_id == 2


def test_statistics_on_empty_list(sample_empty_students_list):
    
    """Тест статистики на пустом списке"""
    
    stats = processing.get_full_statistics(sample_empty_students_list)
    assert stats["count"] == 0
    assert stats["overall_average"] == 0.0
    assert stats["best_student"] is None
    assert stats["worst_student"] is None
    
def test_sort_students_by_id(sample_students):
    
    """Тест сортировки по ID"""
    
    sorted_list = processing.sort_students(sample_students, 'id')
    ids = [s.student_id for s in sorted_list]
    assert ids == [1, 2, 3]

def test_sort_students_by_name(sample_students):
    
    """Тест сортировки по имени"""
    
    sorted_list = processing.sort_students(sample_students, 'name')
    names = [s.name for s in sorted_list]
    assert names == ["Иванов Иван", "Иванов Петр", "Иванова Анна"]

def test_sort_students_by_avg(sample_students):
    
    """Тест сортировки по среднему баллу"""
    
    from lab.models import Student
    sample_students.append(Student(id=4, name="Сидоров Сидор", grades=[80, 89, 84]))
    
    sorted_list = processing.sort_students(sample_students, 'avg')
    ids = [s.student_id for s in sorted_list]
    assert ids == [3, 1, 4, 2]

def test_sort_with_invalid_key_raises_error(sample_students):
    
    """Тест сортировки по неверному ключу"""
    
    with pytest.raises(InvalidSortKeyError):
        processing.sort_students(sample_students, 'lastname')