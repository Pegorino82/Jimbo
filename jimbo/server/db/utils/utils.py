import time
import json

CODING = 'utf-8'


def convert(data):
    result = None
    if isinstance(data, bytes):
        try:
            result = json.loads(data.decode(CODING))
        except:
            print('wrong data format!')
        finally:
            return result
    elif isinstance(data, dict):
        try:
            result = json.dumps(data).encode(CODING)
        except:
            print('wrong data format!')
        finally:
            return result
    else:
        print('wrong data format!')
        return result


def act_time(time_):
    t_local = time.localtime(time_)
    t = time.strftime('%d.%m.%Y - %H:%M:%S', t_local)
    return t


if __name__ == '__main__':
    pass
