0) install mutt, msmtp, offlineimap, python2-gnomekeyring
1) copy all *rc to ~/.*rci
2) copy mutt to ~/.mutt
3) copy offlineimap t0 ~/.offlineimap
4) crontab -e
5) */3 * * * * /path_to_sycmail.sh
6) copy xdbus.desktop to .config/autostart/.
7) logout and login
8) mutt.desktop -> /usr/share/applications/.