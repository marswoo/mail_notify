#!/bin/bash
#只在gateway上跑job，然后scp到开发机

task_path=$(readlink -f $(dirname $0))
force=""
mode="run"
plot="noplot"
recompute="false"
task_name=dolphin

#r参数一般不用，除非在日报指标发生增减修改，加上r就会重跑过去7天的指标数据
while getopts "vfdt:" opt
do
    case $opt in
        t) ago=$OPTARG;;
        v) set -eux;;
        f) force="-f";;
        d) mode="debug";;
        *) echo "Invalid option.";;
    esac
done

################################
# run stat
################################
#cd $task_path/data_processor/scripts
#rm -f ../data/$DATE/*.notation
#cp ../data/*.notation ../data/$DATE

#发email
cd $task_path/../../src/
./run.sh $ago $task_name $mode

