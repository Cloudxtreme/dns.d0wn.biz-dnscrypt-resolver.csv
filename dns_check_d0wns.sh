#!/bin/bash
#
# check d0wns DNS (dns.sh)
# last update: 2016-Aug-28 16-00
# https://vcp.ovpn.to/files/dns/dns_check_d0wns.sh

FILE=/var/www/files/dns/d0wns_dns.txt
LOGF=/var/www/files/dns/d0wns_dns.log

wget https://dns.d0wn.biz/dns.txt -O dns.txt
test -f ${FILE} || FILE=dns.txt
test -f ${LOGF} || LOGF=dns.log
BIN=/usr/local/sbin/dnscrypt-proxy
USER=dnscrypt-proxy
NOT_EXPIRE_IN_MINUTES=1440

echo "`date`" > "$LOGF";
while read LINE; do
 # get values from LINE
 ADDR=`echo "${LINE}"|cut -d, -f2`;
 NAME=`echo "${LINE}"|cut -d, -f1`;
 PROV=`echo "${LINE}"|cut -d, -f6`;
 KEY=`echo "${LINE}"|cut -d, -f5`;
 PORTS=`echo "${LINE}"|cut -d, -f7`;

 echo -en "\n${NAME} ${ADDR}:" >> "$LOGF";
 echo "`timeout 9 dig A omail.pro @${ADDR} |grep -E 'status|msec'`" >> "$LOGF";

 for PORT in ${PORTS}; do
  TEST="timeout 9 ${BIN} -t ${NOT_EXPIRE_IN_MINUTES} -u ${USER} -a 0.0.0.0:65123 -r ${ADDR}:${PORT} --provider-name=${PROV} --provider-key=${KEY}";
  #echo "${TEST}";
  which dnscrypt-proxy >/dev/null && echo -n "check ${NAME} ${ADDR}:${PORT} " && CMD=`${TEST}`;
  if [ $? -eq 0 ]; then
   MSG="`date`: ${NAME} ${ADDR}:${PORT} `echo "$CMD"|grep -i "valid\ from"| cut -d" " -f4,10` DNSCRYPT OK"; echo "OK";
  else
   MSG="`date`: ${NAME} ${ADDR}:${PORT} CERT FAILED"; echo "FAIL";
  fi;
 echo "${MSG}" >> "$LOGF";
 done;
done < <(cat ${FILE}); cat ${LOGF}; echo "#END ${LOGF}"; grep -iE 'fail' "$LOGF";
