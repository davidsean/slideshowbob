#!/bin/ash
# set -e

# create client passwords
# make sure to define PUB_PASSWORD and SUB_PASSWORD in the .env
echo "pub_client:$PUB_PASSWORD" >> /mosquitto/passwords.txt
echo "sub_client:$SUB_PASSWORD" >> /mosquitto/passwords.txt
mosquitto_passwd -U /mosquitto/passwords.txt

# create access control list
# only allow activity on the declared topic, read for sub_client and write for pub_client
echo "user sub_client" > /mosquitto/acl.txt
echo "topic read $TOPIC" >> /mosquitto/acl.txt
echo "user pub_client" >> /mosquitto/acl.txt
echo "topic write $TOPIC" >> /mosquitto/acl.txt

# Set permissions
user="$(id -u)"
if [ "$user" = '0' ]; then
	[ -d "/mosquitto" ] && chown -R mosquitto:mosquitto /mosquitto || true
fi

exec "$@"
