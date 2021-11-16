# 1 安装

pip install auto_run_on_remote

# 2 auto_run_on_remote 介绍

```
全名字含义应该是 auto_run_current_python_script_on_remote_server

在本机运行脚本自动在远程机器上运行。

自动上传文件夹 自动创建文件夹 自动远程机器上运行python脚本。
原理是 run_current_script_on_remote() 函数中自动利用 sys._getframe(1).f_code.co_filename 获取当前文件位置，所以不用传参告诉函数当前脚本的位置。

比pycahrm专业版复杂的配置调用远程python解释器更方便，因为pycahrm专业版如果设置了远程解释器启动脚本时候很卡，启动ide界面更卡，因为ide会去读远程解释器的所有安装的python包，真的是太卡了。
而这个在远程运行启动速度就很快，丝毫不会造成ide卡顿。
```

# 3 用法如下
```
在项目的任意目录层级下的脚本中运行 run_current_script_on_remote(),则脚本会自动运行在远程机器。
当第一次运行脚本时候，会自动在你当项目的根目录生成 auto_run_on_remote_config.py 配置文件，然后，你自己按需修改其中的值。
以后运行run_current_script_on_remote()会自动读取到 auto_run_on_remote_config.py  中的配置。
```

```python
import time
import sys

from auto_run_on_remote import run_current_script_on_remote


run_current_script_on_remote()
# 以下的代码的print都不是在当前机器打印的，是在远程机器上打印的。

for i in range(10):
    print(f'嘻嘻 {i},通过文件路径和python解释器路径，可以发现这句话是在远程机器打印出来的, {__file__} ,{sys.executable} ')
    time.sleep(1)

```



代码运行截图，我本机是win10，可以看到代码是运行在linux的。
[![hXvZff.png](https://z3.ax1x.com/2021/09/10/hXvZff.png)](https://imgtu.com/i/hXvZff)


# 4 配置文件 auto_run_on_remote_config.py 介绍
```python
"""
这个配置文件是自动生成到你的项目根目录的。
"""

import sys

# 项目根目录文件夹，这个一般不需要改，会根据PYTHONPATH智能获取。
# pycahrm自动添加了项目根目录到第一个PYTHONPATH，如果是cmd命令启动这先设置PYTHONPATH环境变量。
# windows设置  set PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令
# linux设置    export PYTHONPATH=你当前python项目根目录,然后敲击你的python运行命令
PYTHON_PROJ_DIR_LOCAL = sys.path[1]

# 这是远程机器的账号密码配置。把这个配置文件加到gitignore就不会泄漏了。
HOST = '192.168.6.133'
PORT = 22
USER = 'ydf'
PASSWORD = '123456'

PYTHON_INTERPRETER = 'python3'  # 如果你安装了四五个python环境，可以直接指定远程解释器的绝对路径  例如 /opt/minicondadir/ens/env35/python

FORBID_DEPLOY_FROM_LINUX = True # 一般生产机器是linux，是否禁止从linux部署到别的机器，这样可以防止你从生产环境远程到测试环境，配置后，即使生产环境的代码有远程部署，也不会执行远程部署而是直接运行。

# 上传文件夹的配置，具体可以看paramiko_util.py里面的代码。
PATH_PATTERN_EXLUDED_TUPLE = ('/.git/', '/.idea/', '/dist/', '/build/')  # 路径中如果有这些就自动过滤不上传
FILE_SUFFIX_TUPLE_EXLUDED = ('.pyc', '.log', '.gz')  # 这些后缀的文件不上传
ONLY_UPLOAD_WITHIN_THE_LAST_MODIFY_TIME = 3650 * 24 * 60 * 60  # 只有在这个时间之内修改的文件才上传。如果项目比较大，可以第一次完整上传，之后再把这个时间改小。
FILE_VOLUME_LIMIT = 1000 * 1000  # 大于这个体积的文件不上传，单位b。
SFTP_LOG_LEVEL = 20  # 文件夹上传时候的日志级别。10 logging.DEBUG ,20 logging.INFO 30 logging.WaRNING,如果要看为什么某个文件上传失败，可以设置debug级别。

EXTRA_SHELL_STR = ''  # 远程执行命令之前，可以自定义执行的shell语句，一般例如可以设置啥环境变量什么的。


```
