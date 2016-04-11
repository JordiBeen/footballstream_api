import base64
import hashlib
import logging
import os
import uuid

import bcrypt
from Crypto.Cipher import AES

from pyramid.security import Everyone, Allow, DENY_ALL, Authenticated

log = logging.getLogger(__name__)


def generate_token(size=64):
    """Generates a relativily secure token for use as CSRF or similar
    purposes

    :param integer size: the number of bits of entropy to use for the hash.
                         Minimum of 64.  Must be divisible by 8.
    :reeturns: sha256 string of 8 random bytes
    """

    assert type(size) == int
    assert size >= 64
    assert size % 8 == 0
    return hashlib.sha256(os.urandom(int(size / 8))).hexdigest()


def hash_password(password, request=None):
    """Hashes a password
    :param unicode password: the password to hash
    :param Request request: a pyramid request. If given this method will
                            attempt to retrieve a "salt_rounds" setting and use
                            that for the salt generation instead.
    :returns: bcrypt hashed password
    """
    num_rounds = 12
    if request:
        try:
            num_rounds = int(request.registry.settings.get('salt_rounds', 12))
        except:
            raise
        if num_rounds < 4:
            raise Exception("invalid salt_rounds setting '%r', "
                            "below 4".format(num_rounds))
        if num_rounds > 31:
            raise Exception("Invalid salt_rounds setting '%r', "
                            "over 31".format(num_rounds))

    hashed_password = bcrypt.hashpw(password.encode('latin1', 'ignore'),
                                    bcrypt.gensalt(num_rounds))

    try:
        hashed_password = hashed_password.decode('latin1')
        log.info("Converting hashed_password to latin1 success")
    except:
        log.warning("Converting hashed_password to latin1 failed",
                    exc_info=True)
    return hashed_password


def check_password(password, stored_password):
    """Checks password against a bcrypt hashed stored password.

    :param unicode password: the password to check
    :param unicode stored_password: the bcrypt hashed password including salt
    :returns True if the password matches the hash, otherwise False
    """
    hashed_password = bcrypt.hashpw(password.encode('latin1',
                                                    'ignore'),
                                    stored_password.encode('latin1',
                                                           'ignore'))
    try:
        hashed_password = hashed_password.decode('latin1')
        log.info("Converting hashed_password to latin1 success")
    except:
        log.warning("Converting hashed_password to latin1 failed",
                    exc_info=True)

    result = (hashed_password == stored_password)
    return result


def uuid_from_string(key):
    try:
        return uuid.UUID(key)
    except ValueError:
        log.error("Client provided illegal UUID: %r", exc_info=True)
        raise Exception("not a valid UUID")
    except:
        log.critical("Error during UUID conversion", exc_info=True)
        raise


def encrypt(value, key):
    u = uuid_from_string(key)

    decoded_value = value.encode('utf-8')

    encryptor = AES.new(u.hex, AES.MODE_CBC, IV=u.bytes)
    padded = decoded_value + ((16 - (len(decoded_value) % 16)) * '\x00')
    return base64.b64encode(encryptor.encrypt(padded))


def decrypt(blob, key):
    u = uuid_from_string(key)
    decryptor = AES.new(u.hex, AES.MODE_CBC, IV=u.bytes)

    encoded = decryptor.decrypt(base64.b64decode(blob)).replace('\x00', '')
    return encoded.decode('utf-8')


class Auth(object):
    __acl__ = [(Allow, Authenticated, 'private'),
               (Allow, Everyone, 'public'),
               DENY_ALL]

    def __init__(self, req):
        self.request = req
