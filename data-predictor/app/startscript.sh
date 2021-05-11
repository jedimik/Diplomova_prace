#!/bin/bash
if [ ! -d "/fifo" ]
then 
    mkdir /fifo
fi
if [ ! -p "/fifo/dataIN" ]
then
	mkfifo /fifo/dataIN
fi
python3 main.py -c "config/config.yaml"