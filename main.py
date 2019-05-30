from sys import argv

from kharabot import Kharabot


def main():
    if not len(argv) == 2:
        print('Usage: python37 main.py $token')
        return

    bot = Kharabot(argv[1])
    bot.run()


if __name__ == "__main__":
    main()
