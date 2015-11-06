# SlackDeleter
Python script to delete Slack files that meet a specific age and size criteria.

# Usage
$ python delete.py

Edit the 4 config lines to configure how this script behaves. By default it runs in Dry Run mode.

# Example Output
<pre>
$ python delete.py

Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 1}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 2}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 3}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 4}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 5}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 6}
Fetching Files with {'token': 'XXX', 'ts_to': 1437145065.0, 'page': 7}

604 files match your criteria.

hm1.png: 3 MB  - Deleted
Hsjfs (3).pdf: 3 MB  - Deleted
Hejoijf (1).pdf: 3 MB  - Deleted
SanFsdf.zip: 3 MB  - Deleted
iosdfws.png: 3 MB  - Deleted
iagfus.png: 3 MB  - Deleted
Archive.zip: 3 MB  - Deleted
big.jpg: 3 MB  - Deleted
bigger.jpg: 3 MB  - Deleted
20150502_160647.jpg: 3 MB  - Deleted
Screen Shot 2015-04-30 at 2.43.29 PM.png: 3 MB  - Deleted
thatfile.tgz: 3 MB  - Deleted
20150325_181801.jpg: 3 MB  - Deleted
Screen Shot 2014-09-18 at 9.32.01 AM.png: 3 MB  - Deleted

Deleted 47 MB of Stuff
</pre>
