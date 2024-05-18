import re

def validate_and_convert(input_string):
    # 使用正则表达式检查输入格式是否合适
    if re.match(r'^\d+(,\d+)*$', input_string):
        # 将逗号分隔的数字字符串转换为整数列表
        port_list = [int(port) for port in input_string.split(',')]
        return port_list
    else:
        print("输入格式不正确，请输入逗号分隔的端口号列表，如：80,443,22")
        return None

# 示例输入
user_input = input("请输入端口号列表：")

# 验证并转换用户输入
ports = validate_and_convert(user_input)
if ports:
    print("转换后的端口列表：", ports)
