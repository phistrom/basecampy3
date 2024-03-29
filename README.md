# BasecamPY3

An easy-to-use Python interface to
the [Basecamp 3 API](https://github.com/basecamp/bc3-api).

*BasecamPY3 will drop Python 2.7 and 3.5 support in the 1.0.0 release.*

## Features

- Easy, AWS CLI-like configuration and installation
- Object-oriented API
- Handles rate-limiting, caching, and authentication for you!

## Install

```shell
pip install basecampy3
bc3 configure
```

Follow the prompts to obtain an access and refresh token which is then saved
to `~/.config/basecamp.conf`, allowing you to call `Basecamp3()` without any
parameters. You will need to make your own
[Basecamp 3 app integration](https://launchpad.37signals.com/integrations)
first.

### Storing in environment variables

Once you have the credentials you can store them in environment variables:

* `BASECAMP_CLIENT_ID`
* `BASECAMP_CLIENT_SECRET`
* `BASECAMP_REDIRECT_URL`
* `BASECAMP_ACCESS_TOKEN`
* `BASECAMP_REFRESH_TOKEN`

This will allow for easier deploys using CI, initializing with:

```py
from basecampy3 import Basecamp3

bc3 = Basecamp3.from_environment()
```

## Usage

### Basic Example

```py
from basecampy3 import Basecamp3

bc3 = Basecamp3()

for project in bc3.projects.list():
    print(project.name)

new_project = bc3.projects.create("My New Project",
                                  description="The best project ever made.")
new_project.campfire.post_message("Hello World!")
new_message = new_project.message_board.post_message("Check this out",
                                                     content="This is a new message thread start.")
new_message.archive()

todolist = new_project.todoset.create("Things to be done")
todolist.create("Get Milk")
todolist.create("Get Eggs")
go_to_bed = todolist.create("Go to bed.")
go_to_bed.check()  # this is marked as done
```

**Not all functionality of the API is available yet.** For anything missing, you
can use the [requests Session object][Session Objects] yourself directly and 
consult the [Basecamp 3 API docs]. The benefit of using this Session object 
is you will benefit from the authentication, rate-limiting, and caching 
features.

The full API _is_ implemented in the `basecampy3.urls` package, however. The 
`Basecamp3` object now has a `urls` object that implements a 1:1 mapping 
with the Basecamp 3 API. Using this `urls` object, you can create the URL 
you need to get the information you want, and then call `.request()` on it to 
receive a `Response` object, from which you can use `.json()` to get the 
data you are looking for.

### Direct Session Example

```python
from basecampy3 import Basecamp3
import json

bc3 = Basecamp3()

# replace these with actual IDs of the Basecamp objects you wish to get
recording_id = 123456789
project_id = 1234567

# Reference:
# https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments

url = bc3.urls.comments.list_by_recording(project=project_id,
                                          recording=recording_id)
response = url.request(bc3.session)
if not response.ok:
    print("Something went wrong. %s: %s" % (
    response.status_code, response.text))
    exit(1)

data = response.json()
pretty_print = json.dumps(data, indent=4)
print(pretty_print)
```

### CLI Example

**COMING SOON!**
Command Line interface for doing stuff with Basecamp.
**(not working yet)**

```
  $ bc3 copy-access 12341234 87658765  # give user 87658765 access to all the projects that 12341234 does
```

## Todo

- The rest of the Basecamp 3 API
- Command line tool (beyond just the "configure" command)
- Better testing coverage

[Basecamp 3 API docs]: <https://github.com/basecamp/bc3-api/tree/master/sections>
[Session Objects]:  <https://requests.readthedocs.io/en/master/user/advanced/#session-objects>
