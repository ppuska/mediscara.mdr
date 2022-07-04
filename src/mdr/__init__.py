"""Init module for the MDR package"""
import coloredlogs

coloredlogs.install(fmt="%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s", level="INFO")

__version__ = '1.0'
