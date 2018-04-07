import os

LOGGER_NAME = 'client_log'
FILE_NAME = LOGGER_NAME + '.log'
FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)

if __name__ == '__main__':
    print(FILE_PATH)