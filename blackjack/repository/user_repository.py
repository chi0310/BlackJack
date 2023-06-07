class UserRepository():

    def check(self, *args):
        raise NotImplementedError

    @classmethod
    def make(cls, type: str, *args, **kwargs):
        if type == 'mem':
            return UserRepositoryMem(*args, **kwargs)
        else:
            raise NotImplementedError(f'{type} is not supported')


class UserRepositoryMem(UserRepository):

    def __init__(self) -> None:
        self.id2nickname = {'id_test': 'nickname_test'}
        self.id2password = {'id_test': 'password_test'}

    def check(self, id: str, password: str, nickname: str):
        ans = self.id2password.get(id, None)
        if password is None and ans != password:
            return False


class UserRepositoryDb(UserRepository):

    def __init__(self) -> None:
        self.users = {}

    def check(self, *args):
        return super().check(*args)
