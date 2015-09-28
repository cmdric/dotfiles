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
export baseDir=svn+ssh://svn.cern.ch/reps/lhcb/
toBeChecked=(Analysis/trunk/Phys/JetTagging Analysis/trunk/Phys/JetAccessoriesMC Phys/trunk/Phys/JetAccessories)
#
for i in "${toBeChecked[@]}"
do
    export revT=$(svn info $baseDir$i | grep "Last Changed Rev" | cut -d ':' -f 2)
    IFS='/' read -ra FILE <<< "$i"
    export nfile=".${FILE[@]:(-1)}"
    pRev=$(cat $nfile)
    if [ $pRev != $revT ]; then
        echo $revT > .${FILE[@]:(-1)}
        pRev=$((pRev+1))
        svn log $baseDir$i -v -r $revT:$pRev > lastcommit.log
        export from="Cedric Potterat<cedric.potterat@cern.ch>"
        export recip="cedric.potterat@cern.ch"
        export subj="New Commit - Project: $i"
        printf "From: $from\nTo: $recip\nSubject: $subj\n\n last commits:\n\n" > mail.txt
        cat lastcommit.log >> mail.txt
        cat mail.txt | msmtp $recip
    fi
done
