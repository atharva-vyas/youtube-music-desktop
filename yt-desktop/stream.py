import os
import time
import eel
from pygame import mixer 
from mutagen.mp3 import MP3
import threading

os.system('cls')
print('')
print('example:- https://www.youtube.com/playlist?list=XYZ123ABC')
link = str(input('ENTER A YOUTUBE PLAYLIST/VIDEO LINK:- '))
print('')

with open('config.txt') as f:
	Store_Temp_Streaming_Data = f.readline()
	Default_Local_Music_Dir = f.readline()
	dir = Store_Temp_Streaming_Data[27:][:-1]

eel.init("web")		# initialises eel

arr = []	#array keeps track of all songs
i = 0		
o = 0		#counter for songs
status = 1	#for play/pause status
vol = 1.0	#controls volume (1.0 = maximum volume)

def yt_dl():
    try:
        os.makedirs(dir)

    except FileExistsError:
        pass

    os.chdir(dir)
    os.system('youtube-dl --no-check-certificate --no-overwrites --ignore-errors --no-continue --rm-cache-dir --no-part -q --metadata-from-title "%(artist)s - %(title)s" --audio-quality 0 -x --audio-format mp3 ' + link)

# adds all songs to array
def updater():
	global i
	global o
	try:
		if i != len(os.listdir(dir)) - 3:
			if os.listdir(dir)[i][-4:] == '.mp3':
				if os.listdir(dir)[i] not in arr:
					arr.append(os.listdir(dir)[i])
		i += 1
	except:
		i = 0

@eel.expose	
def play():
	# plays music
	global status
	status = 1
	mixer.music.unpause()
	updater()
	return 'play'

@eel.expose	
# pauses music
def pause():
	global status
	status = 0
	mixer.music.pause()
	updater()
	return 'pause'

@eel.expose	
# increases volume
def vol_up():
	global vol
	vol += 0.1
	if vol > 1.0:
		vol = 1.0
	mixer.music.set_volume(vol)
	return str('volume: ' + str(round(vol * 100)))

@eel.expose
# decreases volume
def vol_down():
	global vol
	vol -= 0.1
	if vol < 0.1:
		vol = 0
	mixer.music.set_volume(vol)
	return str('volume: ' + str(round(vol * 100)))

@eel.expose	
def next():
	global arr
	global o
	global status
	# if music is not paused
	if status == 1:	
		if o + 1 != len(arr):
			# loads and plays next song
			try:
				o += 1
				mixer.music.load(dir + "\\" + arr[o])
			except:
				return
			mixer.music.play()
			updater()
			return [arr[o][:-16], 'next']
		# if all songs have been played, it starts playing from the begining
		else:
			o = 0
			mixer.music.load(dir + "\\" + arr[o])
			mixer.music.play()
			updater()
			return [arr[o][:-16], 'next']
	
	# if music is paused
	elif status == 0:
		if o + 1 != len(arr):
			# loads and plays next song
			try:
				o += 1
				mixer.music.load(dir + "\\" + arr[o])
			except:
				o += 1
				mixer.music.load(dir + "\\" + arr[o])
				return
			mixer.music.play()
			mixer.music.pause()
			updater()
			return [arr[o][:-16], 'next']
		# if all songs have been played, it starts playing from the begining
		else:
			o = 0
			mixer.music.load(dir + "\\" + arr[o])
			mixer.music.play()
			updater()
			return [arr[o][:-16], 'next']

@eel.expose	
def previous():
	global arr
	global o
	global status
	# if music is not paused
	if status == 1:
		# loads and plays previous song
		try:
			o -= 1
			mixer.music.load(dir + "\\" + arr[o])
		except:
			return
		mixer.music.play()
		updater()
		return [arr[o][:-16], 'previous']
	# if music is paused
	elif status == 0:
		# loads and plays previous song
		try:
			o -= 1
			mixer.music.load(dir + "\\" + arr[o])
		except:
			return
		mixer.music.play()
		mixer.music.pause()
		updater()
		return [arr[o][:-16], 'previous']

@eel.expose
def main():
	global arr
	global o
	global status

	# updates the HTML header with the current playing song
	eel.name_update(arr[o][:-16])

	# gets song length
	def length():
		length = MP3(dir + "\\" + arr[o]).info.length
		return int(length)
	
	# updates song slider bar
	while mixer.music.get_busy() != 0:
		updater()
		os.system('cls')
		print('songs loaded: ', len(arr))
		print('now playing: ', '#' + str(o + 1) , arr[o][:-16])
		eel.time(int((((mixer.music.get_pos()) / 1000) / length()) * 100000000))
		while status == 0:
			updater()
			os.system('cls')
			print('songs loaded: ', len(arr))
			print('now playing: ', '#' + str(o + 1) , arr[o][:-16])
			eel.time(int((((mixer.music.get_pos()) / 1000) / length()) * 100000000))
	
	# plays next song if song has finished
	if mixer.music.get_busy() == 0:
		o += 1
		if o != len(arr):
			mixer.music.load(dir + "\\" + arr[o])
			mixer.music.play()
			main()
		else:
			o = 0
			mixer.music.load(dir + "\\" + arr[o])
			mixer.music.play()
			main()


# Starts the index.html file
def start0():
	eel.start("index.html", size=(551, 390), position=(0,0))

def init():
	mixer.init()
	os.system('cls')
	print('loading, please be patient...')

	# clears old data
	dir_counter = 0
	while len(os.listdir(dir)) != 3:
		try:
			if os.listdir(dir)[dir_counter][-3:] != 'exe':
				os.remove(dir + r'//' + os.listdir(dir)[dir_counter])
			dir_counter += 1
		except:
			dir_counter = 0

	while len(arr) == 0:
		updater()

	# loads initial song
	def loader():
		time.sleep(1)
		try:
			mixer.music.load(dir + '\\' + arr[o])
		except:
			loader()
	loader()

	os.system('cls')
	mixer.music.play()

if __name__ == '__main__':
	threading.Thread(target = yt_dl).start()
	init()
	threading.Thread(target = main).start()
	start0()