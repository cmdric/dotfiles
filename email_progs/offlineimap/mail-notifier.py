#!/usr/bin/env python

import os, gtk, pynotify, rfc822, email.header, email.charset, re, imaplib, time

# This utility monitors maildirs and IMAP boxes
# it emits a notification when new messages arrive.

# How frequently to check for new messages, in seconds
CHECK_FREQUENCY = 300
BOXES = {
    "Home": "maildir:/home/potterat/.mail/Gmail/INBOX/",
#    "Remote": "imaps://user:pass@host.com/Inbox"
}

# Title for notification bubbles
NOTIFY_TITLE="New Mail"
NOTIFY_ICON="/usr/share/icons/gnome/48x48/actions/mail_new.png"

# Output some messages to console.
DEBUG_LEVEL = 1

# Shorten long names or subjects to a maximum of:
MAX_HEADER_LENGTH = 40

class MailNotifier:

    ids_seen = []

    def __init__(self):
        # Register with notification system
        if pynotify.init( ("New Mail") ):
            DEBUG("Registered with Notification system")
            self.notify = True
        else:
            DEBUG("Failed Registration with Notification system")
            self.notify = False

    def run(self):
        # This is the main loop
        self.check_mailboxes()
        gtk.timeout_add(CHECK_FREQUENCY * 1000, self.check_mailboxes)
        gtk.main()

    def check_mailboxes(self):
        DEBUG("Begin Mail Check")
        noticecount = 0
        totalunseen = 0
        new_messages = {} # { box: [sender: subject, sender: subject, sender: subject], ...}

        # Check mailboxes for new mail
        for name, path in BOXES.iteritems():
            try:
                if path.startswith("maildir:"):
                    path = path[8:]
                    DEBUG("Checking '%s' as maildir" % path)
                    # Get a count of "new" mail.
                    # TODO: Should check for unseen mail in cur
                    messages = os.listdir(path + "new")
                    count = len(messages)
                    totalunseen += count
                    DEBUG("Got %d messages" % count)
                    # get sender names and titles for new messages
                    for message in messages:
                        # build an rfc822 object to access email data
                        fh = open( os.path.join(path, "new", message) )
                        parsed_message = rfc822.Message(fh)
                        fh.close()

                        messageid = parsed_message["Message-ID"]
                        DEBUG("Found message ID: " + messageid)
                        if not messageid in self.ids_seen:
                            self.ids_seen.append(messageid)
                            noticecount += 1
                            sender = get_parsed_header(parsed_message, "From")
                            subject = get_parsed_header(parsed_message, "Subject")
                            if new_messages.has_key(name):
                                new_messages[name] += "\n<b>" + sender + "</b>: " + subject
                            else:
                                new_messages[name] = "<b>" + sender + "</b>: " + subject

                elif path.startswith("imap"):
                    rex = re.findall(r"(.+?)\:\/\/(.+?):(.+?)@(.+?)/(.+?)$", path)[0]
                    if len(rex) < 5:
                        DEBUG("Not enough components to imap URL %s (got: %s)" % (path, str(rex)))
                        raise Exception("Not enough components to imap URL %s (got: %s)" % (path, str(rex)))
                    protocol = rex[0]
                    host = rex[3]
                    username = rex[1]
                    password = rex[2]
                    box = rex[4]
                    DEBUG("imap: proto=%s, host=%s, username=%s, password=%s, box=%s" % (protocol, host, username, password, box))

                    imap_server = None
                    if protocol == "imaps":
                        imap_server = imaplib.IMAP4_SSL(host, 993)
                    elif protocol == "imap":
                        imap_server = imaplib.IMAP4(host, 143)
                    else:
                        DEBUG("Unrecognised protocol %s" % protocol)
                        raise Exception("Unrecognised protocol %s" % protocol)

                    imap_server.login(username, password)
                    DEBUG("IMAP login successful")
                    typ, data = imap_server.select(box, True)
                    DEBUG("SELECT %s" % box)
                    if typ != "OK":
                        DEBUG("IMAP error %s" % typ)
                        raise Exception("IMAP error %s" % typ)
                    DEBUG("SEARCH UNSEEN")
                    (retcode, msgs) = imap_server.search(None, "(UNSEEN)")
                    count = len(msgs[0].split(" "))
                    totalunseen += count
                    DEBUG("Got %d messages" % count)
                    for num in msgs[0].split(" "):
                        typ, data = imap_server.fetch(num, '(RFC822)')
                        msg = email.message_from_string(data[0][1])
                        messageid = msg["Message-ID"]
                        DEBUG("Found message ID: " + messageid)
                        if not messageid in self.ids_seen:
                            self.ids_seen.append(messageid)
                            noticecount += 1
                            sender = get_parsed_header(msg, "From")
                            subject = get_parsed_header(msg, "Subject")
                            if new_messages.has_key(name):
                                new_messages[name] += "\n<b>" + sender + "</b>: " + subject
                            else:
                                new_messages[name] = "<b>" + sender + "</b>: " + subject
                    imap_server.logout()

            except Exception, e:
                DEBUG(str(e))
            except OSError,ose:
                DEBUG(str(ose))

            DEBUG("checking '" + name + "': " + str(totalunseen) + " new messages detected", 2)

        if ( noticecount > 0 ):
            # format our notification
            notify_text = ""
            for box in sorted(new_messages.iterkeys()):
                notify_text += "\n\n<b>" + box + "</b>\n\n" + new_messages[box]
            notify_text = str(noticecount) + " new email messages:" + notify_text
            DEBUG(notify_text)
            self.sendnotify(notify_text)
        return True

    def sendnotify(self, message):
        if not self.notify:
            DEBUG("Bypassing notification")
            return True
        DEBUG("Sending notification")
        n = pynotify.Notification(NOTIFY_TITLE, message, NOTIFY_ICON)
        n.show()
        return n

def get_parsed_header(parsed_message, header_name):
    header = parsed_message[header_name]
    header = email.header.decode_header(header)
    if  header[0][1] != None: # no charset specified
        header = unicode(header[0][0], header[0][1])
    else: # charset specified
        header = unicode(header[0][0])
    if header_name == "From":
        # Remove email address and just give name
        header = header.split(" <", 1)[0]
    if len(header) > MAX_HEADER_LENGTH:
        header = header[:MAX_HEADER_LENGTH-3] + "..."
    return header

def DEBUG(message, level = 1):
   if DEBUG_LEVEL >= level:
      print message

if __name__ == "__main__":
    # wait for desktop to come up first
    time.sleep(10)
    notifier = MailNotifier()
    notifier.run()

