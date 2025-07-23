from fastapi import HTTPException


class DomickException(Exception):
    detail = ""

    def __init__(self, *args):
        if args:
            self.detail = args[0]
        else:
            self.detail = None

    def __str__(self):
        if self.detail:
            return f"{self.__class__.__name__}, {self.detail}"
        else:
            return f"{self.__class__.__name__}"


class BookingRoomNotAvailableException(DomickException):
    detail = "Комната недоступна для бронирования"


class DateFromLaterDateToException(DomickException):
    detail = "Дата заезда позже даты выезда"


class EditedTooMatchObjects(DomickException):
    detail = "Отредактировано слишком много объектов"


class ObjectAlreadyExistsException(DomickException):
    detail = "Объект уже существует в БД"


class ObjectNotFoundException(DomickException):
    detail = "Объект не был найден в БД"


class RoomNotFoundException(DomickException):
    detail = "Номер не найден в БД"


class HotelNotFoundException(DomickException):
    detail = "Отель не найден в БД"


class AuthTokenErrorException(DomickException):
    detail = "Неверный токен"


class DomickHTTPException(HTTPException):
    status_code = 500
    detail = None


class HotelNotFoundHTTPException(DomickHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(DomickHTTPException):
    status_code = 404
    detail = "Номер не найден"


class DateFromLaterDateToHTTPException(DomickHTTPException):
    status_code = 422
    detail = "Дата заезда не может быть позже даты выезда"
