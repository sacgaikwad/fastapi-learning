class InvalidCredentialsException(Exception):

    def __init__(self):
        self.message = "Invalid email or password"
        super().__init__(self.message)

