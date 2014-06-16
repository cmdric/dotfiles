import os, time
import datetime
import DIRAC
from DIRAC.Interfaces.API.Dirac import Dirac
dirac = Dirac()
print dirac
time.sleep(4)
print dirac
from DIRAC.Core.Utilities.List import sortList, breakListIntoChunks
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager
rm = ReplicaManager()
print rm
time.sleep(4)
print rm
if not os.path.isfile('onGrid.txt'):
    os.system("touch onGrid.txt")
basedir = "/panasas/radiative/TupleProd/"
for (path, dirs, files) in os.walk(basedir):
  for file_ in files:
    #if os.path.splitext(file_)[1] != ".root":
    #  continue
    typea=path.split("/")
    if(typea[4] == 'Data'): continue
    full_file = os.path.join(path, file_)
    f1l = open('onGrid.txt','r')
    sent = f1l.read()
    f1l.close()
    hasbeensent = sent.split("\n")
    print full_file
    if full_file in hasbeensent:
      print "already copied"
      continue
    if os.path.splitext(file_)[1] == ".txt":
      #continue
      f1l = open(full_file,'r')
      fread = f1l.read()
      f1l.close()
      hasbeensent2 = fread.split("\n")
      if not hasbeensent2[0] == "done":
        #need to be modified to have a different GUID for each file
        print "not done for GUID"
        f1l = open(full_file,'w')
        f1l.write('done'+'\n'+'on grid/castor: done'+'\n'+'number of event processed of type '+ typea[len(typea)-2]+' stripping '+ typea[len(typea)-1]+ ': '+hasbeensent2[0]+'\n'+str( datetime.datetime.now() ))
        f1l.close()
    mypfn = full_file
    dirac = Dirac()
    lfn = full_file.replace('/panasas/radiative/', '/lhcb/user/p/potterat/')
    print lfn
    metaData = dirac.getMetadata(lfn)
#    metaData = metaData['Value']['Successful'][lfn]
   # metaData2 = metaData2['Value']['Successful'][lfn2]
    print metaData
    if len(metaData['Value']['Successful']) < 1:
      test = dirac.addFile( lfn, mypfn, 'CERN-USER',  DIRAC.makeGuid(mypfn))
      print test
      if(test.has_key('Message')):
        #GUID Exists !
        test2 = test['Message'].split(" try again. ")
        print "remove the wrong path"
        rm.removeFile(test2[1])
        dirac.addFile( lfn, mypfn, 'CERN-USER',  DIRAC.makeGuid(mypfn))
     # mypfn.upload(lfn,'CERN-USER')
      print full_file,"copied to",lfn
      f1l = open('onGrid.txt','w')
      f1l.write(sent+full_file+'\n')
      f1l.close()
    else :
      if (metaData['Value']['Successful'][lfn]['Size'] == os.path.getsize(full_file)):
        print " "
        print " "
        print "already done"
        print " "
        print " "
        f1l = open('onGrid.txt','w')
        f1l.write(sent+full_file+'\n')
        f1l.close()
        continue
      else:
        print metaData['Value']['Successful'][lfn]['Size'], os.path.getsize(full_file)
        print "remove : error in the sizes"
        rm.removeFile(lfn)
        dirac.addFile( lfn, mypfn, 'CERN-USER',  DIRAC.makeGuid(mypfn))
        print full_file,"copied to",lfn
        f1l = open('onGrid.txt','w')
        f1l.write(sent+full_file+'\n')
        f1l.close()
      print full_file,"STRANGE",lfn
      f1l = open('onGridSTRANGE.txt','w')
      f1l.write(sent+full_file+'\n')
      f1l.close()

