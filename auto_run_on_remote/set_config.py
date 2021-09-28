# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/4/11 0011 0:56
"""

使用覆盖的方式，做配置。
"""
import sys
import importlib
from pathlib import Path
from shutil import copyfile
import nb_log  # noqa
from auto_run_on_remote import remote_config

PACKAGE_NAME = 'auto_run_on_remote'
DEFAULT_CONFIG_MODLUE = 'remote_config'
CUSTOM_CONFIG_MODULE_NAME = 'auto_run_on_remote_config'

custom_config_module_path = Path(sys.path[1]).absolute() / Path(f'{CUSTOM_CONFIG_MODULE_NAME}.py')


def use_config_form_config_module():
    """
    自动读取配置。会优先读取启动脚本的目录的distributed_frame_config.py文件。没有则读取项目根目录下的distributed_frame_config.py
    :return:
    """

    try:
        m = importlib.import_module(CUSTOM_CONFIG_MODULE_NAME)
        msg = f'{PACKAGE_NAME} 包 读取到\n "{m.__file__}:1" 文件里面的变量作为优先配置了\n'
        print(msg)
        for var_namex, var_valuex in m.__dict__.items():
            if var_namex.isupper():
                setattr(remote_config, var_namex, var_valuex)
    except ModuleNotFoundError:
        auto_creat_config_file_to_project_root_path()
        msg = f'''在你的项目根目录下生成了 \n "{custom_config_module_path}:1" 的 {PACKAGE_NAME} 包 的配置文件，快去看看并修改一些自定义配置吧'''
        print(msg)


def auto_creat_config_file_to_project_root_path():
    # print(Path(sys.path[1]).as_posix())
    # print((Path(__file__).parent.parent).absolute().as_posix())
    """
    :return:
    """
    if Path(sys.path[1]).as_posix() in Path(__file__).parent.absolute().as_posix():
        print('不希望在本项目里面创建')
        return
    # noinspection PyPep8
    """
        如果没设置PYTHONPATH，sys.path会这样，取第一个就会报错
        ['', '/data/miniconda3dir/inner/envs/mtfy/lib/python36.zip', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/lib-dynload', '/root/.local/lib/python3.6/site-packages', '/data/miniconda3dir/inner/envs/mtfy/lib/python3.6/site-packages']
        
        ['', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\python36.zip', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\DLLs', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\multiprocessing_log_manager-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pyinstaller-3.4-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pywin32_ctypes-0.2.0-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\altgraph-0.16.1-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\macholib-1.11-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\pefile-2019.4.18-py3.6.egg', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\win32\\lib', 'F:\\minicondadir\\Miniconda2\\envs\\py36\\lib\\site-packages\\Pythonwin']
    """
    if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
        raise EnvironmentError('''如果用pycahrm启动，默认不需要你手动亲自设置PYTHONPATH，如果你是cmd或者shell中直接敲击python xx.py 来运行，
                               报现在这个错误，你现在肯定是没有设置PYTHONPATH环境变量，不要设置永久环境变量，设置临时会话环境变量就行，
                               windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令    
                               要是连PYTHONPATH这个知识点都不知道，那就要google 百度去学习PYTHONPATH作用了，非常重要非常好用，
                               不知道PYTHONPATH作用的人，在深层级文件夹作为运行起点导入外层目录的包的时候，如果把深层级文件作为python的执行文件起点，经常需要到处很low的手写 sys.path.insert硬编码，这种方式写代码太low了。
                               知道PYTHONPATH的人无论项目有多少层级的文件夹，无论是多深层级文件夹导入外层文件夹，代码里面永久都不需要出现手动硬编码操纵sys.path.append
                               ''')
    # with (Path(sys.path[1]) / Path('nb_log_config.py')).open(mode='w', encoding='utf8') as f:
    #     f.write(config_file_content)
    copyfile(Path(__file__).parent / Path(f'{DEFAULT_CONFIG_MODLUE}.py'), custom_config_module_path)


use_config_form_config_module()
