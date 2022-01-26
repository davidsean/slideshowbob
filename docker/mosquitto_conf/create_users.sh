#!/bin/ash
# set -e

# create client passwords
# make sure to define PUB_PASSWORD and SUB_PASSWORD in the .env
echo "pub_client:$PUB_PASSWORD" > /mosquitto/passwords.txt
echo "sub_client:$SUB_PASSWORD" >> /mosquitto/passwords.txt
mosquitto_passwd -U /mosquitto/passwords.txt

# Set permissions
user="$(id -u)"
if [ "$user" = '0' ]; then
	[ -d "/mosquitto" ] && chown -R mosquitto:mosquitto /mosquitto || true
fi

exec "$@"
