import requests
from settings.config import AUTH, API


# AUTH
def registration(username, email, password, phone=None):
    data = {
        'username': username,
        'email': email,
        'password': password,
        'phone': phone,
    }
    r = requests.post(AUTH + 'users/', data)
    data = r.json()

    if 'id' in data:
        return True
    else:
        return False


def login(email, password):
    data = {
        'email': email,
        'password': password
    }

    r = requests.post(AUTH + 'token/login', data)

    data = r.json()

    if 'non_field_errors' in data:
        code = 'ERROR'
        value = 'Логин или пароль указаны не корректно'
        return code, value
    else:
        code = 'SUCCESS'
        value = data['auth_token']
        return code, value


def logout(token):
    r = requests.post(AUTH + 'token/logout', headers={'Authorization': f'token {token}'})
    return True


# API
# account

def account_detail(token=None):
    r = requests.get(API + 'account/profile/', headers={'Authorization': f'token {token}'})
    data = r.json()
    return data


def account_update(token=None, phone=None, first_name=None, last_name=None):
    if phone is not None:
        data = {'phone': phone}
    elif first_name is not None:
        data = {'first_name': first_name}
    elif last_name is not None:
        data = {'last_name': last_name}
    else:
        data = {}

    r = requests.patch(API + 'account/profile/', data, headers={'Authorization': f'token {token}'})
    data = r.json()
    if 'pk' in data:
        return True
    else:
        return False


# announcement
def announcement_list(token):
    data = {}
    r = requests.get(API + 'announcement/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_create(token):
    data = {}
    r = requests.post(API + 'announcement/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_detail(token, anno_id):
    data = {}
    r = requests.get(API + f'announcement/{anno_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_update(token, anno_id):
    data = {}
    r = requests.patch(API + f'announcement/{anno_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_delete(token, anno_id):
    data = {}
    r = requests.delete(API + f'announcement/{anno_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_filter(token):
    data = {}
    r = requests.get(API + 'announcement/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_my_list(token):
    data = {}
    r = requests.get(API + 'announcement/my/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def announcement_my_detail(token, anno_id):
    data = {}
    r = requests.get(API + f'announcement/my/{anno_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


# favorite

def favorite_list(token):
    data = {}
    r = requests.get(API + 'favorite/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def favorite_create(token):
    data = {}
    r = requests.post(API + 'favorite/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def favorite_delete(token, favorite_id):
    data = {}
    r = requests.delete(API + f'favorite/{favorite_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


# flat

def flat_list(token):
    data = {}
    r = requests.get(API + 'flat/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def flat_create(token):
    data = {}
    r = requests.post(API + 'flat/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def flat_delete(token, flat_id):
    data = {}
    r = requests.delete(API + f'flat/{flat_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def flat_detail(token, flat_id):
    data = {}
    r = requests.get(API + f'flat/{flat_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def flat_update(token, flat_id):
    data = {}
    r = requests.patch(API + f'flat/{flat_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def flat_reserved(token, flat_id):
    data = {}
    r = requests.patch(API + f'flat/{flat_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


# house

def house_list(token):
    r = requests.get(API + 'house/', headers={'Authorization': f'token {token}'})
    data = r.json()
    return data


def house_create(token, info):
    data = {
        'name': info[0],
        'district': info[1],
        'microdistrict': info[2],
        'street': info[3],
        'number': info[4],
        'description': info[5],
        'lcd_status': info[6],
        'type_house': info[7],
        'class_house': info[8],
        'technologies': info[9],
        'to_sea': info[10],
        'payments': info[11],
        'ceiling_height': info[12],
        'gas': info[13],
        'heating': info[14],
        'sewerage': info[15],
        'sales_dep_fullname': info[16],
        'sales_dep_phone': info[17],
        'sales_dep_email': info[18],
        'registration': info[19],
        'calculation_options': info[20],
        'appointment': info[21],
        'sum_in_contract': info[22],
        'state': info[23],
        'territory': info[24],
        'maps': info[25],
        'house_buildings': info[26],
        'sections': info[27],
        'floors': info[28],
        'risers': info[29],
    }
    r = requests.post(API + 'house/', data, headers={'Authorization': f'token {token}'})
    data = r.json()
    print(data)
    if 'id' in data:
        return True
    else:
        return False


def house_detail(token, house_id):
    data = {}
    r = requests.get(API + f'house/{house_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def house_update(token, house_id):
    data = {}
    r = requests.patch(API + f'house/{house_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def house_delete(token, house_id):
    data = {}
    r = requests.delete(API + f'house/{house_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


# notary


def notary_list(token):
    data = {}
    r = requests.get(API + 'notary/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def notary_create(token):
    data = {}
    r = requests.post(API + 'notary/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def notary_detail(token, notary_id):
    data = {}
    r = requests.get(API + f'notary/{notary_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def notary_update(token, notary_id):
    data = {}
    r = requests.patch(API + f'notary/{notary_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def notary_delete(token, notary_id):
    data = {}
    r = requests.delete(API + f'notary/{notary_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()

# users


def user_list(token):
    data = {}
    r = requests.get(API + 'users/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def user_blacklist(token):
    data = {}
    r = requests.get(API + 'users/blacklist/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def user_blacklist_update(token, user_id):
    data = {}
    r = requests.patch(API + f'users/blacklist/{user_id}', data, headers={'Authorization': f'token {token}'})
    data = r.json()
