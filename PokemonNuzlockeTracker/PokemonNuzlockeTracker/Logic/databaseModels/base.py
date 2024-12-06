from sqlalchemy.types import TypeDecorator, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StrictInteger(TypeDecorator):
    """
    Custom type that enforces strict integer validation.
    """
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:  # Allow NULL values
            return value
        if not isinstance(value, int):
            raise ValueError(f"Expected an integer, got {type(value).__name__} with value '{value}'")
        return value
