from settings.models import UserToken


def create_new_user(user_id, chat_id):
    users = UserToken.select().where((UserToken.user == user_id) & (UserToken.chat == chat_id))
    if not users.first():
        UserToken.create(user=user_id, chat=chat_id)


def set_token_user(user_id, token, is_delete=False):
    user = UserToken.select().where(UserToken.user == user_id)
    if user.first() and not is_delete:
        UserToken.update(token=token, is_login=True).where(UserToken.user == user_id).execute()
    elif user.first() and is_delete:
        UserToken.update(token=token, is_login=False).where(UserToken.user == user_id).execute()


def get_token_user(user_id):
    users = UserToken.select().where(UserToken.user == user_id)
    user = users.first()
    if user:
        if user.token is not None and user.is_login:
            return user.token




def is_auth(user_id):
    users = UserToken.select().where(UserToken.user == user_id)
    user = users.first()
    if user:
        if user.is_login:
            return True
        else:
            return False
