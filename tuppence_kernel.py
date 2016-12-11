from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel
from pexpect.replwrap import REPLWrapper
from pexpect.exceptions import EOF

class TuppenceKernel(Kernel):
    implementation = 'Tuppence'
    implementation_version = '1.0'
    language = 'tuppence'
    language_version = '0.1'
    language_info = {'mimetype': 'text/plain', 'name':'tuppence'}
    banner = "Tuppence kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_tuppence()

    def _start_tuppence(self):
        self.replwrapper = REPLWrapper("tuppence", ">>> ", None)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            if not silent:
                output = self.replwrapper.run_command(code)
                stream_content = {'name': 'stdout', 'text': output}
                self.send_response(self.iopub_socket, 'stream', stream_content)

            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   }
        except EOF:
            if not silent:
                output = 'killed'
                stream_content = {'name': 'stdout', 'text': output}
                self.send_response(self.iopub_socket, 'stream', stream_content)

            return {'status': 'ok',
                    # The base class increments the execution count
                    'execution_count': self.execution_count,
                    'payload': [],
                    'user_expressions': {},
                   }

    def do_shutdown(self, restart):
        try:
            self.replwrapper.run_command('exit()')
        except EOF:
            pass

if __name__ == '__main__':
    IPKernelApp.launch_instance(kernel_class=TuppenceKernel)
