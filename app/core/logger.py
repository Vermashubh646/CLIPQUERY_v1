import sys
from loguru import logger

logger.remove()

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>[Req_ID: {extra[request_id]}]</cyan> | "
    "<level>{message}</level>"
    )

logger.configure(extra={'request_id':'system_startup'})

logger.add(
    sys.stderr,
    format= log_format,
    level= "INFO",
    colorize=True)

custom_logger=logger