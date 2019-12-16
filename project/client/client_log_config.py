import logging

logger = logging.getLogger('client')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler = logging.FileHandler('client.log')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)
