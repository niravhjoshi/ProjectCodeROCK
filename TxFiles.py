import time,sys,os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

locallogslocation={'WKLogs':[
               '/Users/nirav//logs/saas-prodcm71-wk/saas-prodcm71-wk-app01',
               '/Users/nirav//logs/saas-prodcm71-wk/saas-prodcm71-wk-app02',
               '/Users/nirav//logs/saas-prodcm71-wk/saas-prodcm71-wk-app98',
               '/Users/nirav//logs/saas-prodcm71-wk/saas-prodcm71-wk-app99'],
                'CAPLogs':[
               '/Users/nirav//logs/saas-prodcm71-cap/saas-prodcm71-cap-app01',
               '/Users/nirav//logs/saas-prodcm71-cap/saas-prodcm71-cap-app02',
               '/Users/nirav//logs/saas-prodcm71-cap/saas-prodcm71-cap-app98',
               '/Users/nirav//logs/saas-prodcm71-cap/saas-prodcm71-cap-app99'],
                'INAILLogs':[
               '/Users/nirav//logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app01',
               '/Users/nirav//logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app02',
               '/Users/nirav//logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app98',
               '/Users/nirav//logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app99']
               }

toolslogslocation ={'WKLogs':[
               '/home/nirav.joshi/logs/saas-prodcm71-wk/saas-prodcm71-wk-app01',
               '/home/nirav.joshi/logs/saas-prodcm71-wk/saas-prodcm71-wk-app02',
               '/home/nirav.joshi/logs/saas-prodcm71-wk/saas-prodcm71-wk-app98',
               '/home/nirav.joshi/logs/saas-prodcm71-wk/saas-prodcm71-wk-app99'],
                'CAPLogs':[
               '/home/nirav.joshi/logs/saas-prodcm71-cap/saas-prodcm71-cap-app01',
               '/home/nirav.joshi/logs/saas-prodcm71-cap/saas-prodcm71-cap-app02',
               '/home/nirav.joshi/logs/saas-prodcm71-cap/saas-prodcm71-cap-app98',
               '/home/nirav.joshi/logs/saas-prodcm71-cap/saas-prodcm71-cap-app99'],
                'INAILLogs':[
               '/home/nirav.joshi/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app01',
               '/home/nirav.joshi/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app02',
               '/home/nirav.joshi/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app98',
               '/home/nirav.joshi/logs/saas-prodcm71-INAIL/saas-prodcm71-INAIL-app99']
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
        srcpath = event.src_path
        print "scp %s nirav.joshi@108.168.207.6:/home/nirav.joshi" %srcpath
        oscmd = "scp %s nirav.joshi@108.168.207.6:/home/nirav.joshi" %srcpath
        os.system(oscmd)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
# Create Observer to watch directories
observer = Observer()
# Empty list of observers .
observers = []

for path in locallogslocation:
    print path, 'correspond to ', locallogslocation[path]
    for location in locallogslocation[path]:
        # convert line into string and strip newline character
        targetpath = str(location).rstrip()
        print targetpath
        # Schedules watching of a given path
        observer.schedule(MyHandler(), targetpath)
        # Add observable to list of observers
        observers.append(observer)

        # start observer
observer.start()




if __name__ == '__main__':
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