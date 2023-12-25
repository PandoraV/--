'''
这个是检测种粒，seed_grain
'''
# %%
import os
import re

top_path = "soybean_dataset"
child_img_list = os.listdir(top_path)
print(child_img_list)


# %%
import json
import requests

# Run inference on an image
url = "https://api.ultralytics.com/v1/predict/tlD3tnNjPLAomdTBUB1h"
headers = {"x-api-key": "5d8cc9bc6cc02ba0794c67082598823753b3828daf"}
data = {"size": 640, "confidence": 0.25, "iou": 0.45}
with open("test_images/seed/seed_1.jpg", "rb") as f:
	response = requests.post(url, headers=headers, data=data, files={"image": f})

# Check for successful response
response.raise_for_status()

# %%
# Print inference results
print(json.dumps(response.json(), indent=2))

# %%
with open("detect_list_json_output.json", "w") as f:
	f.writelines(json.dumps(response.json(), indent=2))

# %%
# print(response.json()["data"])
data_dict_of_grain_seed = response.json()["data"]
# print(type(data_dict_of_grain_seed[0]))

# %%
import math

bean_info_list = []
bean_num = len(data_dict_of_grain_seed)
for i in range(bean_num):
	box_axis = data_dict_of_grain_seed[i]["box"]
	box_X_length = box_axis["x2"] - box_axis["x1"]
	box_Y_length = box_axis["y2"] - box_axis["y1"]
	bean_area = box_X_length * box_Y_length * math.pi / 4
	current_bean = []
	if box_X_length >= box_Y_length:
		current_bean.append(box_X_length)
		current_bean.append(box_Y_length)
	else:
		current_bean.append(box_Y_length)
		current_bean.append(box_X_length)
	current_bean.append(bean_area)
	circumference = current_bean[1]*math.pi + 2*(current_bean[0] - current_bean[1])
	roundness = current_bean[1] / current_bean[0]
	current_bean.append(circumference)
	current_bean.append(roundness)
	bean_info_list.append(current_bean)


# %%
img_name = "seed_1.jpg"
img_path = "test_images/seed/"
first_line = ["bean_num", "box_X_length", "box_Y_length", "bean_area", "circumference", "roundness"]
line_length = len(first_line) - 1
'''
这里img_name须调整，下面写文件目录一起调整：6
'''
with open("detail_info_of_" + img_name[:6] + ".csv", "w") as f:
	f.write("bean_num")
	for i in range(1, line_length + 1):
		f.write("," + first_line[i])
	f.write('\n')

	for j in range(bean_num):
		f.write(str(j))
		for i in range(line_length):
			f.write("," + str(bean_info_list[j][i]))
		f.write('\n')

# %%
