import os
import getpass


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
	getpass.getpass(prompt='')
