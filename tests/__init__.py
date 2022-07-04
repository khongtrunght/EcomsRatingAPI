import logging
import sys

# Reconfiguring the logger here will also affect test running in the PyCharm IDE
log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)
