import watchdog.events, watchdog.observers, os.path, sys, subprocess, time

class SpandocHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, fn, callback, verbose=False):
        '''
        fn : str
          file the to be watched (probably the output file)
        callback : function (no arguments)
          function that will cause the update
        verbose : bool
          print when pandoc is run
        '''
        self.fn = os.path.abspath(fn)
        self.callback = callback
        self.verbose = verbose

    def on_any_event(self, event):
        if os.path.abspath(event.src_path) == self.fn:
            if self.verbose:
                print(event)

            if event.event_type in ['created', 'modified']:
                if self.verbose:
                    print('running pandoc')

                self.callback.__call__()

def watch(watch_fn, callback, verbose=False):
    watch_fn = os.path.abspath(watch_fn)
    watch_dir = os.path.dirname(watch_fn)
    handler = SpandocHandler(watch_fn, callback, verbose)
    observer = watchdog.observers.Observer()
    observer.schedule(handler, watch_dir)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print('caught keyboard interrupt; quitting')

    observer.join()
