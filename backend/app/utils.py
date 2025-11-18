class ReprMixin:
    # Представлення моделі у форматі <ModelName>(field1=value1, field2=value2, ...)
    def __repr__(self) -> str:
        try:
            return f"{self.__class__.__name__}({', '.join([f'{key}={value}' for key, value in list(self.__dict__.items())[1:]])})"
        except Exception as e:
            return f"Error in __repr__: {e}"
