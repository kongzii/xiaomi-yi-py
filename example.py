#!/usr/bin/python3
from time import sleep

from xiaomi_yi import XiaomiYi

if __name__ == "__main__":
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
	cmd = {	"msg_id": 2,
			"token": camera.token(),
			"type": "video_quality", 
			"param": "S.Fine" 
		}
	camera.send(cmd)

	# Close connection.
	camera.close()