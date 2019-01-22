import os
import sys
import settings


def cls():
	os.system('cls' if os.name == 'nt' else 'clear')


def main():
	cfg = settings.Settings


if __name__ == "__main__":
	main()
