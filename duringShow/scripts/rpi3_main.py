# this file just needs to wait for an osc message and then use it as a trigger to refresh the rsync folder

from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
import os
import sys

# from waveshare_epd import epd5in83_V2

import rsync
import image_functions
import reload_screen

global msg
global loop_number
global prepared 
global prepared_diff
global layer

stored_exception=None


rpi4_ip_home = "192.168.0.80"
rpi4_ip_Fefes_Wifi = "192.168.8.126"
rpi4_ip = rpi4_ip_Fefes_Wifi
rpi3_ip_home = "192.168.0.119"
rpi3_ip_Fefes_Wifi = "192.168.8.237"
rpi3_ip = rpi3_ip_Fefes_Wifi
port_IN = 8002
path_IN = "/update_ur_screen"

loop_number = 0
msg=0
prepared_diff=0
layer=1

# def main(path: str, *osc_arguments):
#     msg = osc_arguments[-1]
#     print("input message: {}".format(msg))
#     # rsync_reload(msg, rpi4_ip)
#     # reload_screen(msg, dir_path)
#     return

def handlerfunction(address, s):
	global msg
	msg=int(s)
	print('receiving from rpi4'+str(msg))
    # Will receive message address, and message data flattened in s, x, y
	return



if __name__ == "__main__":
	global prepared
	prepared=1
	dir_path = os.path.dirname(os.path.realpath('main.py'))
	osc_startup()
	# Make server channels to receive packets.
	osc_udp_server(rpi3_ip, port_IN, "rpi3")
	print('osc_ud_server started up')
	# osc_method("/test/*", handlerfunction)
	osc_method("/update_ur_screen/", handlerfunction, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
	try:
		while True:
			osc_process()
			# input_address = [rpi4_ip, port_IN, path_IN]
			# listen_to_rpi4(input_address, dir_path)
			if msg>loop_number:
				print('msg is:'+str(msg))
				rsync.sync_the_folder(rpi4_ip)
				# image_functions.resize_the_file(msg, dir_path)
				reload_screen.reloading(dir_path, msg)
				# prepared=prepared+1
				loop_number=msg
				print('loop_number is: '+str(loop_number))
			if stored_exception:
				break
	except KeyboardInterrupt:
		print("[CTRL+C detected]")
		stored_exception=sys.exc_info()

# if stored_exception:
#     raise stored_exception[0], stored_exception[1], stored_exception[2]

osc_terminate()
sys.exit()

