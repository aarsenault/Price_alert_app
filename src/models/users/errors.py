

class UserError(Exception):
    def __init__(self, message):
        self.message = message

# inherit from above
class NoUser(UserError):
    pass

class IncorrectPassword(UserError):
    pass


class UserAlreadyRegistered(UserError):
    pass

class InvalidEmailError(UserError):
    pass