from src.decorators import decorator


def test_decorator():
    @decorator
    def function():
        """Функция для теста декоратора"""
        return "My function is OK"

    result = function()
    assert result is None
