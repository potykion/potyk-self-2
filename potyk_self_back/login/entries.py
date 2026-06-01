from flask_login import UserMixin


class SecretUser(UserMixin):
    def __init__(self, secret):
        self.secret = secret

    def get_id(self):
        return self.secret