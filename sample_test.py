from src.utils.log_module import setup_logger

logger = setup_logger()

x = 4
y = 2
z = 3
k = False

if not k and x > (y and z):
    logger.info(1)
