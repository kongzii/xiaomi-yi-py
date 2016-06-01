#!/usr/bin/python3
import json
import socket
from time import sleep, perf_counter

REST = 3

class XiaomiYi:
    """
    # Make XiaomiYi object with default values.
    # You can override these like :
    # camera = XiaomiYi(ip="192.168.42.1", port=7878, timeout=5)
    camera = XiaomiYi()

    # Make connection to the camera.
    camera.connect()

    # Take single photo.
    camera.take_photo()

    # You can start recording.
    camera.start_video()
    sleep(5)

    # And stop it manually.
    camera.stop_video()

    # Or record for a desired time (in seconds).
    camera.start_video(10)

    # Take photo every 5 seconds, for 30 sec.
    # If second parameter is ommited, take photos forever.
    camera.seq_photos(5, 30)

    # Enable streaming for X seconds, or forever if ommited.
    # Connect to stream on http://192.168.42.1/live with VLC or something.
    # camera.stream(30)

    # Send custom commands.
    # You can find list of some common in commands.txt
    cmd = { "msg_id": 2,
            "token": camera.token(),
            "type": "video_quality", 
            "param": "S.Fine" 
        }
    camera.send(cmd)

    # Close connection.
    camera.close()
    """

    def __init__(self, ip="192.168.42.1", port=7878, timeout=5):
        self._ip = ip
        self._port = port
        self._timeout = timeout

        self.__token = None
        self.__timeout = timeout
        self.__control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    def send(self, data, connect=False):
        """
        There needs to be little delay after every command,
        except while getting token, 
        otherwise Yi will ignore following commands.
        """
        if self.__token or connect:
            self.__control.send(bytes(json.dumps(data), 'UTF-8'))
            if not connect: sleep(REST)
        else:
            raise LookupError("Make connection with object.connect() first.")

    def token(self):
        # print("Your token is: ", __token)
        return self.__token

    def connect(self):
        self.__control.settimeout(self.__timeout)
        self.__control.connect((self._ip, self._port))

        self.send({"msg_id": 257, "token": 0}, True)
        data = self.__control.recv(512).decode("utf-8")
        if not "rval" in data:
            data = self.__control.recv(512).decode("utf-8")
        self.__token = json.loads(data)["param"]

    def take_photo(self):
        self.send({"msg_id": 769, "token": self.__token})

    def start_video(self, duration=False):
        self.send({"msg_id": 513, "token": self.__token})
        if duration:
            sleep(duration)
            self.send({"msg_id": 514, "token": self.__token})

    def stop_video(self):
        self.send({"msg_id": 514, "token": self.__token})

    def seq_photos(self, every, until=False):
        if every < REST: every = REST

        begin = perf_counter()
        while True:
            self.take_photo()
            if until and (until < perf_counter() - begin):
                break
            sleep(every - REST)

    def stream(self, until=False):
        begin = perf_counter()

        self.send({"msg_id": 259, "token": self.__token, "param": "none_force"})
        while True:
            sleep(1)
            if until and (until < perf_counter() - begin):
                break

        return json(self.__control.recv(512).decode("utf-8"))

    def close(self):
        self.__control.close()
