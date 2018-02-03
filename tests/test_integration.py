import multiprocessing
import os
import signal
import socket
from queue import Empty
from time import sleep

import requests
from honcho.process import Process


def test_create_file(tmpdir):
    old_wd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        os.system('python -m django_zero init --no-input project foo')

        os.chdir(str(tmpdir.join('foo')))
        os.system('make install')
        os.system('python -m django_zero webpack')

        events = multiprocessing.Queue()
        server = Process('python -m django_zero manage runserver', name='server')
        server_process = multiprocessing.Process(name='server', target=server.run, args=(events, True))

        target = '127.0.0.1', 8000

        try:
            server_process.start()
            exit = False
            pid = None

            while 1:
                try:
                    msg = events.get(timeout=0.1)
                except Empty:
                    if exit:
                        break
                else:
                    # print(msg)
                    if msg.type == 'start':
                        pid = msg.data['pid']

                        conn_ok = False
                        for i in range(10):
                            try:
                                s = socket.create_connection(target, 1)
                                s.close()
                                conn_ok = True
                            except socket.error:
                                sleep(1)
                        assert conn_ok

                        try:
                            target = 'http://{}:{}'.format(*target)
                            resp = requests.get(target + '/')
                            assert resp.status_code == 200

                            resp = requests.get(target + '/static/bootstrap.css')
                            assert resp.status_code == 200

                            resp = requests.get(target + '/static/bootstrap.js')
                            assert resp.status_code == 200
                        finally:
                            os.killpg(pid, signal.SIGKILL)
                    elif msg.type == 'stop':
                        pid = None
                        exit = True
        finally:
            server_process.terminate()
            server_process.join(timeout=2)
            if server_process.is_alive() and pid:
                try:
                    os.killpg(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    finally:
        os.chdir(old_wd)
