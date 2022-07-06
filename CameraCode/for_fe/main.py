import sys
import os
from os import path

import gather
import post_processing

def check_folder_exists(dir_path, folder_str):
	return os.path.isdir(os.path.join(dir_path, folder_str))

def gather_session_movies(current_session_dir):
	video_folder = 'input_movies'
	video_folder_path = os.path.join(current_session_dir, video_folder)
	os.makedirs(video_folder_path)
	gather.gather_session_movies(video_folder_path, still_images_folder)

def post_process_movie(session_path):
	## 1. convert videos to frames
	videos_to_frames_path = os.path.join(session_path, 'videos_to_images')
	os.makedirs(videos_to_frames_path)
	post_processing.videos_to_frames(video_folder_path, videos_to_frames_path)

	## 2. extract foregrounds from frames
	extract_foreground_output_path = os.path.join(session_path, 'extract_foreground_output')
	os.makedirs(extract_foreground_output_path)
	post_processing.extract_foreground_from_frames(videos_to_frames_path, extract_foreground_output_path)

if __name__=='__main__':

	dir_path = os.path.dirname(os.path.realpath('main.py'))

	while True:

		# For first time users it goes straight to taking the videos
		if not check_folder_exists(dir_path, "session_1"):
			print("Welcome new user, let's start taking photos")
			current_session_dir = os.path.join(dir_path, "session_1")
			os.makedirs(current_session_dir)
			gather_session_movies(current_session_dir)

		else:

			input_val = input("*****Main menu******\n\nWould you like to \n(1) take more movies\n(2) move to post processing? \n(3) exit\n(Please enter 1, 2 or 3)\n\n")
			
			# Input val == '1' means take more movies 
			if input_val == '1':
				print("\nTaking more movies...\n")

				existing_session_folders = [x for x in os.listdir() if x.startswith("session_")]

				# existing_session_folders = []
				# for x in os.listdir():
				# 	if x.startswith("session_"):
				# 		existing_session_folders.append(x)

				max_existing_session = max([int(x.strip("session_")) for x in existing_session_folders])

				# session_numbers = []
				# for x in existing_session_folders:
				# 	session_numbers.append(int(x.strip("session_")))
				# max_existing_session = max(session_numbers)

				current_session_dir = os.path.join(dir_path, "session_{}".format(max_existing_session + 1))
				os.makedirs(current_session_dir)
				
				gather_session_movies(current_session_dir)
				print("Finished taking videos\n")

			# Input val == '2' means move to post processing
			elif input_val == '2':
				print("\nMoving to post_processing...\n")

				session_dirs = [x for x in os.listdir() if x.startswith("session_")]
				session_dir_paths = [os.path.join(dir_path, x) for x in session_dirs]

				for session_path in session_dir_paths:
					if (check_folder_exists(session_path, "input_movies")):
						if (len(os.listdir(os.path.join(session_path, "input_movies"))) > 0) and (not check_folder_exists(session_path, "movies_to_frames")):
							post_process_movie(session_path)

			# Input val == '3' for exiting
			elif input_val == '3':
				print("Exiting...")
				break

			else:
				print("\nDidn't recognise that input, please try again\n")

