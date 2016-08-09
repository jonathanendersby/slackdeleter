import requests
from datetime import datetime, timedelta
import time
import click
import sys


def slack_call(token, url, params=None, section=None):
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


def fetch_files(token, days, only_created):
    threshold = datetime.now() - timedelta(days=days)
    unixtime = time.mktime(threshold.timetuple())
    params = {'token': token, 'ts_to': unixtime, 'page': 1}

    if only_created:
        user = get_user(token)
        # print "User ID: %s" % user['user_id']
        params['user'] = user['user_id']

    print '.',

    json = slack_call(token, 'https://slack.com/api/files.list', params=params)
    pages = json['paging']['pages']
    files = json['files']

    for i in range(2, pages+1):
        params['page'] = i
        # print "Fetching Files with %s" % params
        print '.',
        json = slack_call(token, 'https://slack.com/api/files.list', params=params)
        files += json['files']

    return files


def human_size(b):
    if b > 1000000:
        return "%0.2f MB" % (b / 1000000.0)

    if b > 1000:
        return "%0.2f KB" % (b / 1000.0)

    else:
        return "%s Bytes" % b


def delete_files(queue, token):
    params = {'token': token}
    bytes_deleted = 0
    files_deleted = 0
    for f in queue:
        print "  Deleting %s (%s) ... " % (f['name'], human_size(f['size'])),

        params['file'] = f['id']
        a = requests.get('https://slack.com/api/files.delete', params=params)
        if a.status_code == 200 and a.json()['ok']:
            bytes_deleted += f['size']
            files_deleted += 1
            print "Deleted"
        else:
            print " - ERROR: HTTP:%s (%s)" % (a.status_code, a.json()['error'])

    return files_deleted, bytes_deleted


# Age From Timestamp
def aft(timestamp):
    d = datetime.fromtimestamp(int(timestamp))

    td = datetime.now() - d

    if td.total_seconds() > 60 * 60 * 24:
        return "%0.0f days ago" % (td.total_seconds() / 86400)

    elif td.total_seconds() > 60 * 60:
        return "%0.0f hours ago" % (td.total_seconds() / 3600)

    else:
        return "%0.0f minutes ago" % (td.total_seconds() / 60)


def get_real_name(users, user_id):
    n = where(users, 'id', user_id)

    if 'profile' in n:  # Caters for deleted profiles.
        return n['profile']['real_name']

    else:
        return n['real_name']


@click.command()

@click.option('--token', prompt='Slack Test Token',
              help='Your Slack test token (https://api.slack.com/docs/oauth-test-tokens)',
              type=click.STRING)

@click.option('--days', default=31, prompt='Age of files to delete.',
              help='How old a file must be in order to delete it.')

@click.option('--only_created', default=True, prompt='Only delete files you created?',
              help="Only delete files you created?", type=click.BOOL)

@click.option('--sort', default='size', prompt='Sort by',
              help="Sort by 'size', 'date' or 'user'.", type=click.Choice(['size', 'date', 'user']))

@click.option('--min_kb', default='1000', prompt='Minimum filesize to delete (in kilobytes)',
              help="Minimum number of Kilobytes for file to qualify.", type=click.INT)

def query_slack(token, days, only_created, sort, min_kb):

    print "Querying Slack's Servers",

    users = get_users(token)

    files = fetch_files(token, days, only_created)

    if sort == 'size':
        files = sorted(files, key=lambda k: k['size'], reverse=True)

    elif sort == 'date':
        files = sorted(files, key=lambda k: k['created'])

    elif sort == 'user':
        files = sorted(files, key=lambda k: k['user'])

    min_bytes = min_kb * 1000

    delete_queue = []
    total_bytes = 0

    file_name_lengths = []

    for f in files:
        if f['size'] >= min_bytes:
            file_name_lengths.append(len(f['name']))
            total_bytes += f['size']
            delete_queue.append(f)

    if delete_queue:
        np = max(file_name_lengths)

        print "\nFiles:"

        for f in delete_queue:
            real_name = get_real_name(users, f['user'])

            print "  %s %s\t%s\t%s" % (f['name'].ljust(np + 4), human_size(f['size']).ljust(12),
                                         real_name.ljust(24),
                                         aft(f['created']))

        print "\n%s files match your criteria. (%s)\n" % (len(delete_queue), human_size(total_bytes))

        delete = click.confirm('Do you want to delete all of these files now?')

        if delete:
            really = click.prompt("Type \"YES\" to really delete the files listed above")
            if really != "YES":
                print "You didn't type \"YES\" so I'm quitting to be safe."
                return

            print "\nDELETING FILES:"
            files_deleted, bytes_deleted = delete_files(delete_queue, token)
            print '\n%s files deleted (%s)' % (files_deleted, human_size(bytes_deleted))

    else:
        print "\nNo files matched your criteria."

    print ""
if __name__ == '__main__':
    try:
        query_slack()
    except Exception as e:
        print "\nFATAL ERROR: %s\n" % e
        sys.exit(99)
