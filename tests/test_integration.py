import gc
import multiprocessing
import os
import signal
import socket
from queue import Empty

import requests
from honcho.process import Process
from time import sleep


def get_free_port():
    """Get free port."""
    sock = socket.socket()
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    del sock
    gc.collect()
    return port


def test_create_file(tmpdir):
    old_wd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        os.system("python -m django_zero create --no-input project foo")

        os.chdir(str(tmpdir.join("foo")))

        # TODO: move back into make install
        os.system("python -m django_zero install")
        os.system("yarn install")

        os.system("python -m django_zero manage migrate")

        # Run the webpack assets builder
        os.system("python -m django_zero webpack")

        target = "127.0.0.1", get_free_port()
        print("Target:", *target)

        events = multiprocessing.Queue()
        server_command = "python -m django_zero manage runserver {0}:{1}".format(*target)
        print("Command:", server_command)
        server = Process(server_command, name="server")
        server_process = multiprocessing.Process(name="server", target=server.run, args=(events, True))

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
                    if msg.type == "start":
                        pid = msg.data["pid"]

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
                            target = "http://{}:{}".format(*target)
                            resp = requests.get(target + "/")
                            assert resp.status_code == 200

                            resp = requests.get(target + "/static/bootstrap.css")
                            assert resp.status_code == 200

                            resp = requests.get(target + "/static/bootstrap.js")
                            assert resp.status_code == 200
                        finally:
                            os.killpg(pid, signal.SIGKILL)
                    elif msg.type == "line":
                        print(">>>", msg.data.decode("utf-8"), end="")
                    elif msg.type == "stop":
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
