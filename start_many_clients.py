"""Утилита запуска нескольких клиентов
    не более 20 клиентов за один раз"""

from subprocess import Popen, CREATE_NEW_CONSOLE


def run_clients():
    p_list = []  # Список клиентских процессов

    for client in range(3):
        # writer_name = 'Writer_' + str(w_c + 1)
        # password = '123'
        p_list.append(Popen('python client_start.py',
                            creationflags=CREATE_NEW_CONSOLE))


if __name__ == '__main__':
    run_clients()
