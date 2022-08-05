from wotsong.api import api


@api.route('/users', methods=["POST"])
def create_user():
    print("create user")