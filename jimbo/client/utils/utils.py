import time
import json

CODING = 'utf-8'


def convert(data):
    """
    converting json_bytes to dict or dict to json_bytes
    :param data:
    :return:
    """
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
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-flag', help='w for write, r for read')
    parser.add_argument('-name', help='account_name')
    parser.add_argument('-pas', help='password')
    parser.add_argument('-action', help='auth, msg, add, get')

    args = parser.parse_args()


    # client_action(sys.argv)

    def too(flag, name, pas, act):
        print('flag {}\nname {}\npassword {}\naction {}\n'.format(flag, name, pas, act))


    too(args.flag, args.name, args.pas, args.action)
