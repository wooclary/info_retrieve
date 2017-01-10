import json

with open('./result/tag_result.txt') as f:
    result = json.loads(f.read())
    print(result)
