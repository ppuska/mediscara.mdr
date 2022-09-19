"""Init module for the MDR package"""
import coloredlogs

coloredlogs.install(
    fmt="%(asctime)s %(funcName)s %(levelname)s %(message)s", level="INFO"
)

__version__ = "1.0"
