"""
This should be an example in the README.md and it should be runnable. If it's not, then that's pretty embarrassing.
"""

from basecampy3 import Basecamp3
from pprint import pprint

bc3 = Basecamp3()
session = bc3._session
MY_COMPANY_ID = 1234567
recording_id = 123456789
project_id = 1234567

# Reference:
# https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments
BASE_URL = "https://3.basecampapi.com/{company_id}/".format(company_id=MY_COMPANY_ID)  # base of all API requests
ENDPOINT = "{base_url}/buckets/{project_id}/recordings/{recording_id}/comments.json"  # get comments endpoint
url = ENDPOINT.format(base_url=BASE_URL, project_id=project_id, recording_id=recording_id)
resp = session.get(url)  # make a GET request. Substitute get() with post() or put() or delete() as needed
if not resp.ok:  # API returned a 4XX or 5XX error
    print("Something went wrong.")
pprint(resp.json())  # resp.json() will make a nice dictionary of the JSON response from Basecamp
