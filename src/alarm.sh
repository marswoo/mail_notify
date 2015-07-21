#!/bin/sh

cwd=`dirname $0`

echo "alarm:" $1 $2 $4
EMAILFrom="display-algo-mid-log@alibaba-inc.com"
EMAILTo=$1
#SMTPServer="smtp.alibaba-inc.com:465"
#SMTPServer="smtp.ops.aliyun-inc.com"
SMTPServer="smtp-inc.alibaba-inc.com"

Subject="$2"
Emailbody="$3"
$cwd/sendEmail -s "${SMTPServer}" -f "${EMAILFrom}" -t "${EMAILTo}" -u "${Subject}"  -m "${Emailbody}" -a "${File}" -xu "display-algo-mid-log@alibaba-inc.com" -xp "Displayalgo1234" -o message-charset="utf-8"
