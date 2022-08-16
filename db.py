from peewee import SqliteDatabase, Model, CharField, IntegerField, InternalError
from uuid import uuid4
################################# MODELS ##################################

db = SqliteDatabase('key.db')

class Key(Model):
    name = CharField()
    key = CharField(unique=True)

    class Meta:
        database = db



###########################################################################
def add_key():
    key_name = str(uuid4())
    key = Key.create(name="", key=key_name)
    key.save()
    return key_name

def chek_is_key_exist(username, key): # Добавить сюда юзернейм
    try:
        single_key = Key.select().where(Key.key == key).get()
        single_key.name = username
        single_key.save()
        return True
    except:
        return False
def get_key_by_username(username):
    try:
        key = Key.select().where(Key.name == username).get()
    except:
        return ""
    return key.key

def get_all_keys():
    keys_list = []
    query = Key.select()
    for key in query:
        keys_list.append(f"{key.name} - {key.key}")
    return keys_list

def delete_key(key):
    Key.get(Key.key == key).delete_instance()
if __name__ == '__main__':
    try:
        print(get_all_keys())
        # db.connect()
        # Key.create_table()
    except InternalError as px:
        print(str(px))