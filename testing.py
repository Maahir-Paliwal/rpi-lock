from picamera2 import Picamera2

picam2 = Picamera2()

config = picam2.create_preview_configuration({"size": (808, 606)})
print(config["main"])
picam2.align_configuration(config)
print(config["main"])