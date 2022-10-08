from shared import exceptions


class UniversityDataUnavailable(exceptions.AppException):
    status_code = exceptions.status.HTTP_503_SERVICE_UNAVAILABLE
    message = 'TSU schedule proxy unavailable'
