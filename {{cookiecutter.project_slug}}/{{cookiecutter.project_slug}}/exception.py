class IbanCheckerException(Exception):
    status_code = 500
    errorcode = "internal-error"

    def __init__(self, message, payload=None):
        super().__init__()
        self.payload = dict(payload or ())
        self.message = message

    def to_dict(self):
        return {
            "code": self.errorcode,
            "message": self.message,
            "details": self.payload,
        }

    def __str__(self):
        return self.message


class InvalidUsage(IbanCheckerException):
    status_code = 400
    errorcode = "invalid-usage"


class InvalidParams(IbanCheckerException):
    status_code = 422
    errorcode = "invalid-parameters"


class ResourceNotFound(IbanCheckerException):
    status_code = 404
    errorcode = "resource-not-found"


class Forbidden(IbanCheckerException):
    status_code = 403
    errorcode = "forbidden"


class UnauthorizedAccess(IbanCheckerException):
    status_code = 401
    errorcode = "unauthorized-access"


class Unsupported(IbanCheckerException):
    status_code = 501
    errorcode = "unsupported"


class Unexpected(IbanCheckerException):
    status_code = 500
    errorcode = "unexpected-error"
