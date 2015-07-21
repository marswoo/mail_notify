#used to generate configure file of each task
task_name=$1
if [ $task_name != '' -a ! -d ./task/${task_name}/ ]
then
	#### creat conf dir
	mkdir -p ./task/${task_name}/
	cp ./resource/report_pipeline.conf ./task/${task_name}/
	cp -r ./resource/conf ./task/${task_name}/
	cp -r ./resource/*.sh ./task/${task_name}/
	#### creat report dir
	mkdir ./task/${task_name}/report/  
	#### creat data_processor
	mkdir ./task/${task_name}/data_processor/ ./task/${task_name}/data_processor/data/
fi



