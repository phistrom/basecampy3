"""
This should be an example in the README.md and it should be runnable. If it's not, then that's pretty embarrassing.
"""

from basecampy3 import Basecamp3
import json

bc3 = Basecamp3()

# replace these with actual IDs of the Basecamp objects you wish to get
recording_id = 123456789
project_id = 1234567

# Reference:
# https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments

url = bc3.urls.comments.list_by_recording(project=project_id, recording=recording_id)
response = url.request(bc3.session)
if not response.ok:
    print("Something went wrong. %s: %s" % (response.status_code, response.text))
    exit(1)

data = response.json()
pretty_print = json.dumps(data, indent=4)
print(pretty_print)
