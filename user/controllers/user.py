import json
from ..models.user import signup, login


class UserController:
    @staticmethod
    def signup(username, password, fullName):
        try:
            signup(username, password, fullName)

            return {
                'status': 200,
                'data': {}
            }
        except Exception as e:
            return {
                'status': 202,
                'data': {'error_msg': str(e)}
            }

    @staticmethod
    def login(username, password):
        try:
            login(username, password)
            return {
                'status': 200,
                'data': {}
            }
        except Exception as e:
            return {
                'status': 202,
                'data': {'error_msg': str(e)}
            }
