#!/usr/bin/sh
#
if ! ping -c1 www.google.com > /dev/null 2>&1; then 
    # Ping could be firewalled ...
    # '-O -' will redirect the actual html to stdout and thus to /dev/null
    if ! wget -O - www.google.com > /dev/null 2>&1; then
        # Both tests failed. We are probably offline 
        # (or google is offline, i.e. the end has come)
        exit 1;
    fi
fi
#
#
#
source $HOME/.Xdbus
export SSH_AUTH_SOCK=/tmp/$USER/ssh-agent.sock
if [ ! -L $SSH_AUTH_SOCK ]; then
    export SSH_AUTH_SOCK=/tmp/ssh-agent.sock
fi
#
export baseDir=$HOME/CERN/notes/toBeWatched/
toBeChecked=(ParticleFowINT ZbANANOTE JetAccessories JetAccessoriesMC)
#
for i in "${toBeChecked[@]}"
do
    cd $baseDir$i
    svn update > test.txt
    export nLines=$(wc -l test.txt)
    if [ "$nLines" != "2 test.txt" ]; then
        export revT=$(svn info | grep "Last Changed Rev" | cut -d ':' -f 2)
        svn log -v -r $revT > lastcommit.log
        export from="Cedric Potterat<cedric.potterat@cern.ch>"
        export recip=$(cat emails.txt)
        export subj="New Commit - Project: $i"
        printf "From: $from\nTo: $recip\nSubject: $subj\n\n last commit:\n\n" > mail.txt
        cat lastcommit.log >> mail.txt
        cat mail.txt | msmtp $recip
    fi
done
