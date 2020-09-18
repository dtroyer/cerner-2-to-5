#!/bin/bash
# ddnsupdate - Update DNS for local machine (MacOS)
#
# ddnsupdate -4|-6 [-c] [-i <interface>] [fqdn]

set -x

ZONE=d.xr7.org
SERVER=ns1.xr7.org
TTL=600

[[ "$1" == "-4" ]] && DO_4=1 && shift && RR=A && \
    DATA=$(ipconfig getpacket en0 | awk "/yiaddr/ { print \$3 }")
[[ "$1" == "-6" ]] && DO_6=1 && shift && RR=AAAA && \
    DATA=$(ipconfig getv6packet en0 | awk "/IAADDR/ { if (\$8 != -1) { print \$6 } }")
[[ -z $RR ]] && echo "Specify -4 or -6" &&exit 1

INTERFACE=${INTERFACE:-en0}
FQDN=${FQDN:-$(hostname -s)}
KEYDIR=${HOME}/etc/bind/keys

LABEL=${FQDN}.${ZONE}
KEY=${KEYDIR}/${LABEL}.key
CMD="update delete ${LABEL} ${RR}"$'\n'"update add ${LABEL} ${TTL} ${RR} ${DATA}"

nsupdate -k ${KEY} -v <<EOF
server ${SERVER}
zone ${ZONE}
${CMD}
send
EOF

# cerner_2^5_2020
