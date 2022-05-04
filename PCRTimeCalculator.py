from hoshino import Service

help_use_str = "\n使用方法：补偿轴 [返还时间] [时间1] [时间2] ...\n例：补偿轴 121 118 110 107 105"
help_str = "计算返还时间下对应的时间轴" + help_use_str

sv = Service("补偿轴计算器", help_=help_str)


def time_converter(time):
    # 把PCR轴时间的 分:秒 格式转换为十进制的秒
    if not 0 <= time <= 130:
        raise Exception("Time out of range")
    if 60 <= time <= 99:
        raise Exception("Time out of range")
    if time >= 100:
        return time - 40
    return time


def pretty_time(time):
    # 把十进制的秒转换为PCR时间轴的 分:秒
    if time <= 0:
        return "0:00"
    if time < 60:
        return "0:%s" % (str(time) if time >= 10 else str("0" + str(time)))  # 补0
    return "1:%s" % (str(time - 60) if time >= 70 else str("0" + str(time - 60)))


def pretty_output(origin_time_array, new_time_array):
    # 对齐输出
    ret = ""
    for i, j in enumerate(origin_time_array):
        ret += "\n%s     %s" % (j, new_time_array[i])
    return ret


def handle_main(remain_time, origin_time_array):
    try:
        # 转为int型的 分:秒
        remain_time = int(remain_time)
        origin_time_array = list(map(int, origin_time_array))
    except:
        return "转换时间轴时发生错误，请检查输入的时间轴\n时间轴无需输入小数点，如1.03直接输入103即可"
    try:
        # PCR时间轴的 分:秒 转为十进制的秒
        remain_time = time_converter(remain_time)
        origin_time_array = list(map(time_converter, origin_time_array))
    except:
        return "有时间超出范围，请检查输入时间轴\n请确保输入时间轴范围均在130-100及059-001之间"
    used_time = 90 - remain_time  # 计算已使用的时间
    new_time_array = list(map(lambda i: i - used_time, origin_time_array))  # 减去已使用的时间得到补偿时间轴
    ret = "补偿时间:%s\n" % pretty_time(remain_time)
    ret += "原始轴 补偿轴"
    ret += pretty_output(list(map(pretty_time, origin_time_array)), list(map(pretty_time, new_time_array)))
    return ret


@sv.on_prefix("补偿轴")
async def time_calculator(bot, ev):
    message = ev.message.extract_plain_text()
    message = list(filter(lambda x: False if x is None or x == "" else True, message.split(" ")))  # 过滤掉多余的空格
    message = list(filter(lambda x: True if x.isdigit() else False, message))  # 去除非纯文本的时间轴
    array_length = len(message)
    if array_length <= 1:
        await bot.finish(ev, "参数不足：请至少输入一个原始轴时间" + help_use_str)
    if array_length >= 35:
        # 长度限制,可视情况解除
        await bot.finish(ev, "原始轴过长，请分开两次计算")
    send_text = handle_main(message[0], message[1:])
    await bot.send(ev, send_text)
