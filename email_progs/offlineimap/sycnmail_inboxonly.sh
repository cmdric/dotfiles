#!/usr/bin/env bash

# Check every ten seconds if the process identified as $1 is still 
# running. After 5 checks (~60 seconds), kill it. Return non-zero to 
# indicate something was killed.
#touch $HOME/.Xdbus
#chmod 600 $HOME/.Xdbus
#env | grep DBUS_SESSION_BUS_ADDRESS > $HOME/.Xdbus
#echo 'export DBUS_SESSION_BUS_ADDRESS' >> $HOME/.Xdbus

sendmailcommand="$HOME/.msmtp/msmtp-runqueue.sh"
source $HOME/.Xdbus
#Check connection status
if ! ping -c1 www.google.com > /dev/null 2>&1; then 
    # Ping could be firewalled ...
    # '-O -' will redirect the actual html to stdout and thus to /dev/null
    if ! wget -O - www.google.com > /dev/null 2>&1; then
        # Both tests failed. We are probably offline 
        # (or google is offline, i.e. the end has come)
        exit 1;
    fi
fi


#(${sendmailcommand} &> ~/.msmtp/queue.log) &
monitor() {
    local pid=$1 i=0

    while ps $pid &>/dev/null; do
        if (( i++ > 5 )); then
            echo "Max checks reached. Sending SIGKILL to ${pid}..." >&2
            kill -9 $pid; return 1
        fi

        sleep 10
    done

    return 0
}

read -r pid < ~/.offlineimap/pid

if ps $pid &>/dev/null; then
    echo "Process $pid already running. Exiting..." >&2
    exit 1
fi
offlineimap -o -qf INBOX -u quiet & monitor $!