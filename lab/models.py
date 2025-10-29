from typing import List

class Student:
    
    """Модель для представления данных о студенте"""

    
    def __init__(self, id: int, name: str, grades: List[int] = None):
        
        """Конструктор для создания объекта студента"""
        
        self.student_id = id
        self.name = name
        if grades is None:
            self.grades = []
        else:
            self.grades = grades

    def __repr__(self) -> str:
        
        """Строковое представление объекта"""
        
        return f"Student(id={self.student_id}, name='{self.name}', grades={self.grades})"

    def __eq__(self, other) -> bool:
        
        """Сравнение студентов на равенство по id"""
        
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id
    
    @property
    def average(self) -> float:
        
        """
        Рассчитывает средний балл студента
        Возвращает 0.0 если список оценок пуст
        """

        
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)