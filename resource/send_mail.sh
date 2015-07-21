#!/bin/bash
#只在gateway上跑job，然后scp到开发机

source /home/yasong.lys/.bashrc
task_path=$(readlink -f $(dirname $0))
source $task_path/conf/main.conf
force=""
mode="run"
plot="noplot"
recompute="false"

#r参数一般不用，除非在日报指标发生增减修改，加上r就会重跑过去7天的指标数据
while getopts "vfdrt:" opt
do
    case $opt in
        t) ago=$OPTARG;;
        v) set -eux;;
        f) force="-f";;
        d) mode="debug";;
		p) plot="plot";;
        r) recompute="true";;
        *) echo "Invalid option.";;
    esac
done

################################
# run job
################################

DATE=`date -d "$ago day ago" +%Y%m%d`

if [ -z "$DATE" ]; then
    echo "DATE is empty in daily_run.sh"
    exit
fi
echo DATE: $DATE
echo "runing $mode mode!!"

task_name=disp_outer_log_stat.1
job_scripts_path=$task_path/../../../DisplayAdGuarder
hadoop_output_path=/group/tbalgo-dev/cloud_resys/DiamondLogsDailyReport

#如果加上参数r，则会重新跑跑去7天的job，否则只算ago天前的当天job，当然job具体是否会执行还要看参数f。
recompute_days=1
if [ $recompute = "true" ];then
	recompute_days=7
fi
beg=$(($ago+$recompute_days-1))
while [ $beg -gt $(($ago-1)) ]
do
	cd $job_scripts_path/scripts
    SOMEDAY=`date -d"$beg day ago" +"%Y%m%d"`
    if [ ! -e $task_path/data_processor/raw_data/$SOMEDAY/ ]; then
        mkdir $task_path/data_processor/raw_data/$SOMEDAY/
    fi
    if [ ! -e $task_path/data_processor/data/$SOMEDAY/ ]; then
        mkdir $task_path/data_processor/data/$SOMEDAY/
    fi
    ################################
    # merge adMidTier
    ################################
    #sh TransStatNewMerge.sh $force -b ${SOMEDAY}
    
    
    ################################ 
	# 产出钻展总体关键指标
    ################################
    sh keyIndictor.sh $force -b ${SOMEDAY}
    hcat $hadoop_output_path/KeyIndictorStat/$SOMEDAY/* > $task_path/data_processor/raw_data/$SOMEDAY/key_indictor_data

    ################################ 
	# 产出单个pid关键指标
    ################################
    sh pidKeyIndictor.sh $force -b ${SOMEDAY}
    hcat $hadoop_output_path/PidKeyIndictor/$SOMEDAY/* > $task_path/data_processor/raw_data/$SOMEDAY/pid_key_indictor_data

    ################################ 
	# 从云梯直接获取当天pid对应名称
    ################################
	# 执行一遍，总是会出现name乱码，所以这里执行两遍
	htext /group/taobao/taobao/hive_data/ods/$SOMEDAY/s_ods_nz_z_adzone/* | awk -F"[\001\t]" '{printf "%s\t%s\n", $2, $3}' > $task_path/data_processor/raw_data/$SOMEDAY/adzone_name_data

	#复制raw数据到开发机
	#scp -r $task_path/data_processor/raw_data/$SOMEDAY `whoami`@$ip:$raw_data_path

	#复制data数据到开发机
	#scp -r $task_path/data_processor/data/$SOMEDAY `whoami`@$ip:$data_path
    beg=$((beg - 1))
done

#touch $task_path/data_processor/raw_data/$DATE/flag.done
#scp $task_path/data_processor/raw_data/$DATE/flag.done `whoami`@$ip:$raw_data_path/$DATE

################################
# run stat
################################
cd $task_path/data_processor/scripts
rm -f ../data/$DATE/*.notation
cp ../data/*.notation ../data/$DATE

#生成email需要的数据
python2.7 key_gen_email_data.py --date $DATE
Rscript trend_report.R key_indictor_report $DATE 7 $plot
Rscript key_indictor.R $DATE
Rscript pid_key_indictor.R $DATE

#修改json的列名
sh modify_colname.sh $ago

#发email
cd $task_path/../../src/
./run.sh $ago $task_name $mode

