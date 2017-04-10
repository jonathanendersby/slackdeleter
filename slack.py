import requests


def slack_call(token, url, params=None, section=None):

    # print params

    if params is None:
        params = {}

    params['token'] = token
    result = requests.get(url, params=params)

    if result.status_code == 200 and result.json()['ok']:
        if section:
            res = result.json()
            if section in res:
                return result.json()[section]
            else:
                raise Exception('Section not found in JSON response. Was looking for %s' % section)
        else:
            return result.json()

    else:
        raise Exception("ERROR: HTTP %s (%s)" % (result.status_code, result.json()['error']))


def where(in_list, key, value):
    for i in in_list:
        if key in i and i[key] == value:
            return i

    return None


def get_user(token):
    return slack_call(token, 'https://slack.com/api/auth.test')


def get_users(token):
    return slack_call(token, 'https://slack.com/api/users.list', section='members')
