#!/bin/bash

#Create fifos for data delivery
if [ ! -d "/fifo" ]
then 
    mkdir /fifo
fi
if [ ! -p "/fifo/dataIN" ]
then
	mkfifo /fifo/dataIN
fi

python main.py -c 'config/config.json'

