# %%
from ultralytics import YOLO
# Print image.jpg results in JSON format
import json
import os
import math

# Load model
model = YOLO('eyecrack_best.pt')

# top_path = "test_images/cr_ey"
top_path = "crack_eye/images"
child_img_list = os.listdir(top_path)
child_img_list_length = len(child_img_list)
total_img_num_to_detect = child_img_list_length
total_beans_with_cracks = 0
num_of_cracks = 0
num_of_eyes = 0
single_millimeter_pixels = 12
all_cracks = []

output_path = top_path + '/' + "OUTPUT"
if os.path.exists(output_path):
    pass
else:
    os.mkdir(output_path)

f = open(output_path + '/' + "eye_info_list.csv", "w")
first_line = ["eye_num", "box_X_length", "box_Y_length", "eye_area", "circumference"]
each_line_length = len(first_line)
for i in range(each_line_length):
    f.write(first_line[i])
    if i != each_line_length - 1:
        f.write(',')
    else:
        f.write('\n')
each_line_length -= 1

for bean_num in range(child_img_list_length):
    image_name = child_img_list[bean_num]
    if image_name == ".DS_Store":
        total_img_num_to_detect -= 1
        continue
    elif image_name == "OUTPUT":
        total_img_num_to_detect -= 1
        continue
    image_path = top_path + '/' + image_name
    
    # Run inference
    results = model(image_path)

    # type(json.loads(results[0].tojson())[0])
    data_list_of_grain_seed = json.loads(results[0].tojson())
    # print(data_list_of_grain_seed)
    for result_dict in data_list_of_grain_seed:
        current_bean = []
        current_crack = []
        if result_dict["name"] == "eye":
            box_axis = result_dict["box"]
            box_X_length = (box_axis["x2"] - box_axis["x1"]) / single_millimeter_pixels
            box_Y_length = (box_axis["y2"] - box_axis["y1"]) / single_millimeter_pixels
            bean_area = box_X_length * box_Y_length * math.pi / 4
            if len(current_bean) == 0:
                if box_X_length >= box_Y_length:
                    current_bean.append(box_X_length)
                    current_bean.append(box_Y_length)
                else:
                    current_bean.append(box_Y_length)
                    current_bean.append(box_X_length)
                current_bean.append(bean_area)
                circumference = current_bean[1]*math.pi + 2*(current_bean[0] - current_bean[1])
                # roundness = current_bean[1] / current_bean[0]
                current_bean.append(circumference)
                # current_bean.append(roundness)
            else:
                if bean_area < current_bean[2]:
                    # update
                    current_bean = []
                    if box_X_length >= box_Y_length:
                        current_bean.append(box_X_length)
                        current_bean.append(box_Y_length)
                    else:
                        current_bean.append(box_Y_length)
                        current_bean.append(box_X_length)
                    current_bean.append(bean_area)
                    circumference = current_bean[1]*math.pi + 2*(current_bean[0] - current_bean[1])
                    # roundness = current_bean[1] / current_bean[0]
                    current_bean.append(circumference)
                    # current_bean.append(roundness)
        # crack
        elif result_dict["name"] == "crack":
            box_axis = result_dict["box"]
            temp_x1 = []
            temp_x2 = []
            temp_y1 = []
            temp_y2 = []
            temp_x1.append(box_axis["x1"])
            temp_x2.append(box_axis["x2"])
            temp_y1.append(box_axis["y1"])
            temp_y2.append(box_axis["y2"])
            box_X_length = (box_axis["x2"] - box_axis["x1"]) / single_millimeter_pixels
            box_Y_length = (box_axis["y2"] - box_axis["y1"]) / single_millimeter_pixels
            bean_area = box_X_length * box_Y_length * math.pi / 4
            if len(current_crack) == 0:
                if box_X_length >= box_Y_length:
                    current_crack.append(box_X_length)
                    current_crack.append(box_Y_length)
                else:
                    current_crack.append(box_Y_length)
                    current_crack.append(box_X_length)
                current_crack.append(bean_area)
                circumference = current_crack[1]*math.pi + 2*(current_crack[0] - current_crack[1])
                # roundness = current_crack[1] / current_crack[0]
                current_crack.append(circumference)
                # current_crack.append(roundness)
                current_crack.append(image_name)
                all_cracks.append(current_crack)
                num_of_cracks += 1
            else:
                # 如果裂纹落在上一个裂纹框里，则忽略，否则记录
                average_X_aixs = (box_axis["x1"] + box_axis["x2"]) / 2
                average_Y_aixs = (box_axis["y1"] + box_axis["y2"]) / 2
                leap_flag = False
                for i in range(len(temp_x1)):
                    if average_X_aixs >= temp_x1[i] and average_X_aixs <= temp_x2[i] and average_Y_aixs >= temp_y1[i] and average_Y_aixs <= temp_y2[i]:
                        # 重合
                        leap_flag = True
                        break
                if leap_flag:
                    continue
                else: # 不重合，记录
                    current_crack = [] # 重置
                    temp_x1.append(box_axis["x1"]) # 更新
                    temp_x2.append(box_axis["x2"])
                    temp_y1.append(box_axis["y1"])
                    temp_y2.append(box_axis["y2"])
                    if box_X_length >= box_Y_length:
                        current_crack.append(box_X_length)
                        current_crack.append(box_Y_length)
                    else:
                        current_crack.append(box_Y_length)
                        current_crack.append(box_X_length)
                    current_crack.append(bean_area)
                    circumference = current_crack[1]*math.pi + 2*(current_crack[0] - current_crack[1])
                    # roundness = current_crack[1] / current_crack[0]
                    current_crack.append(circumference)
                    # current_crack.append(roundness)
                    current_crack.append(image_name)
                    all_cracks.append(current_crack)
                    num_of_cracks += 1
            # print("crack found!")
        
        # write file
        if current_bean:
            f.write(str(num_of_eyes))
            num_of_eyes += 1
            for i in range(each_line_length):
                f.write(',' + str(current_bean[i]))
            f.write('\n')
        if current_crack:
            total_beans_with_cracks += 1
        #     all_cracks.append(current_crack)
'''
有这么几种可能：
- 种子里什么也没有；
- 种子里只有裂纹；
- 种子里只有种脐
- 种子里同时有种脐和裂纹；
- 种子里识别到多个裂纹和种脐。

对于第一种情况，得到的结果是一个空的列表；对于最后一种情况，应当选择较小的种脐方框作为最终结果，并记录全部的裂纹。
'''
f.close()
# %%
with open(output_path + '/' + "cracks_info_list.csv", "w") as f:
    first_line = ["crack_num", "box_X_length", "box_Y_length", "crack_area", "circumference", "file_name"]
    each_line_length = len(first_line)
    for i in range(each_line_length):
        f.write(first_line[i])
        if i != each_line_length - 1:
            f.write(',')
        else:
            f.write('\n')
    each_line_length -= 1

    for i in range(num_of_cracks):
        # current_crack_num = len(all_cracks[i])
        f.write(str(i))
        for j in range(each_line_length):
            f.write(',' + str(all_cracks[i][j]))
        f.write('\n')


# %%
print("The total number of cracks is {}, and the ratio of beans with cracks is {}".format(num_of_cracks, total_beans_with_cracks / total_img_num_to_detect))
# %%
