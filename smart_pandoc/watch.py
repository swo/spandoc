import watchdog.events, os.path, sys

class SpandocHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, fn, callback):
        '''
        fn : str
          file the to be watched (probably the output file)
        callback : function (no arguments)
          function that will cause the update
        '''
        self.fn = os.path.abspath(fn)
        self.callback = callback

    def on_any_event(self, event):
        if os.path.abspath(event.src_path) == self.fn:
            if event.event_type == 'modified':
                self.callback.__call__()
                subprocess.run(self.command)
            elif event.event_type == 'deleted':
                print('watched file was deleted; quitting')
                sys.exit(0)
