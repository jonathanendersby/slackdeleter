import requests
from datetime import datetime, timedelta
import time


# Your Settings Here
WEEKS = 2  # How many weeks old must a file be to be considered.
MB = 4  # How big must a file be in order to be considered.
TOKEN = "YOUR-SLACK-TOKEN-HERE"  # Look at https://api.slack.com/web#authentication
REALLY_DELETE = False  # Set to True to actually delete files, otherwise it's a dry run.


# You shouldn't need to change anything below here.
threshold = datetime.now() - timedelta(weeks=WEEKS)

unixtime = time.mktime(threshold.timetuple())
params = {'token': TOKEN, 'ts_to': unixtime, 'page': 1}

print "\nCriteria: Looking for files %s weeks old and larger than %s MB." % (WEEKS, MB)

if not REALLY_DELETE:
    print "\n########################################  DRY RUN  ########################################"
    print "  Nothing is really being deleted. Set REALLY_DELETE = True to delete files for realsies."
    print "###########################################################################################"

print "\nFetching Files with %s" % params

result = requests.get('https://slack.com/api/files.list', params=params)
json = result.json()
pages = json['paging']['pages']
files = json['files']

for i in range(2, pages+1):
    params['page'] = i
    print "Fetching Files with %s" % params
    result = requests.get('https://slack.com/api/files.list', params=params)
    json = result.json()
    files += json['files']

print "\n%s files match your age criteria.\n" % len(files)

params = {'token': TOKEN}

total_bytes_deleted = 0

for f in files:
    if f['size'] > MB * 1000000:
        print "%s: %s MB" % (f['name'], f['size']/1000000),

        if REALLY_DELETE:
            params['file'] = f['id']
            a = requests.get('https://slack.com/api/files.delete', params=params)
            if a.status_code == 200:
                print " - Deleted"
                total_bytes_deleted += f['size']
            else:
                print " - ERROR: %s " % a.status_code
                print a.json()
                print ""
        else:
            print " - Matched Age and Size Criteria."

print "\nDeleted %s MB." % (total_bytes_deleted / 1000000)
