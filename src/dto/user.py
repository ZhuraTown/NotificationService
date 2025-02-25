from dto.base import BaseDTO


class CreateUser(BaseDTO):
    username: str
    password: str


class UserCreated(BaseDTO):
    id: int
    username: str


class UserRead(UserCreated):
    ...


class LoginCreate(BaseDTO):
    username: str
    password: str


class JWTTokenResponse(BaseDTO):
    access_token: str
