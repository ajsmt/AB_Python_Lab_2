from typing import (
    List, 
    Optional, 
    Dict, 
    Any
)
from .models import Student
from .errors import (
    StudentNotFoundError,
    DuplicateStudentIdError,
    InvalidSortKeyError,
    DataValidationError
)


def find_student_by_id(students: List[Student], student_id: int) -> Optional[Student]:
    
    """
    Поиск студента в списке по его id
    :param students: список студентов для поиска
    :param student_id: id искомого студента
    """
    
    for student in students:
        if student.student_id == student_id:
            return student
    return None

def add_student(students: List[Student], name: str, student_id: int):
    
    """
    Добавление нового студента в список
    :param students: Список студентов
    :param name: ФИО нового студента
    :param student_id: id нового студента
    :raises DuplicateStudentIdError: если студент с таким id уже существует
    """
    
    if find_student_by_id(students, student_id) is not None:
        raise DuplicateStudentIdError(f"Студент с id {student_id} уже существует")
    new_student = Student(id=student_id, name=name)
    students.append(new_student)

def remove_student(students: List[Student], student_id: int):
    
    """
    Удаляет студента из списка по его ID
    :param students: cписок студентов
    :param student_id: id студента для удаления
    :raises StudentNotFoundError: если студент с таким id не найден
    """

    student_to_remove = find_student_by_id(students, student_id)
    if student_to_remove is None:
        raise StudentNotFoundError(f"Студент с ID {student_id} не найден")
    students.remove(student_to_remove)

def update_grades(student_id: int, new_grades: List[int], students: List[Student]):
    
    """
    Обновляет список оценок для указанного студента
    предварительно валидируя их
    """
    
    student_to_update = find_student_by_id(students, student_id)
    if student_to_update is None:
        raise StudentNotFoundError(f"Студент с ID {student_id} не найден")
    for grade in new_grades:
        if not isinstance(grade, int) or not (0 <= grade <= 100):
            raise DataValidationError(
                f"Ошибка: оценка '{grade}' не является целым числом от 0 до 100"
            )
    student_to_update.grades = new_grades

def get_student_count(students: List[Student]) -> int:
    
    """Количество студентов в списке"""
    
    return len(students)


def get_overall_average(students: List[Student]) -> float:
    
    """Cредний балл по всем оценкам всех студентов"""
    
    all_grades = [grade for student in students for grade in student.grades]
    if not all_grades:
        return 0.0
    return sum(all_grades) / len(all_grades)


def get_best_student(students: List[Student]) -> Optional[Student]:
    
    """
    Поиск лучшего студента по среднему баллу
    Возвращает None, если список студентов пуст
    """
    
    if not students:
        return None
    return max(students, key=lambda student: student.average)


def get_worst_student(students: List[Student]) -> Optional[Student]:
    
    """
    Поиск худшего студента по среднему баллу
    Возвращает None, если список студентов пуст
    """

    if not students:
        return None
    return min(students, key=lambda student: student.average)

def get_full_statistics(students: List[Student]) -> Dict[str, Any]:
    
    """
    Сбор полной статистики по группе
    :param students: список студентов для анализа
    """
    
    count = get_student_count(students)
    overall_avg = get_overall_average(students)
    best_student = get_best_student(students)
    worst_student = get_worst_student(students)
    
    return {
        "count": count,
        "overall_average": overall_avg,
        "best_student": best_student,
        "worst_student": worst_student
    }

def sort_students(students: List[Student], sort_by: str) -> List[Student]:
    
    """
    Сортировка список студентов по указанному ключу
    :param students: список студентов для сортировки
    :param sort_by: ключ для сортировки ['id', 'name' или 'avg']
    :raises InvalidSortKeyError: если передан неверный ключ сортировки
    """
    
    if sort_by == 'id':
        return sorted(students, key=lambda student: student.student_id)
    elif sort_by == 'name':
        return sorted(students, key=lambda student: student.name)
    elif sort_by == 'avg':
        return sorted(students, key=lambda student: (-student.average, student.name))
    else:
        raise InvalidSortKeyError("Неверный ключ сортировки")
