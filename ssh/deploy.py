#!/usr/bin/env python

import os
import glob
import shutil
here = os.path.dirname( __file__ )

for link, target in ( ( ".ssh", os.path.join( here, "ssh" ) ) , ):
  target = os.path.realpath( target )
  link = os.path.expanduser( os.path.join( "~", link ) )
  if os.path.exists( link ):
    if os.path.islink( link ):
      if os.readlink( link ) == target:
        continue
    if os.path.isdir( link ):
      shutil.move( link, link+'.bak' )
  print "Linking %s -> %s" % ( link, target )
  os.symlink( target, link )
  if os.path.exists( link+'.bak' ):
      for fName in glob.glob(link+'.bak/*'):
          shutil.copy(fName, fName.replace('.bak',''))
      shutil.rmtree(link+'.bak')
  print "Fixing permissions of ssh folder"
  os.system('chmod 700 ~/dotfiles/ssh/ssh')
  os.system('chmod 644 ~/dotfiles/ssh/ssh/*')
  os.system('chmod 600 ~/dotfiles/ssh/ssh/id_dsa')
  os.system('chmod 600 ~/dotfiles/ssh/ssh/authorized_keys')
