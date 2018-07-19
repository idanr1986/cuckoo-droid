from subprocess import Popen
"""
Enables Popen to be used "with"
https://stackoverflow.com/questions/30421003/exception-handling-when-using-pythons-subprocess-popen
"""

class MyPopen(Popen):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()
        if self.stdin:
            self.stdin.close()
        # Wait for the process to terminate, to avoid zombies.
        self.wait()