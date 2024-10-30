import json

# Sample JSON data
response = {
    "order": [
        "tnpmg4ksffns3fyefcthzc3z6w",
        "6z43woyfb7fyuyr6juqj44oaka"
    ],
    "posts": {
        "6z43woyfb7fyuyr6juqj44oaka": {
            "id": "6z43woyfb7fyuyr6juqj44oaka",
            "create_at": 1730257712943,
            "update_at": 1730257712943,
            "edit_at": 0,
            "delete_at": 0,
            "is_pinned": False,
            "user_id": "84bcwjnjkfnn5rszc1wf9geixa",
            "channel_id": "993n5g6cniyam8m7sh3ib5ehow",
            "root_id": "tnpmg4ksffns3fyefcthzc3z6w",
            "original_id": "",
            "message": "ok",
            "type": "",
            "props": {},
            "hashtags": "",
            "pending_post_id": "",
            "reply_count": 1,
            "last_reply_at": 0,
            "participants": None,
            "metadata": {}
        },
        "tnpmg4ksffns3fyefcthzc3z6w": {
            "id": "tnpmg4ksffns3fyefcthzc3z6w",
            "create_at": 1730257668791,
            "update_at": 1730257748786,
            "edit_at": 1730257748785,
            "delete_at": 0,
            "is_pinned": False,
            "user_id": "u9m8ks7d33y1ibqnwg4tchyp1w",
            "channel_id": "993n5g6cniyam8m7sh3ib5ehow",
            "root_id": "",
            "original_id": "",
            "message": "@lei  孚瑞得 签订采购订单 ，采购抓 其余传送带模组下单 - V6 机加件 ， 用于 275-WPF（MCP-275-WPF） ，费用为 4080  元，SAP： 241501 ，请审批",
            "type": "",
            "props": {
                "disable_group_highlight": True
            },
            "hashtags": "",
            "file_ids": [
                "98nyec4tm7f5zy3swpmkaeo5kh"
            ],
            "pending_post_id": "",
            "reply_count": 1,
            "last_reply_at": 0,
            "participants": None,
            "metadata": {
                "files": [
                    {
                        "id": "98nyec4tm7f5zy3swpmkaeo5kh",
                        "user_id": "u9m8ks7d33y1ibqnwg4tchyp1w",
                        "post_id": "tnpmg4ksffns3fyefcthzc3z6w",
                        "channel_id": "",
                        "create_at": 1730257643641,
                        "update_at": 1730257643641,
                        "delete_at": 0,
                        "name": "GZ-PO241501-1029_孚瑞得（已盖章）.pdf",
                        "extension": "pdf",
                        "size": 297608,
                        "mime_type": "application/pdf",
                        "mini_preview": None,
                        "remote_id": "",
                        "archived": False
                    }
                ]
            }
        }
    }
}

# Extract messages
messages = [post["message"] for post in response["posts"].values()]

# Print the result
print(messages)

# Check if any message contains "ok" (case insensitive)
found_ok = any("ok" in post["message"].lower() for post in response["posts"].values())

# Print the result
print(found_ok)

messages_length = len(messages)
print(messages_length)

# Conditional statements
if not found_ok and messages_length > 1:
    print("Approval rejected")
elif not found_ok and messages_length == 1:
    print("Approval pending")
else:
    print("Approval approved")