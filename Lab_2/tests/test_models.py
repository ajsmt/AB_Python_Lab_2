from lab.models import Student

def test_student_creation():
    
    """Тест на корректное создание объекта Student"""
    
    s = Student(id=1, name="Тест", grades=[80, 90])
    assert s.student_id == 1
    assert s.name == "Тест"
    assert s.grades == [80, 90]

def test_student_average_calculation():
    
    """Тест на корректный расчет среднего балла"""
    
    s = Student(id=1, name="Тест", grades=[80, 90, 100])
    assert s.average == 90.0

def test_student_average_with_no_grades():
    
    """Тест расчета среднего для студента без оценок"""
    
    s = Student(id=1, name="Тест", grades=[])
    assert s.average == 0.0

def test_student_average_with_none_grades():
    
    """Тест, что при создании студента без оценок список grades пустой"""
    
    s = Student(id=1, name="Тест") 
    assert s.grades == []
    assert s.average == 0.0