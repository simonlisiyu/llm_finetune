import subprocess

def run_server():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])
    # subprocess.run(["scripts/test.sh", "-l", "~/Downloads"], shell=False)

if __name__ == "__main__":
    run_server()
