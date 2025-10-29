from typing import List, Optional
from .models import Student
from . import io_utils
from . import processing
from .errors import (
    StudentAppError, 
    DuplicateStudentIdError, 
    StudentNotFoundError,
    InvalidSortKeyError,
    DataValidationError
)

def handle_load_students(students: List[Student]) -> List[Student]:
    
    """Загрузка студентов из файла"""
    
    filepath = input("Введите путь к CSV файлу для загрузки: ").strip()
    header_choice = input("В файле есть заголовок (y/n): ").strip().lower()
    has_header = (header_choice == 'y')
    try:
        loaded_students = io_utils.load_students_from_csv(filepath, has_header=has_header)
        print(f"Загружено {len(loaded_students)} студентов")
        return loaded_students
    except FileNotFoundError as e:
        print(f"Ошибка: не удалось загрузить файл: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    return students

def handle_save_students(students: List[Student]):
    
    """Сохранение студентов в файл"""
    
    if not students:
        print("Список студентов пуст")
        return

    filepath = input("Введите путь к CSV файлу для сохранения: ").strip()
    header_choice = input("В файле есть заголовок (y/n): ").strip().lower()
    has_header = (header_choice == 'y')
    try:
        io_utils.save_students_to_csv(filepath, students, has_header=has_header)
        print(f"Данные сохранены в файл '{filepath}'")
    except IOError as e:
        print(f"Ошибка: Не удалось сохранить файл: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

def handle_show_all(students: List[Student]):
    
    """Показ всех студентов"""
    
    print("\n--- Список всех студентов ---\n")
    if not students:
        print("Список студентов пуст")
    else:
        for s in students:
            print(s)
    print("---------------------------")

def handle_add_student(students: List[Student]):
    
    """Добавление нового студента"""
    
    try:
        student_id_str = input("Введите id: ").strip()
        student_id = int(student_id_str)
        name = input("Введите ФИО: ").strip()
        processing.add_student(students, name, student_id)
        print(f"Студент '{name}' с id {student_id} добавлен")

    except ValueError:
        print("Ошибка: id должен быть целым числом")
    except DuplicateStudentIdError as e:
        print(f"Ошибка: {e}")
    except StudentAppError as e:
        print(f"Ошибка: {e}")

def handle_remove_student(students: List[Student]):

    """Удаление студента по id"""

    try:
        student_id_str = input("Введите id студента для удаления: ").strip()
        student_id = int(student_id_str)
        processing.remove_student(students, student_id)
        print(f"Студент с id {student_id} удален")

    except ValueError:
        print("Ошибка: id должен быть целым числом")
    except StudentNotFoundError as e:
        print(f"Ошибка: {e}")
    except StudentAppError as e:
        print(f"Ошибка: {e}")

def handle_update_grades(students: List[Student]):
    
    """Обновление оценок студента"""
    
    try:
        student_id_str = input("Введите id студента: ").strip()
        student_id = int(student_id_str)
        
        student = processing.find_student_by_id(students, student_id)
        if student is None:
            raise StudentNotFoundError(f"Студент с id {student_id} не найден")
            
        print(f"Текущие оценки для {student.name}: {student.grades}")
        grades_str = input("Введите новый список оценок через пробел: ").strip()

        if not grades_str:
            new_grades = []
        else:
            new_grades = [int(g) for g in grades_str.split()]

        processing.update_grades(student_id, new_grades, students)
        print(f"Оценки для студента с id {student_id} обновлены")

    except ValueError:
        print("Ошибка: ID и оценки должны быть целыми числами")
    except DataValidationError as e:
        print(f"Ошибка ввода данных: {e}")
    except StudentNotFoundError as e:
        print(f"Ошибка: {e}")
    except StudentAppError as e:
        print(f"Ошибка: {e}")

def handle_show_statistics(students: List[Student]):
    
    """Показ статистики по группе"""
    
    if not students:
        print("\nСписок студентов пуст")
        return

    stats = processing.get_full_statistics(students)

    print("\n--- Статистика по группе ---\n")
    print(f"Всего студентов: {stats['count']}")
    print(f"Общий средний балл: {stats['overall_average']:.2f}")

    if stats['best_student']:
        best = stats['best_student']
        print(f"Лучший студент: {best.name} (средний балл: {best.average:.2f})")
    else:
        print("Лучший студент: невозможно определить")

    if stats['worst_student']:
        worst = stats['worst_student']
        print(f"Худший студент: {worst.name} (средний балл: {worst.average:.2f})")
    else:
        print("Худший студент: невозможно определить")
    print("---------------------------")

def handle_sort_students(students: List[Student]):
    
    """Сортировка и показ студентов"""
    
    if not students:
        print("\nСписок студентов пуст")
        return

    sort_key = input("Введите ключ для сортировки [id, name, avg]: ").strip().lower()

    try:
        sorted_list = processing.sort_students(students, sort_key)
        
        print(f"Студенты, отсортированные по '{sort_key}'")
        for s in sorted_list:
            print(s)
        print("---------------------------")

    except InvalidSortKeyError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

def handle_export_top_students(students: List[Student]):
    
    """Экспорт лучших студентов в csv"""
    
    if not students:
        print("\nСписок студентов пуст")
        return
        
    try:
        n_str = input("Введите количество студентов (N): ").strip()
        n = int(n_str)
        if n <= 0:
            print("Ошибка: N должно быть положительным числом")
            return

        filepath = input(f"Введите путь к файлу для экспорта: ").strip()

        io_utils.export_top_students_to_csv(filepath, students, n)
        print(f"Студенты экспортированы в файл '{filepath}'")

    except ValueError:
        print("Ошибка: N должно быть целым числом")
    except IOError as e:
        print(f"Ошибка: Не удалось сохранить файл: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def print_menu():
    """Печать меню"""
    
    print("\n--- Меню управления студентами ---\n")
    print("1. Загрузить студентов из CSV")
    print("2. Сохранить студентов в CSV")
    print("3. Показать всех студентов")
    print("4. Добавить студента")
    print("5. Удалить студента по ID")
    print("6. Обновить оценки студента по ID")
    print("7. Показать статистику по группе")
    print("8. Экспорт ТОП-N студентов в CSV")
    print("9. Сортировать и показать студентов")
    print("0. Выход")
    print("---------------------------")

def main():    
    students: List[Student] = []
    
    while True:
        print_menu()
        choice = input("Введите номер пункта меню: ").strip()

        if choice == '0':
            print("Завершение работы программы...")
            break
        elif choice == '1':
            students = handle_load_students(students)
        elif choice == '2':
            handle_save_students(students)
        elif choice == '3':
            handle_show_all(students)
        elif choice == '4':
            handle_add_student(students)
        elif choice == '5':
            handle_remove_student(students) 
        elif choice == '6':
            handle_update_grades(students)
        elif choice == '7':
            handle_show_statistics(students) 
        elif choice == '8':
            handle_export_top_students(students)
        elif choice == '9':
            handle_sort_students(students)
        else:
            print("Неверный пункт меню")

if __name__ == "__main__":
    main()