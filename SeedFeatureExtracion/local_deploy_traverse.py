'''
这个是检测种粒，seed_grain
'''
# %%
import os
import re
import json
import requests
import math
from ultralytics import YOLO

# Load model
model = YOLO('bean_best.pt')
# single_square_millimeter_pixels = 144
single_millimeter_pixels = 12
top_path = "soybean_dataset"
# top_path = "test_images/seed"
child_img_list = os.listdir(top_path)
# print(child_img_list)
'''
The standard name of the images is like: 'ZS110296_19_G.jpg'
'''
total_image_num = len(child_img_list)
for image_num in range(total_image_num):
    image_name = child_img_list[image_num]
    if image_name == ".DS_Store":
        continue
    elif image_name == "OUTPUT":
        continue
    image_path = top_path + '/' + image_name
    # print(image_path)

    results = model(image_path)
    data_list_of_grain_seed = json.loads(results[0].tojson())
    # print(type(data_dict_of_grain_seed[0]))

    # %%

    bean_info_list = []
    bean_num = len(data_list_of_grain_seed)
    for i in range(bean_num):
        box_axis = data_list_of_grain_seed[i]["box"]
        box_X_length = (box_axis["x2"] - box_axis["x1"]) / single_millimeter_pixels
        box_Y_length = (box_axis["y2"] - box_axis["y1"]) / single_millimeter_pixels
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
    # img_name = "seed_1.jpg"
    # img_path = "test_images/seed/"
    first_line = ["bean_num", "box_X_length", "box_Y_length", "bean_area", "circumference", "roundness"]
    line_length = len(first_line) - 1
    '''
    这里img_name须调整，下面写文件目录一起调整：6
    '''
    if os.path.exists(top_path + '/' + "OUTPUT"):
        pass
    else:
        os.mkdir(top_path + '/' + "OUTPUT")
    with open(top_path + '/' + "OUTPUT" + '/' + "detail_info_" + image_name[2:8] + ".csv", "w") as f:
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
