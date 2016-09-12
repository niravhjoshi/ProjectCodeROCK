import fileinput
import sys
import os
import bz2
from bz2 import decompress
import  re


accountname = {'1':'WK','2':'INAIL','3':'WIPRO','4':'CAP','5':'BB'}
appserverlist ={'1':'App1','2':'App2','98':'App98','99':'App99'}
moname ={'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'June','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'}


#Regex pattern example
date_pattern1 =re.compile('^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3}')
only_datePattern2 = re.compile('^\d{4}-\d{2}-\d{2}')
pattern2 = re.compile('\d+ ERROR [()[\]{}][a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+[()[\]{}]')
regex  = re.compile('0500 ERROR [()[\]{}][a-z]+[a-z]+.[a-z]+.[a-z]+.[a-z]+.[a-z]+.+[[\]{}]')

#THis function will decompress files for respecitive app server
def DecompressBZ2files(userInDir,userOpDir):

    Decomdirpath = userOpDir+"\\"+gsrvname
    bz2filepath = userInDir+"\\"+gsrvname
    if os.path.exists(Decomdirpath) is False:
        os.makedirs(Decomdirpath)
        print "created dir decom"

    for file in os.listdir(bz2filepath):
        archive_path = os.path.join(userInDir+"\\"+gsrvname, file)
        outfile_path = os.path.join(userOpDir+"\\"+gsrvname, file[:-4])
        with open(archive_path, 'rb') as source, open(outfile_path, 'wb') as dest:
            dest.write(bz2.decompress(source.read()))
    print "Decmpression has been done for " +gsrvname


#This function will create new file named conclusion which will contain all error related lines only.
def PatternMatchERROR(userOpDir):
    newpath = userOpDir+"\\"+gsrvname
    opfilepath = newpath
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
def CountRepoErrorinConclufile(usererrordictpath,userOpDir):

    Countferrorrepo = usererrordictpath
    Countconclufile = os.path.join(userOpDir+"\\"+gsrvname,(gsrvname+"conclusion"+"_"+gacctname+"_"+gmoname))
    Countferrorfile = open(Countferrorrepo)

# We need put logic where after picking up each line from error dict file  it will search lines using date wise rather than just over seach from
#Conclusion File through which we will get more granualar report about understanding error pattern datewise.
    for errlines in Countferrorfile:
        groupbyDate = []  # Create List for the Dates Entries to be included.
        Countnewerrlines = errlines.strip() # Strip error dict file line for any unwanted things
        confile = open(Countconclufile,"r+")#This will keep opening file every time when we need new error to search.
        confilelines = confile.readlines() #This will read all lines from file.
        confile.seek(0)
        c=0
        for eachlineinconfile in confilelines:  # Pick each line from error_dict
            new_eachlineinconfile = eachlineinconfile.strip()  #

            if re.match(only_datePattern2,new_eachlineinconfile):
                newDate = new_eachlineinconfile[:10]
                if newDate not in groupbyDate:
                    groupbyDate.append(new_eachlineinconfile[:10])
                    errcnt = 0
                    print "Group Date==============================>:{}".format(groupbyDate[-1])



            if Countnewerrlines in new_eachlineinconfile:
                c=c+1
                errcnt = errcnt +1 # this count only set to 0 after new error picked up.
                print "This error {} came on {} these many times{} ".format(Countnewerrlines,errcnt,groupbyDate[-1])
        print "\n\nThis line counts {}  ====>{}".format(Countnewerrlines,c)

#Use delimeter  format and export this result in to CSV -- Add feature

#This function will be matching error lines from error repo files and if matched it will yank those lines from the files.
def MatchandYankerrors(usererrodict,userOpDir):
    ferrorrepo = usererrodict
    conclufile = os.path.join(userOpDir+"\\"+gsrvname,(gsrvname+"conclusion"+"_"+gacctname+"_"+gmoname))
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


#Main function of program.

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
    while True:
        user_dirInput = raw_input("Please enter file path where you have downloaded files in folder:->")
        if os.path.exists(user_dirInput) is False:
            print "I could not find that path in your file system please ensure it is correct!!! " +str(user_dirInput)
            continue
        else:
            pathcompressfile = str(user_dirInput)
            break

    #Please enter decompress path for your bz2 file if it is not there create it.
    while True:
        user_DecomDir = raw_input("Please enter path or location where you want to decompress files:->")
        if os.path.exists(user_DecomDir) is False:
            os.makedirs(user_DecomDir)
            print "New Dir is created at following location" +str(user_DecomDir)
            decompath = str(user_DecomDir)
            break
        else:
            print "Directory already there"
            decompath = str(user_DecomDir)
            break

    while True:
        user_errordict =  raw_input("Please enter full path of error dict file name:->")
        if os.path.exists(user_errordict) is False:
            print "I could not find that path in your file system please ensure it is correct!!! " + str(user_errordict)
            continue
        else:
            errordictfilepath = str(user_errordict)
            break





    #Calling All function one by one.
    DecompressBZ2files(str(user_dirInput),str(user_DecomDir))
    PatternMatchERROR(str(user_DecomDir))#Calling ERROR Keyword matching function
    CountRepoErrorinConclufile(str(user_errordict),str(user_DecomDir))
    #MatchandYankerrors(str(user_errordict),str(user_DecomDir))


if __name__ == '__main__':
    main()

