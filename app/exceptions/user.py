from fastapi import status


class UserNotFoundException(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.status_code = status.HTTP_404_NOT_FOUND

class UserAlreadyExistsException(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.status_code = status.HTTP_409_CONFLICT

class InvalidUserDataException(Exception):
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.status_code = status.HTTP_400_BAD_REQUEST

class UserServiceException(Exception):

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR