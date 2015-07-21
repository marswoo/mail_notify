#!/bin/sh

cwd=`dirname $0`

echo "alarm:" $1 $2 $4
EMAILFrom="woody213@yeah.net"
EMAILTo=$1
#SMTPServer="smtp.alibaba-inc.com:465"
#SMTPServer="smtp.ops.aliyun-inc.com"
#SMTPServer="smtp-inc.alibaba-inc.com"
SMTPServer="smtp.yeah.net"

Subject="$2"
Emailbody="$3"
$cwd/sendEmail -s "${SMTPServer}" -f "${EMAILFrom}" -t "${EMAILTo}" -u "${Subject}"  -m "${Emailbody}" -a "${File}" -xu "woody213@yeah.net" -xp "iamwhoiam126" -o message-charset="utf-8"
