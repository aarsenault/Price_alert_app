import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        # returns a hex rather than obj
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/pass combo
        as sent by the site forms is valid or not
        checks that the e-mail exists, and that the password
        associated to that email is correct.

        :param email: the user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one("users", {"email": email})
        # Pass in pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.NoUser("User does not exist!")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPassword("Password Doesn't Match")

        else:
            return True


    @staticmethod
    def register_user(email, password):
        """
        Method registeres a user using e-mail and pass.
        the pass already comes hashed as sha512

        :param email: user's email - might be invalid
        :param password: sha512 hased pass
        :return: True if successful registration, false otherwise (exceptions raised)

        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            # Tell user they're already registered
            raise UserErrors.UserAlreadyRegistered("The E-mail you entered is already registered")

        if not Utils.email_is_valid(email):
            # tell user that emai is not constructed properly
            raise UserErrors.InvalidEmailError("E-mail does not have a valid format")


        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        # inserts the Json data into the users collection of the db
        Database.insert("users", self.json())

    def json(self):
        return{

            "id": self._id,
            "email": self.email,
            "password": self.password
        }
