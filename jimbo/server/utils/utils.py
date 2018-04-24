import time
import json

from .common import CODING, TIME_TEMPLATE


def convert(data, coding=CODING):
    """
    converting byte_json to dict or dict to byte_json
    :param data:
    :return:
    """
    result = None
    if isinstance(data, bytes):
        try:
            result = json.loads(data.decode(coding))
        except Exception as err:
            print('wrong data format!', err)
        finally:
            return result
    elif isinstance(data, dict):
        try:
            result = json.dumps(data).encode(coding)
        except Exception as err:
            print('wrong data format!', err)
        finally:
            return result
    else:
        print('wrong data format!')
        return result


def act_time(time_, template=TIME_TEMPLATE):
    '''
    make readable time format by template from <UNIX>
    :param time_:
    :param template:
    :return:
    '''
    t_local = time.localtime(time_)
    t = time.strftime(template, t_local)
    return t


if __name__ == '__main__':
    pass
