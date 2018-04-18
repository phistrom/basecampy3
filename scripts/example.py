"""
This should be an example in the README.md and it should be runnable. If it's not, then that's pretty embarrassing.
"""

from basecampy3 import Basecamp3

bc3 = Basecamp3()

for project in bc3.projects.list():
    print(project.name)

new_project = bc3.projects.create("My New Project", description="The best project ever made.")
new_project.campfire.post_message("Hello World!")
new_message = new_project.message_board.post_message("Check this out", content="This is a new message thread start.")
new_message.archive()

todolist = new_project.todoset.create("Things to be done")
todolist.create("Get Milk")
todolist.create("Get Eggs")
go_to_bed = todolist.create("Go to bed.")
go_to_bed.check()  # this is marked as done
