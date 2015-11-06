# SlackDeleter
Python script to delete Slack files that meet a specific age and size criteria.

# Usage
$ python delete.py

Edit the 4 config lines to configure how this script behaves. By default it runs in Dry Run mode.

```python
WEEKS = 30  # How many weeks old must a file be to be considered.
MB = 2  # How big must a file be in order to be considered.
TOKEN = "YOUR-SLACK-TOKEN-HERE"  # Look at https://api.slack.com/web#authentication
REALLY_DELETE = False  # Set to True to actually delete files, otherwise it's a dry run.
```

# Example Output
<pre>
$ python delete.py

Criteria: Looking for files 40 weeks old and larger than 1 MB.

Fetching Files with {'token': 'XXX', 'ts_to': 1422632963.0, 'page': 1}
Fetching Files with {'token': 'XXX', 'ts_to': 1422632963.0, 'page': 2}

122 files match your age criteria.

Pasted image at 2015_01_30 01_53 PM.png: 1 MB  - Deleted
The Branding.zip: 1 MB  - Deleted
Pasted image at 2014_11_21 11_27 AM.png: 1 MB  - Deleted
Image.jpg: 1 MB  - Deleted
Event Map - Final.pdf: 1 MB  - Deleted

Deleted 6 MB.
ox:slackdeleter jonathan$ 
</pre>

## Or with REALLY_DELETE = False

<pre>
$ python delete.py

Criteria: Looking for files 2 weeks old and larger than 4 MB.

########################################  DRY RUN  ########################################
  Nothing is really being deleted. Set REALLY_DELETE = True to delete files for realsies.
###########################################################################################

Fetching Files with {'token': 'xoxp-2524370452-3396924721-14035506230-26ec1ff1', 'ts_to': 1445615554.0, 'page': 1}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 2}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 3}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 4}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 5}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 6}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 7}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 8}
Fetching Files with {'token': 'XXX', 'ts_to': 1445615554.0, 'page': 9}

817 files match your age criteria.

thatdomain.com.har: 5 MB  - Matched Age and Size Criteria.
20150820_160215.jpg: 4 MB  - Matched Age and Size Criteria.

Deleted 0 MB.
</pre>
