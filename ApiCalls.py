import time,sys,os,requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import json,urllib2
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tools_logslocation = []

#Making call to api to get list of customer for which log monitoring is enable.
response_customerwihLogMonitoringOn = urllib2.urlopen("http://127.0.0.1:8000/logconfig/CustomerLoglocationapi?fields=cust_name,srv1_name_dir,srv2_name_dir,srv98_name_dir,srv99_name_dir,appsrv_tools_logpath&log_monitor=True")
data = json.load(response_customerwihLogMonitoringOn)
print len(data)
i = len(data)
j=0
while True:
    print j
    customer_name = data[j]['cust_name']
    customer_name = str(customer_name)
    tools_logslocation.append(customer_name)

    tools_path = data[j]['appsrv_tools_logpath']
    #ws_srv_path = data[j]['appsrv_localws_logpath']
    srv1dir = data[j]['srv1_name_dir']
    srv2dir = data[j]['srv2_name_dir']
    srv98dir = data[j]['srv98_name_dir']
    srv99dir = data[j]['srv99_name_dir']
    tools_srv1_path = tools_path + '/' + srv1dir
    tools_srv1_path = str(tools_srv1_path)
    tools_logslocation.append(tools_srv1_path)

    tools_srv2_path = tools_path + '/' + srv2dir
    tools_srv2_path = str(tools_srv2_path)
    tools_logslocation.append(tools_srv2_path)

    tools_srv98_path = tools_path + '/' + srv98dir
    tools_srv98_path = str(tools_srv98_path)
    tools_logslocation.append(tools_srv98_path)

    tools_srv99_path = tools_path + '/' + srv99dir
    tools_srv99_path = str(tools_srv99_path)
    tools_logslocation.append(tools_srv99_path)

    logger.info('Start customer name from API')
    print customer_name
    logger.info('Printing tools path')
    print tools_path

    j = j+1
    if j>=i:
        break
print tools_logslocation


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.BZ2", "*.bz2"]

    def process(self, event):
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug
        srcpath = event.src_path
        logger.info('Preparing command for sending file using scp')
        print "scp %s nirav.joshi@108.168.207.6:/home/nirav.joshi" %srcpath
        logger.info('SCPing following file')
        oscmd = "scp %s nirav.joshi@108.168.207.6:/home/nirav.joshi" %srcpath
        os.system(oscmd)
        logger.info('Scping is completed for file %s',srcpath)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
# Create Observer to watch directories
observer = Observer()
# Empty list of observers .
observers = []

for path in tools_logslocation:
    if path.find('/') != -1:
        logger.info('Got path  %s', path)
        targetpath = str(path).rstrip()
        print targetpath
        # Schedules watching of a given path
        observer.schedule(MyHandler(), targetpath)
        # Add observable to list of observers
        observers.append(observer)

        # start observer
observer.start()




if __name__ == '__main__':
    print tools_logslocation
    for o in observers:
        # Wait until the thread terminates before exit
        o.join()
    #print toolslogslocation