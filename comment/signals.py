"""
Signals relating to comments.
"""
from django.dispatch import Signal

 


comment_will_be_posted = Signal(providing_args=["comment", "request"])

# Sent just after a comment was posted. See above for how this differs
# from the Comment object's post-save signal.
comment_was_posted = Signal(providing_args=["comment", "request"])

# Sent after a comment was "flagged" in some way. Check the flag to see if this
# was a user requesting removal of a comment, a moderator approving/removing a
# comment, or some other custom user flag.
comment_was_flagged = Signal(providing_args=["comment", "flag", "created", "request"])

comment_save = Signal(providing_args=["comment", "object"])