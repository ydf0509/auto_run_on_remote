import sys
import re
import os
import time
import nb_log
from auto_run_on_remote.paramiko_util import ParamikoFolderUploader
from fabric2 import Connection
from auto_run_on_remote import remote_config
from auto_run_on_remote import set_config  # noqa

logger = nb_log.get_logger('run_script_on_remote_server')
python_proj_dir = remote_config.PYTHON_PROJ_DIR_LOCAL.replace('\\', '/')
if not python_proj_dir.endswith('/'):
    python_proj_dir += '/'
python_proj_dir_short = python_proj_dir.split('/')[-2]

if remote_config.USER == 'root':  # 文件夹会被自动创建，无需用户创建。
    remote_dir = f'/pycodes/{python_proj_dir_short}/'
else:
    remote_dir = f'/home/{remote_config.USER}/pycodes/{python_proj_dir_short}/'


def run_current_script_on_remote():
    if remote_config.FORBID_DEPLOY_FROM_LINUX and os.name == 'posix':
        # 一般生产机器是linux，是否禁止从linux部署到别的机器，这样可以防止你从生产环境远程到测试环境，配置后，即使生产环境的代码有远程部署，也不会执行远程部署而是直接运行。
        return
    if int(os.getenv('is_auto_remote_run', 0)) == 1:  # 不能循环递归远程启动。
        return
    logger.warning(f'将本地文件夹代码 {python_proj_dir}  上传到远程 {remote_config.HOST} 的 {remote_dir} 文件夹。')
    t_start = time.perf_counter()
    uploader = ParamikoFolderUploader(remote_config.HOST, remote_config.PORT, remote_config.USER, remote_config.PASSWORD,
                                      python_proj_dir, remote_dir,
                                      path_pattern_exluded_tuple=remote_config.PATH_PATTERN_EXLUDED_TUPLE,
                                      file_suffix_tuple_exluded=remote_config.FILE_SUFFIX_TUPLE_EXLUDED,
                                      only_upload_within_the_last_modify_time=remote_config.ONLY_UPLOAD_WITHIN_THE_LAST_MODIFY_TIME,
                                      file_volume_limit=remote_config.FILE_VOLUME_LIMIT, sftp_log_level=remote_config.SFTP_LOG_LEVEL)

    uploader.upload()
    logger.info(f'上传 本地文件夹代码 {python_proj_dir}  上传到远程 {remote_config.HOST} 的 {remote_dir} 文件夹耗时 {round(time.perf_counter() - t_start, 3)} 秒')
    # conn.run(f'''export PYTHONPATH={remote_dir}:$PYTHONPATH''')
    # 获取被调用函数所在模块文件名
    # print(sys._getframe())
    local_file_name = sys._getframe(1).f_code.co_filename.replace('\\', '/')  # noqa
    # file_name = re.sub(f'^{python_proj_dir}', '', local_file_name)
    file_name = re.sub(f'^{python_proj_dir}', remote_dir, local_file_name)  # 远程文件名字。
    process_mark = f'auto_remote_run_mark__{file_name.replace("/", "__")[:-3]}'

    conn = Connection(remote_config.HOST, port=remote_config.PORT, user=remote_config.USER, connect_kwargs={"password": remote_config.PASSWORD}, )
    kill_shell = f'''ps -aux|grep {process_mark}|grep -v grep|awk '{{print $2}}' |xargs kill -9'''
    logger.warning(f'{kill_shell} 命令杀死 {process_mark} 标识的进程')
    uploader.ssh.exec_command(kill_shell)
    # conn.run(kill_shell, encoding='utf-8')

    python_exec_str = f''' {remote_config.PYTHON_INTERPRETER} {file_name}  -auto_remote_process_mark {process_mark} '''
    shell_str = f'''export is_auto_remote_run=1;export PYTHONPATH={remote_dir}:$PYTHONPATH ;cd {remote_dir}; {python_exec_str}'''
    extra_shell_str2 = remote_config.EXTRA_SHELL_STR  # 内部函数对外部变量不能直接改。
    if not extra_shell_str2.endswith(';') and remote_config.EXTRA_SHELL_STR != '':
        extra_shell_str2 += ';'
    shell_str = extra_shell_str2 + shell_str
    logger.warning(f'使用语句 {shell_str} 在远程机器 {remote_config.HOST} 上启动脚本 {file_name}')
    conn.run(shell_str, encoding='utf-8')
    sys.exit()  # 使本机不执行代码。
