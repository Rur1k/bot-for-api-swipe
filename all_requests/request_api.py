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
    data = r.json()
    if not data:
        return True
    else:
        return False


# API
# account

def account_detail(token=None):
    r = requests.get(API + 'account/profile/', headers={'Authorization': f'token {token}'})
    data = r.json()
    return data


def account_update(token=None):
    data = {}
    r = requests.patch(API + 'account/profile/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


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
    data = {}
    r = requests.get(API + 'house/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


def house_create(token):
    data = {}
    r = requests.post(API + 'house/', data, headers={'Authorization': f'token {token}'})
    data = r.json()


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
