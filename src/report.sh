#!/bin/sh
#### generate daily configure file ####

if [ $# -ne 2 ]
then
	echo " USAGE: report.sh i task_name"
	exit 0
else
	DATE=$1
	task_name=$2
fi

DIR_TASK=../task/${task_name}
DIR_REPORT=${DIR_TASK}/report
DIR_CONF=${DIR_TASK}/conf
DIR_DATA=${DIR_TASK}/data_processor/data

DIR_RESOURCE=../resource
DIR_SRC=`pwd`

echo report.sh: $DATE
DATEFORMAT=$DATE
if [ -e ${DIR_TASK}/report_pipeline.conf ]
then

	mkdir -p ${DIR_REPORT}/${DATE}
	if [ ! -e ${DIR_CONF}/header/header.html ]
	then
	    cp ${DIR_RESOURCE}/header.html ${DIR_CONF}/header/header.html
	fi
    
    echo ${DIR_RESOURCE}/footer.html
	if [ ! -e ${DIR_CONF}/footer/footer.html ]
	then
	    cp ${DIR_RESOURCE}/footer.html ${DIR_CONF}/footer/footer.html
	fi

	${DIR_SRC}/configure_replace.py ${DIR_CONF}/header/header.json ${DATEFORMAT}  ${DIR_CONF}/header/header.html ${DIR_REPORT}/${DATE}/header.html
	cp ${DIR_RESOURCE}/footer.html ${DIR_REPORT}/${DATE}/footer.html

	${DIR_SRC}/body_report.py ${DIR_TASK}/report_pipeline.conf ${DATE}
	
	cat ${DIR_REPORT}/${DATE}/header.html ${DIR_REPORT}/${DATE}/body.html ${DIR_REPORT}/${DATE}/footer.html > ${DIR_REPORT}/${DATE}/report.html

else
    echo "no ${DIR_TASK}/report_pipeline.conf"
fi
