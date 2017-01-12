import logging
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import LoggingEventHandler

logslocation ={'WKLogs':[
               '/Users/nirav/logs/saas-prodcm71-wk/saas-prodcm71-wk-app01',
               '/Users/nirav/logs/saas-prodcm71-wk/saas-prodcm71-wk-app02',
               '/Users/nirav/logs/saas-prodcm71-wk/saas-prodcm71-wk-app98',
               '/Users/nirav/logs/saas-prodcm71-wk/saas-prodcm71-wk-app99'],
                'CAPLogs':[
               '/Users/nirav/logs/saas-prodcm71-cap/saas-prodcm71-cap-app01',
               '/Users/nirav/logs/saas-prodcm71-cap/saas-prodcm71-cap-app02',
               '/Users/nirav/logs/saas-prodcm71-cap/saas-prodcm71-cap-app98',
               '/Users/nirav/logs/saas-prodcm71-cap/saas-prodcm71-cap-app99'],
                'INAILLogs':[
               '/Users/nirav/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app01',
               '/Users/nirav/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app02',
               '/Users/nirav/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app98',
               '/Users/nirav/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app99']
               }


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.BZ2", "*.bz2"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# Attach a logging event AKA FileSystemEventHandler
event_handler = LoggingEventHandler()
# Create Observer to watch directories
observer = Observer()
# Empty list of observers .
observers = []
# Base logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


for path in logslocation:
    print path ,'correspond to ', logslocation[path]
    for location in logslocation[path]:
        #print location
        # convert line into string and strip newline character
        targetpath = str(location).rstrip()
        print targetpath
        # Schedules watching of a given path
        observer.schedule(MyHandler(), targetpath)
        # Add observable to list of observers
        observers.append(observer)

# start observer
observer.start()

try:
    while True:
        # poll every second
        time.sleep(5)
except KeyboardInterrupt:
    for o in observers:
        o.unschedule_all()
        # stop observer if interrupted
        o.stop()
for o in observers:
    # Wait until the thread terminates before exit
    o.join()