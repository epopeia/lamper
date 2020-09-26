import http.client  as http_client
import logging


def get_logger(name=None, level=None):
    if not level:
        level = logging.INFO
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S', level=level)

    logging.getLogger().setLevel(level)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(level)
    requests_log.propagate = True

    my_logger = logging.getLogger(name)
    my_logger.setLevel(level)
    return my_logger
