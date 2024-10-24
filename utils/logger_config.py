# Deprecated due to the use of loguru, just for archiving

import logging
from colorlog import ColoredFormatter
import json

def setup_logger(name, level=logging.INFO):  # Default level is INFO
    # Define a handler
    handler = logging.StreamHandler()

    # Define a ColoredFormatter with color configuration
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(relativeCreated)d - %(name)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',  # Use 'purple' instead of 'magenta'
        }
    )

    # Attach the formatter to the handler
    handler.setFormatter(formatter)

    # Get the logger instance and attach the handler
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)

    # Avoid duplicated log entries if the logger is already configured
    logger.propagate = False

    return logger

def log_dict(logger, data, level=logging.DEBUG, description=""):
    
    # Log a dictionary in a formatted JSON way along with a description
    if data is not None:
        log_message = f"{description}\n{json.dumps(data, indent=4, ensure_ascii=False)}"
        logger.log(level, log_message)
    else:
        logger.log(level, f"{description} No data provided")

if __name__ == "__main__":
    # Set up the logger, defaulting to INFO level
    logger = setup_logger("test_logger")

    # Set the logger level to DEBUG when run as the main script
    logger.setLevel(logging.DEBUG)

    # Log messages with different levels
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")

    # Use a dict to test
    data = {
        
        'key1': 'value1',
        'key2': 'value2'
    }
    
    sample_material_data = [
        {
            "__metadata": {
                "uri": "https://my601274.sapbyd.cn/sap/byd/odata/cust/v1/mcmaterial/MaterialCollection('00163E8BB9C41EDAA7CDB7A490EB7FA9')",
                "type": "cust.Material"
            },
            "ObjectID": "00163E8BB9C41EDAA7CDB7A490EB7FA9",
            "InternalID": "10000001",
            "LastChangeDateTime": "/Date(1715845943549)/"
        }
    ]

    # Log the data in a formatted JSON way
    log_dict(logger, data, logging.DEBUG, "Test Data")

    log_dict(logger, sample_material_data, logging.INFO, "Sample Material Data")