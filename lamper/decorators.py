from lamper import config
from lamper.https import HttpMethod


__logger = config.get_logger(__name__)


class Mapping(object):

    def __init__(self):
        self.routes = {}

    def __decorator(self, function, path, method):
        self.routes[path + method.value] = function
        return function

    def get(self, path: str):
        def decorator(function):
            return self.__decorator(function, path, HttpMethod.GET)
        return decorator

    def post(self, path: str):
        def decorator(function):
            return self.__decorator(function, path, HttpMethod.POST)
        return decorator

    def put(self, path: str):
        def decorator(function):
            return self.__decorator(function, path, HttpMethod.PUT)
        return decorator

    def delete(self, path: str):
        def decorator(function):
            return self.__decorator(function, path, HttpMethod.DELETE)
        return decorator

    def patch(self, path: str):
        def decorator(function):
            return self.__decorator(function, path, HttpMethod.PATCH)
        return decorator

    def options(self, path: str):

        def decorator(function):
            return self.__decorator(function, path, HttpMethod.OPTIONS)
        return decorator

