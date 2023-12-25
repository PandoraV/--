# 大豆种子表型提取

## 使用模型和部署

本项目使用[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)模型完成简单开发，并通过[YOLOv5 文档](https://docs.ultralytics.com/yolov5/)完成完井部署。本版本在最低要求的基础上使用`Python 3.8.11`和`OpenCV 4.6.0.66`的基础完成的，系统为`macOS Mojave (macOS 10.14)`。

开发过程中模型的使用方式包括**本地**和**在线**两种方式。本地方式的简单demo见[test.py](SeedFeatureExtracion/test.py)，在线方式的单张文件处理demo见[online_deploy_10_22.py](SeedFeatureExtracion/online_deploy_10_22.py)。使用`Jupyter`完成开发的单张文件处理是[online_deploy_15_18.py](SeedFeatureExtracion/online_deploy_15_18.py)。

## 快速使用

将数据集和代码文件放在同一目录下运行即可，输出位于数据集文件夹的`OUTPUT`中。对于种粒，会将每张图片中的种粒信息输出在一张`CSV`内，每张图片均会输出；对于裂纹和种脐，会将所有识别到的信息集合在一张数据集文件内输出。

### 数据格式

输入的数据集，对于：

1. **种粒** 为`1276*1276`的单张图片，图内最多有`10*10`的大豆种粒。

2. **种脐和裂纹** 为提前分割好的单个豆子。

输出的数据信息包括：

1. **种粒** 每张图片内每个种粒的长宽、面积、周长、圆度等。注意，本例使用识别矩形框的**内切椭圆**来代替种粒本身，未来可改为图像分割方式提高精度。

2. **种脐和裂纹** 与上相同，额外统计有裂纹的个数和有裂纹的种粒的占比。