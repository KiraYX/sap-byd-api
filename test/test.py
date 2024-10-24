from helper.json_converter import convert_jdy_json_to_widget_format
from loguru import logger
import sys

input_data = {
        'material_id': '10000001',
        'internal_description': '043-拆垛及混码-视觉控制器_MUJIN_MC9000-3DV-RS-LOGI',
        'material_name': '043-拆垛及混码-视觉控制器',
        'brand': 'MUJIN',
        'model_number': 'MC9000-3DV-RS-LOGI',
        'IsObsolete': False,
        '_id': '6683e2b3f99e5bc64e8b431d',
        'appId': '6683c4a2399857dff128b206',
        'entryId': '6683c4b0ae4fd18278021f46'
}

converted_output = convert_jdy_json_to_widget_format(input_data, debug=True)

logger.info("Converted output: {}", converted_output)