#!/bin/bash

ln -s /usr/bin/python3 /usr/bin/python

#python run_server.py
python -m uvicorn main:app --host 0.0.0.0 --port 8088
