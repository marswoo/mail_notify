#!/usr/local/bin/sh
#### generate daily configure file ####
ROOT_DIR=`pwd`
LOG_DIR=$ROOT_DIR/log

DATE=$1
mkdir -p $LOG_DIR/$DATE/

if [ $# -ne 3 ]
then
	echo " USAGE: run.sh i task_name run/test/debug"
	exit 0
else
	task_name=$2 #例如 disp_outer_log_stat
	mode=$3
    #report.sh 生成展示html
	./report.sh $DATE $task_name #2>$LOG_DIR/$DATE/err.log
    echo "sending mail..."
    ./mail.py $DATE $task_name $mode
    echo "send finish"
fi
