import pytest
from lab.models import Student

@pytest.fixture
def sample_students():
    
    """Фикстура, предоставляющая тестовый список студентов"""
    
    return [
        Student(id=3, name="Иванова Анна", grades=[92, 88, 95]),
        Student(id=1, name="Иванов Иван", grades=[78, 85, 90]),
        Student(id=2, name="Иванов Петр", grades=[65, 70, 0]),
    ]

@pytest.fixture
def sample_empty_students_list():
    
    """Фикстура, предоставляющая пустой список студентов"""
    
    return []