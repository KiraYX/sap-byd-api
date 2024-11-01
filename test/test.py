import requests
import json
from rich import print as rich_print

url = "https://my601274.sapbyd.cn/sap/byd/odata/ana_businessanalytics_analytics.svc/RPSCMINVV02_Q0001QueryResults?$select=TLOG_AREA_UUID,CLOG_AREA_UUID,TON_HAND_STOCK_UOM,CON_HAND_STOCK_UOM,TMATERIAL_UUID,CMATERIAL_UUID,TSITE_UUID,CSITE_UUID,KCON_HAND_STOCK&$format=json"
payload = {}
headers = {
  'Authorization': 'Basic eWkueHU6SDReSCplJkV0Jmc0YnJedw==',
  'Cookie': 'sap-login-XSRF_LWJ=20241031033831-Kb6Wz5ENeSU2CSYwnWPXwQ%3d%3d; sap-usercontext=sap-client=146'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
formatted_response = response.json()
rich_print(formatted_response)
