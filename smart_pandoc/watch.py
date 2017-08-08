import watchdog.events, os.path, subprocess, sys

class SpandocHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, fn, command):
        '''
        fn : str
          file the to be watched (probably the output file)
        command : list of strings
          pandoc command to be run with subprocess
        '''
        self.fn = os.path.abspath(fn)
        self.command = command

    def on_any_event(self, event):
        if os.path.abspath(event.src_path) == self.fn:
            if event.event_type == 'modified':
                subprocess.run(self.command)
            elif event.event_type == 'deleted':
                print('watched file was deleted; quitting')
                sys.exit(0)
