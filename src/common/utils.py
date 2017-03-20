from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def hash_password(password):

        """
        Encrypts a password using pbkdf2_sha512
        This uses double encryption

        :param password: the sha512 pass from the Login/register form
        :return: a sha512 -> pbkdf2_sha512 encrypted pass
        """
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        checks that the pass the user sent matches that of the database
        the database pas is encrypted more that the user's password at this stage

        :param password: sha512-hashed password
        :param hashed_password: PBKDF2_sha512 encrypted password
        :return: True if passwords match, False otherwise

        """

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        # TODO
        # might need to mod this regex
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False