## NO.1: monitor galaxy search product daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/web_search_daily_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 web_search_daily_monitor run >>out.log 2>>err.log
## NO.3: monitor cloudrec image/algorithm quality daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_quality_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_quality_monitor run >>out.log 2>>err.log
## NO.4: cloudrec_domain_monitor  daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_domain_monitor/data_processor; sh run_processor.sh 1 $2 >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_domain_monitor run >>out.log 2>>err.log
## NO.5: cloudrec_domain_index_monitor daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_domain_index_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_domain_index_monitor run >>out.log 2>>err.log
## NO.6: cloudrec_webpagerec_monitor daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_webpagerec_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_webpagerec_monitor run >>out.log 2>>err.log
## NO.7: cloudrcc_channel_monitor daily
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_channel_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_channel_monitor run >>out.log 2>>err.log
## NO.9: cloudrec_domainfluc_monitor daily  #need the data from cloudrec_quality_monitor
cd /dataAnlysis/logana_share/log_monitor_platform/task/cloudrec_domainfluc_monitor/data_processor; sh run_processor.sh >>out.log 2>>err.log; cd /dataAnlysis/logana_share/log_monitor_platform/src; sh run.sh 1 cloudrec_domainfluc_monitor run >>out.log 2>>err.log

