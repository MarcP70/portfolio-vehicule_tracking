class Config:
    """
    A class used to store configuration settings for an application.

    Fields:
    - SECRET_KEY: A field that holds a secret key used for
    cryptographic operations.
    - SESSION_COOKIE_SAMESITE: A field that holds the value for the SameSite
    attribute of the session cookie.
    - SESSION_COOKIE_SECURE: A field that holds a boolean value indicating
    whether the session cookie should be secure.
    - MONGO_URI: A field that holds the URI for connecting to a MongoDB
    database.
    """

    SECRET_KEY = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    MONGO_URI = 'mongodb://localhost:27017/vehicle_tracking_db'
