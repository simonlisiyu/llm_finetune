import subprocess


# 用于运行脚本并将输出日志返回
def run_script_and_return_output(script, args1, args2, args3):
    script_args = [args1, args2, args3]
    command = [script] + script_args
    print("离线任务开始执行:", command)
    result = subprocess.run(command, shell=False, capture_output=True, text=True)
    print("离线任务执行完成:", result)
    if result.returncode == 0:
        print("脚本执行成功")
        print("输出信息 stdout：", result.stdout, "输出信息 stderr：", result.stderr)
    else:
        print("脚本执行失败")
        print("输出信息 stdout：", result.stdout, "输出信息 stderr：", result.stderr)


# 用于运行脚本并将输出写入日志文件
# 使用 subprocess.Popen 函数启动子进程，并使用 subprocess.PIPE 捕获其标准输出和标准错误
import threading


def capture_output(process, log_file):
    for line in process.stdout:
        log_file.write(line)
        print(line)
        log_file.flush()  # 刷新缓冲区，确保实时写入日志文件


def run_script_and_log_output(script_path, log_file_path):
    # 打开日志文件以追加模式写入
    with open(log_file_path, 'a') as log_file:
        # 使用 Popen 启动子进程
        process = subprocess.Popen(script_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # 创建线程来处理输出
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()

        # 等待子进程完成
        process.wait()

        # 等待输出线程完成
        output_thread.join()


# 示例用法
script_path = '../scripts/test.sh'  # 替换为您要运行的脚本路径
script_args = ["arg1", "arg2"]  # 替换为脚本参数
log_file_path = 'output.log'  # 替换为日志文件路径

command = [script_path] + script_args
run_script_and_log_output(command, log_file_path)
# run_script_and_return_output(script_path, "arg1", "arg2", "arg3")