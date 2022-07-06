import os
import time

def sync_the_folder(rpi4_ip_address):
	os.system('rsync -avz -ssh pi@'+str(rpi4_ip_address)+':marksMade/output/ output/' )
		# os.system('rsync -avz -ssh rpi3@192.168.8.237 :rsync_test/ rsync_test/')
		# os.system('Veggie36')
	time.sleep(5)
	os.system('exit')