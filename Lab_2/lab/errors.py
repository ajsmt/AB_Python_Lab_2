class StudentAppError(Exception):

    """Базовый класс для всех исключений"""

    pass

class StudentNotFoundError(StudentAppError):

    """Исключение когда студент не найден по id"""

    pass

class DuplicateStudentIdError(StudentAppError):

    """Исключение при попытке добавить студента с существующим id"""

    pass

class InvalidSortKeyError(StudentAppError):

    """Исключение при передаче неверного ключа для сортировки"""

    pass

class DataValidationError(StudentAppError):

    """Исключение при ошибках валидации данных в csv файле"""

    pass

class DuplicateStudentIdInFileError(DataValidationError):
    
    """Исключение при обнаружении дубликата id в csv файле"""
    
    pass
