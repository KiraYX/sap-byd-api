from utils.debug import log_json

if __name__ == "__main__":
    data = {
        'key1': 'value1',
        'key2': 'value2'
    }
    logger.setLevel(logging.DEBUG)
    log_json(data)