import os

# loads default temp dir to clear it
with open('config.txt') as f:
	dir = f.readline()[27:][:-1]

# clears old data
dir_counter = 0
print(len(os.listdir(dir)))
while len(os.listdir(dir)) != 3:
    try:
        if os.listdir(dir)[dir_counter][-3:] != 'exe':
            os.remove(dir + '/' + os.listdir(dir)[dir_counter])
        dir_counter += 1
    except:
        dir_counter = 0

os.system('cls')
print('')
def main():
    input_main = input('(1) PLAY OFFLINE SONGS \n(2) STREAM YOUTUBE MUSIC \n \n=>')
    if input_main == '1':
        os.system('cls')
        os.system('python offline.py')
    elif input_main == '2':
        os.system('cls')
        os.system('python stream.py')
    else:
        os.system('cls')
        print('INVALID INPUT')
        main()

main()