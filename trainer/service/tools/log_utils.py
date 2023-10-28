
def capture_output(process, log_file):
    for line in process.stdout:
        log_file.write(line)
        print(line)
        log_file.flush()  # 刷新缓冲区，确保实时写入日志文件
