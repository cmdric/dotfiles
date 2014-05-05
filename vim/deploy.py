#!/usr/bin/env python

import os
import shutil
here = os.path.dirname( __file__ )

for link, target in ( ( ".vimrc", os.path.join( here, "vimrc" ) ), ( ".vim", os.path.join( here, "vim" ) ) ):
  target = os.path.realpath( target )
  link = os.path.expanduser( os.path.join( "~", link ) )
  if os.path.exists( link ):
    if os.path.islink( link ):
      if os.readlink( link ) == target:
        continue
    if os.path.isdir( link ):
      shutil.rmtree( link )
    else:
      os.unlink( link )
  print "Linking %s -> %s" % ( link, target )
  os.symlink( target, link )

for dName in ( "backups", "swaps", "undo" ):
  dName = os.path.expanduser( os.path.join( "~", ".vim", dName ) )
  if not os.path.isdir( dName ):
    os.makedirs( dName )

if not os.path.exists(os.path.expandvars('$HOME/dotfiles/vim/vim/bundle/vundle')):
    os.system("git clone http://github.com/gmarik/vundle.git $HOME/dotfiles/vim/vim/bundle/vundle")
os.system("vim +BundleInstall +qall")
#os.system("mkdir vim/yankring_history")
