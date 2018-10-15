"""
Contains the logic for the confirmation token.
"""

from itsdangerous import URLSafeTimedSerializer

from samo.core import app


def generate_confirmation_token(email):
    """
    Generates the confirmation token.
    :param email:
    :return:
    :rtype: json
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    """
    Confirms the token.
    :param token:
    :param expiration:
    :return: email
    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except Exception:  # pylint: disable=broad-except
        return False
    return email
