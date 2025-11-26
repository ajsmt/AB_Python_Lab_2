import csv
from typing import List, Tuple
from .models import Student
from .errors import (
    DataValidationError,
    DuplicateStudentIdInFileError
)

def _parse_and_validate_row(row: List[str], line_num: int) -> Student:
    
    """Парсит и валидирует строку из csv, возвращает Student"""
    
    if len(row) < 2:
        raise DataValidationError(f"Строка {line_num}: Недостаточно данных нужен id и имя")

    try:
        student_id = int(row[0])
    except ValueError:
        raise DataValidationError(f"Строка {line_num}: id должен быть целым числом")

    name = row[1].strip()
    if not name:
        raise DataValidationError(f"Строка {line_num}: имя не может быть пустым")

    grades = []
    for grade_str in row[2:]:
        grade_str = grade_str.strip()
        if not grade_str:
            continue
        try:
            grade = int(grade_str)
            if not (0 <= grade <= 100):
                raise ValueError()
            grades.append(grade)
        except ValueError:
            raise DataValidationError(
                f"Строка {line_num}: оценка должна быть целым числом от 0 до 100"
            )
            
    return Student(id=student_id, name=name, grades=grades)

def load_students_from_csv(filepath: str, has_header: bool = True) -> List[Student]:
    
    """
    Загрузка списка студентов из csv файла
    Пропускает строки с ошибками валидации выводя сообщение в консоль
    :param filepath: путь к файлу для загрузки
    :param has_header: есть ли в файле строка с заголовком (default=True)
    :return: список загруженных объектов Student
    :raises FileNotFoundError: если файл не найден
    """
    
    students = []
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            if has_header:
                try:
                    next(reader)
                except StopIteration:
                    return []

            start_line = 2 if has_header else 1

            for i, row in enumerate(reader, start=start_line):
                try:
                    student = _parse_and_validate_row(row, i)
                    if any(s.student_id == student.student_id for s in students):
                        raise DuplicateStudentIdInFileError(
                            f"дубликат id {student.student_id}"
                        )
                    
                    students.append(student)
                except DataValidationError as e:
                    print(f"Предупреждение: строка {i} пропущена. Ошибка: {e}")

    except FileNotFoundError:
        raise FileNotFoundError(f"Ошибка: файл '{filepath}' не найден")
    return students


def save_students_to_csv(filepath: str, students: List[Student], has_header: bool = True):
    
    """
    Сохраняет список студентов в CSV-файл
    :param filepath: путь к файлу для сохранения
    :param students: список объектов Student для сохранения
    :param has_header: Записывать ли строку с заголовком (default=True)
    """
    if not students:
        max_grades = 0
    else:
        max_grades = max(len(s.grades) for s in students)

    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if has_header:
            header = ['id', 'name'] + [f'grade{i+1}' for i in range(max_grades)]
            writer.writerow(header)

        for student in students:
            grades_str = [str(g) for g in student.grades]
            padded_grades = grades_str + [''] * (max_grades - len(grades_str))
            row = [str(student.student_id), student.name] + padded_grades
            writer.writerow(row)

def export_top_students_to_csv(filepath: str, students: List[Student], n: int):
    
    """
    Сортирует студентов по убыванию среднего балла и экспортирует N лучших в csv файл

    :param filepath: путь к файлу для сохранения
    :param students: список всех студентов
    :param n: количество лучших студентов для экспорта
    """
    
    sorted_students = sorted(students, key=lambda s: (-s.average, s.name))
    
    top_n_students = sorted_students[:n]

    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        header = ['id', 'name', 'average', 'grades']
        writer.writerow(header)

        for student in top_n_students:
            grades_str = ' '.join(map(str, student.grades))
            
            row = [
                student.student_id,
                student.name,
                f"{student.average:.2f}",
                grades_str
            ]
            writer.writerow(row)
