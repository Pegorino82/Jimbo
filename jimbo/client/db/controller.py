from .storage import add_contact, del_contact, add_message
from .storage import Contact

def controller_msg(response, user):
    try:
        result = add_message(user, response)
        print(result)
        print('msg added {} {}'.format(user, response['message']))
    except Exception as err:
        print('error msg', err)

def controller_add_contact(response, user):
    if response['response'] == 404:
        print('contact not found')
    else:
        try:
            contact_name = response['contact']
            print('mongo_db controller contact', contact_name)
            contact = Contact(contact_name).con_dict
            result = add_contact(contact)
            if result == 'almost in contacts':
                print(contact_name, result)
            else:
                print('contact {} added'.format(contact_name))
        except Exception as err:
            print('error add', err)

def controller_del_contact(response, user):
    if response['response'] == 404:
        print('contact not found')
    else:
        try:
            contact_name = response['contact']
            print('mongo_db controller contact', contact_name)
            contact = Contact(contact_name).con_dict
            result = del_contact(contact)
            if 'not found' in result:
                print(result)
            else:
                print('contact {} deleted'.format(contact_name))
        except Exception as err:
            print('error del', err)