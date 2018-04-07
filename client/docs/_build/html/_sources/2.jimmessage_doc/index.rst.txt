====================
Capture 'JIMMessage'
====================

Кратко
------
Класс **JIMMessage** отвечает за формирование сообщений Клиента согласно протоколу *JIM*

Методы класса JIMMessage:
-------------------------
 * Статические:

  #. presence
  #. probe_answer
  #. authenticate
  #. msg
  #. get_contacts
  #. add_contact
  #. del_contact
  #. join
  #. left
  #. quit

 * Свойства:

  #. show
  #. dump_to_json

Presence & probe_answer
:::::::::::::::::::::::

Методы *presence*, *probe_answer* возвращают объект класса **JIMMessage** с полями:

 * action
 * status
 * time
 * sender

Authenticate
::::::::::::

Метод *authenticate* возвращает объект класса **JIMMessage** с полями:

 * action
 * time
 * account_name
 * password
 * username

Msg
:::

Метод *msg* возвращает объект класса **JIMMessage** с полями:

 * action
 * time
 * sender
 * target
 * message
 * encoding

Show
::::

Свойство *show* представляет объект класса **JIMMessage** в виде словаря *dict* с соответствующими полями.

Dump_to_json
::::::::::::

Свойство *dump_to_json* формирует объект *json* в байтовом представлении из объекта класаа **JIMMessage**.

