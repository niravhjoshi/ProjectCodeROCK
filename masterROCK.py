import fileinput
import sys
import os
import bz2
from bz2 import decompress
import  re


accountname = {'1':'WK','2':'INAIL','3':'WIPRO','4':'CAP','5':'BB'}
appserverlist ={'1':'App1','2':'App2','98':'App98','99':'App99'}
moname ={'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'June','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

errorrepopath = "C:\\ROCKwall\\July Data\\ErrorDict.txt"
pathcompressfile ="C:\\ROCKwall\\July Data\\RawData\\"

Decompressfilepath = "C:\\ROCKwall\\July Data\\RawData\\Decompress\\"

#Regex pattern example
pattern1 =re.compile('^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}')
pattern2 = re.compile('\d+ ERROR [()[\]{}][a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+[()[\]{}]')
regex  = re.compile('0500 ERROR [()[\]{}][a-z]+[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.+[[\]{}]')


def DecompressBZ2files(userInDir):
    Decomdirpath = Decompressfilepath+gsrvname
    bz2filepath = pathcompressfile+gsrvname
    if not os.path.exists(Decomdirpath):
        os.makedirs(Decomdirpath)

    for file in os.listdir(bz2filepath):
        archive_path = os.path.join(pathcompressfile+gsrvname, file)
        outfile_path = os.path.join(Decompressfilepath+gsrvname, file[:-4])
        with open(archive_path, 'rb') as source, open(outfile_path, 'wb') as dest:
            dest.write(bz2.decompress(source.read()))
    print "Decmpression has been done for " +gsrvname

def PatternMatchERROR():
    newpath = Decompressfilepath+gsrvname
    opfilepath = Decompressfilepath
    concluerrfile = open(os.path.join(opfilepath,gsrvname+"conclusion"+"_"+gacctname+"_"+gmoname),"w")
    for eachfiles in os.listdir(newpath):
        i = 0
        openfilefullpath = os.path.join(newpath,eachfiles)
        openeachfile = open(openfilefullpath,'r')

        for eachlinesinfile in openeachfile:
            if re.match("(.*)(E)(R)(R)(O)(R)(.*)", eachlinesinfile, re.M):
                print >> concluerrfile,eachlinesinfile,
                i = i+1
        print "In Application server {} each day {}  Errors:{}".format(gsrvname,eachfiles[-10:],i)


#This function will just count error message reference to error dict and our conclusion file
def CountRepoErrorinConclufile():
    Countferrorrepo = errorrepopath
    Countconclufile = os.path.join(Decompressfilepath,(gsrvname+"conclusion"+"_"+gacctname+"_"+gmoname))
    Countferrorfile = open(Countferrorrepo)

    for errlines in Countferrorfile:  # Pick each line from error_dict
        Countnewerrlines = errlines.strip() # Strip error dict file line for any unwanted things
        confile = open(Countconclufile,"r+")#This will keep opening file every time when we need new error to search.
        confilelines = confile.readlines() #This will read all lines from file.
        confile.seek(0)
        c=0
        for eachlineinconfile in confilelines:
            new_eachlineinconfile = eachlineinconfile.strip()
            if Countnewerrlines in new_eachlineinconfile:
                c=c+1
        print "This line counts {}  ====>{}".format(Countnewerrlines,c)

#Use delimeter  format and export this result in to CSV -- Add feature

#This function will be matching error lines from error repo files and if matched it will yank those lines from the files.
def MatchandYankerrors():
    ferrorrepo = errorrepopath
    conclufile = os.path.join(Decompressfilepath,(gsrvname+"conclusion"+"_"+gacctname+"_"+gmoname))
    ferrorfile = open(ferrorrepo)
    output = []

    for errlines in ferrorfile: #Pick each line from error_dict
        c = 0
        newerrliens = errlines.strip()  # error_dict file each line strip and spilit
        #confile = open(conclufile,"r+")#This will keep opening file every time when we need new error to search.
        #confilelines = confile.readlines() #This will read all lines from file.
        #confile.seek(0)
        i=0
        for line in fileinput.input(conclufile,inplace=1,backup='.orig'):
            line = line.strip()
            if newerrliens in line:
                pass
            else:
                print line
        fileinput.close()







def main():
    #Global Varialble for storing.
    global gmoname
    global gacctname
    global gsrvname

    #select Month Name
    for mname in moname:
        print(mname, moname[mname])
    miname = raw_input("Which month you want to go with Please enter number:-")
    print "You have selected Month =>  {}".format(moname[miname])
    gmoname = moname[miname]
    print gmoname

    # Select account Name
    for accname in accountname:
        print(accname, accountname[accname])
    acctname = raw_input("Which account you want to go with Please enter number:-")
    print "You have selected Account =>  {}".format(accountname[acctname])
    gacctname = accountname[acctname]
    print gacctname

    #select account name
    while True:

        try:
            for appsrv in appserverlist:
                print(appsrv, appserverlist[appsrv])
            appsrvname = int(raw_input("Which Server  you want to go with Please enter number:-"))

        except ValueError:
            if appsrvname not in appserverlist:
                print "Sorry Wrong Input:"
            continue

        else:
            appsrvname = str(appsrvname)
            if appsrvname not in appserverlist:
                print "Your number is not in server list"
                continue
            print "You have selected App Server => {}".format(appserverlist[appsrvname])
            gsrvname =appserverlist[appsrvname]
            print gsrvname
            break



    # Add Input to point user where there download zip files are located in directory.
    user_dirInput = raw_input("Please enter file path where you have downloaded files in folder:->")
    assert os.path.exists(user_dirInput),"I could not find that path in your file system please ensure it is correct!!! " +str(user_dirInput)




    DecompressBZ2files(str(user_dirInput))

    PatternMatchERROR()#Calling ERROR Keyword matching function
    CountRepoErrorinConclufile()
    MatchandYankerrors()


if __name__ == '__main__':
    main()

