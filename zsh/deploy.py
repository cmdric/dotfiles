#!/usr/bin/env python

import sys, os

here = os.path.dirname( os.path.realpath( __file__ ) )

prezto_dir = os.path.expanduser(os.path.join("~", ".zprezto"))
# Check of prezto is already cloned
if os.path.isdir(prezto_dir):
    print "Seems oh-my-zsh is already installed in %s" % prezto_dir
else:
    os.environ[ "GIT_SSL_NO_VERIFY"] = "true"
    if os.system('git clone --recursive https://github.com/sorin-ionescu/prezto.git  "%s"' % prezto_dir) != 0:
        print "Cound not clone prezto into %s" % prezto_dir
        sys.exit(1)
    os.symlink(os.path.expanduser('~/dotfiles/zsh/prompt/prompt_apuignav_setup'),
               os.path.join(prezto_dir, 'modules/prompt/functions/prompt_apuignav_setup'))

