from ..db.fetchers import UserFetcher


class Validate:
    @staticmethod
    def request(keys, json):
        if len(keys) != len(json):
            return 3008

        for item in json.items():
            if item[0] not in keys:
                return 3008
        return json

    @staticmethod
    def user_duplicate(user_dict):
        vu = False
        ve = False
        if 'username' in user_dict:
            vu = UserFetcher.fetch({'username': user_dict['username']})

        if 'email' in user_dict:
            ve = UserFetcher.fetch({'email': user_dict['email']})

        if vu and ve:
            return 3002

        elif vu:
            return 3003

        elif ve:
            return 3004

        else:
            return 2000
