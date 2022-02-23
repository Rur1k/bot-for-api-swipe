from models import UserToken


def create_new_user(user_id, chat_id):
    users = UserToken.select().where((UserToken.user == user_id) & (UserToken.chat == chat_id))
    if not users.first():
        UserToken.create(user=user_id, chat=chat_id)


def set_token_user(user_id, token):
    user = UserToken.select().where(UserToken.user == user_id)
    if user.first():
        UserToken.update(token=token).where(UserToken.user == user_id).execute()


def get_token_user(user_id):
    users = UserToken.select().where(UserToken.user == user_id)
    user = users.first()
    if user:
        return user.token
