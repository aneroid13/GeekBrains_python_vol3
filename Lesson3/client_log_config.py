import logging
import logging.handlers

logging.basicConfig(
    filename='./log/client_log.txt',
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    level=logging.DEBUG
)
logger_cl = logging.getLogger("client_logger")
console_handle = logging.StreamHandler()
console_handle.setLevel(logging.INFO)
logger_cl.addHandler(console_handle)