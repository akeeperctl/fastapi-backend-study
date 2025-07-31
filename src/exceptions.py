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


class EditedTooMatchObjectsException(DomickException):
    detail = "Отредактировано слишком много объектов"


class ObjectAlreadyExistsException(DomickException):
    detail = "Объект уже существует в БД"


class ObjectNotFoundException(DomickException):
    detail = "Объект не был найден в БД"


class ObjectKeyNotCorrectException(DomickException):
    detail = "Некорректный ключ сущности"


class FacilityKeyNotCorrectException(DomickException):
    detail = "Некорректный ключ удобства"


class FacilityAlreadyExistsException(DomickException):
    detail = "Такое удобство уже существует в БД"


class RoomNotFoundException(DomickException):
    detail = "Номер не найден в БД"


class HotelNotFoundException(DomickException):
    detail = "Отель не найден в БД"


class AuthTokenErrorException(DomickException):
    detail = "Неверный токен"


class UserAlreadyExistsException(DomickException):
    detail = "Такой пользователь уже существует в БД"


class UserNotExistsException(DomickException):
    detail = "Такой пользователь не существует"


class UserPasswordWrongException(DomickException):
    detail = "Введен неверный пароль"


class UserNotDefinedException(DomickException):
    detail = "Текущий пользователь не определен"


class DBNotAvailableException(DomickException):
    detail = "База данных недоступна"


class RedisNotAvailableException(DomickException):
    detail = "Redis недоступен"


class CeleryBrokerNotAvailableException(DomickException):
    detail = "Брокер Celery недоступен"


class DomickHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(DomickHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(DomickHTTPException):
    status_code = 404
    detail = "Номер не найден"


class DateFromLaterDateToHTTPException(DomickHTTPException):
    status_code = 422
    detail = "Дата заезда не может быть позже даты выезда"


class AuthTokenErrorHTTPException(DomickHTTPException):
    status_code = 422
    detail = "Неверный токен"


class AuthTokenNotFoundHTTPException(DomickHTTPException):
    status_code = 401
    detail = "Токен доступа не найден "


class UserAlreadyExistsHTTPException(DomickHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует"


class UserNotExistsHTTPException(DomickHTTPException):
    status_code = 404
    detail = "Такой пользователь не существует"


class UserPasswordWrongHTTPException(DomickHTTPException):
    status_code = 403
    detail = "Неверный пароль"


class BookingRoomNotAvailableHTTPException(DomickHTTPException):
    status_code = 403
    detail = "Номер недоступен для бронирования на указанный срок"


class FacilityKeyNotCorrectHTTPException(DomickHTTPException):
    status_code = 422
    detail = "Некорректный идентификатор удобства"


class FacilityAlreadyExistsHTTPException(DomickHTTPException):
    status_code = 409
    detail = "Такое удобство уже существует"


class ServiceNotAvailableHTTPException(DomickHTTPException):
    status_code = 424
    detail = "Сервис временно недоступен. Повторите попытку позже"
