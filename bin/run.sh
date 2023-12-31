#!/bin/bash

# Activate virtual environment if necessary
# source path/to/venv/bin/activate

# Define function to start the server
start_server() {
  cp -r config scripts/src/llmtuner/config
  if [ -n "$1" ]; then
    ln -s "$1"/* llm
  fi
  python main.py &
  echo "Server started."
}

# Define function to stop the server
stop_server() {
  kill $(lsof -t -i:8000)
  echo "Server stopped."
}

# Define function to restart the server
restart_server() {
  stop_server
  start_server
}

# Check for command line argument
if [ "$1" == "start" ]
then
  start_server $2
elif [ "$1" == "stop" ]
then
  stop_server
elif [ "$1" == "restart" ]
then
  restart_server $2
else
  echo "Usage: run.sh [start|stop|restart] [llm_dir]"
  exit 1
fi

exit 0