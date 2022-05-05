# 补偿轴计算器
基于HoshinoBot的补偿轴计算器插件，可以计算返还时间下对应的时间轴
# 安装
1. 在HoshinoBot的插件目录`modules`中clone本项目`git clone git@github.com:OREOCODEDEV/pcr_time_calculator.git`
1. 打开`config`文件夹中的`__bot__.py`文件，并在`MODULES_ON`中添加`pcr_time_calculator`
# 使用方法
补偿轴 [返还时间] [时间1] [时间2] ...\
例：发送：`补偿轴 121 118 110 107 58`\
回复：
```
补偿时间:1:21
原始轴 补偿轴
1:18   1:09
1:10   1:01
1:07   0:58
0:58   0:49
```
