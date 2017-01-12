import time,sys,os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


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

for path in logslocation:
    print path



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
        os.system("scp wipro-dev-nestle_wipro-dev-nestle_20161216-144742_dump.tar.bz2 nirav.joshi@108.168.207.6:/home/nirav.joshi")

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()