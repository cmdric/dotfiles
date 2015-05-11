0) install mutt, msmtp, offlineimap, python2-gnomekeyring, python2-keyring
1) copy all or ln *rc to ~/.*rc
2) copy or ln mutt to ~/.mutt
3) copy or ln offlineimap to ~/.offlineimap
4) crontab -e
5) */3 * * * * /path_to_sycmail.sh
6) copy xdbus.desktop to .config/autostart/.
7) logout and login
8) mutt.desktop -> /usr/share/applications/.
9) use offlineimap-gnome-tool.py to set up passowrd for offlineimap for gmail: server imap.gmail.com
10) save gmail goobok respct. via python2 "import keyring, keyring.set_password('cern','username','passwd') and ('gmail','username','passwd')"
10) save cern cred using msmtp-gnome-tool.py: server smtp.cern.ch
