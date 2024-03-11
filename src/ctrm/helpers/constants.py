class UserError:
    INACTIVE_USER = "User is currently inactive."


class AuthError:
    NOT_ADMIN = "User doesn't have enough privileges."


class ForwarderError:
    CLIENT_NOT_FOUND = "Client does not exists"
    BASE_URL_NOT_FOUND = "Client base url does not exists"


class EmailSubject:
    NEW_ACCOUNT = "Welcome to Gabriel - Let's get started!"


class EmailTemplates:
    NEW_ACCOUNT = "new_account.html"


class WorkbenchError:
    ALREADY_EXISTS = "Workbench ID already exists."
