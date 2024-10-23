import json
from loguru import logger
import pprint

# 假设这是你要记录的字典
data = {
    'key1': 'value1',
    'key2': 'value2',
    'nested': {
        'nested_key1': 'nested_value1',
        'nested_key2': 'nested_value2'
    }
}

# 使用 json.dumps() 方法将字典转换为格式化的 JSON 字符串
formatted_data = json.dumps(data, indent=4, ensure_ascii=False)

# 使用 Loguru 记录格式化后的字典
logger.debug(formatted_data)


# # 使用 pprint 模块的 pformat() 方法格式化字典
# formatted_data = pprint.pformat(data)

# # 使用 Loguru 记录格式化后的字典
# logger.info(formatted_data)