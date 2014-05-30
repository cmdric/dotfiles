#!/usr/bin/sh
source $HOME/.Xdbus
export SSH_AUTH_SOCK=/tmp/potterat/ssh-agent.sock
if [ ! -L $SSH_AUTH_SOCK ]; then
    export SSH_AUTH_SOCK=/tmp/ssh-agent.sock
fi

export baseDir=/home/potterat/CERN/notes/toBeWatched/
toBeChecked=(ParticleFowINT ZbANANOTE)

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
