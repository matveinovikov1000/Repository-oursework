def decorator(func):
    """Декоратор для записи результата работы функции в файл"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("src/result_reports", "w", encoding="utf8") as file:
            file.write(str(result))
    return wrapper
