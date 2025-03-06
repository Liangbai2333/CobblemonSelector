import os


def resolve(file_path) -> str:
    """
    返回文件绝对路径
    :param file_path: 文件相对位置
    :return: 文件绝对路径
    """
    return os.path.join(os.path.join(os.getcwd(), "data"), file_path)

def get_file_name_without_ext(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]