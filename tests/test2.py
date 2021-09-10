import time
import sys

from auto_run_on_remote.run_script_on_remote_server import run_current_script_on_remote


run_current_script_on_remote()
# 以下的代码的print都不是在当前机器打印的，是在远程机器上打印的。

for i in range(10):
    print(f'嘻嘻 {i},通过文件路径和python解释器路径，可以发现这句话是在远程机器打印出来的, {__file__} ,{sys.executable} ')
    time.sleep(1)
