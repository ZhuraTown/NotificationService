from dataclasses import dataclass
from fastapi.exceptions import ValidationException


@dataclass
class ToClientException(ValidationException):
    errors: str = "Validation errors"

    @property
    def message(self):
        return self.errors
