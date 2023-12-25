'''
这个是检测种脐和裂纹，小数据集
'''

# %%
import json
import requests

# Run inference on an image
url = "https://api.ultralytics.com/v1/predict/5f2jUcdflFNiRF3iOKKa"
headers = {"x-api-key": "5d8cc9bc6cc02ba0794c67082598823753b3828daf"}
data = {"size": 640, "confidence": 0.25, "iou": 0.45}
with open("path/to/image.jpg", "rb") as f:
	response = requests.post(url, headers=headers, data=data, files={"image": f})

# Check for successful response
response.raise_for_status()

# Print inference results
print(json.dumps(response.json(), indent=2))