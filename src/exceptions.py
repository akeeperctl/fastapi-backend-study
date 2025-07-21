class DomickException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"{self.__class__.__name__}, {self.message}"
        else:
            return f"{self.__class__.__name__}"

class BookingRoomNotAvailableException(DomickException):
    def __init__(self):
        super().__init__("""Номер недоступен для бронирования""")

class UserAlreadyExistException(DomickException):
    def __init__(self):
        super().__init__("""Такой пользователь уже существует""")

class DateFromLaterThanDateToException(DomickException):
    def __init__(self):
        super().__init__("""Дата заезда позже даты выезда""")

class HotelNotExistException(DomickException):
    def __init__(self):
        super().__init__("""Такой отель не существует""")

class RoomNotExistException(DomickException):
    def __init__(self):
        super().__init__("""Такой номер не существует""")

class EditedTooMatchRoomsException(DomickException):
    def __init__(self):
        super().__init__("Отредактировано слишком много комнат")

