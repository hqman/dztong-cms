import re
import time
import datetime

from django import forms
from django.forms.util import ErrorDict
from django.conf import settings
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.utils.hashcompat import sha_constructor
from django.utils.text import get_text_list
from django.utils.translation import ungettext, ugettext_lazy as _
from dztong.comment.models import DZComment as Comment

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

MAX_TAG_LENGTH = getattr(settings, 'MAX_TAG_LENGTH', 50)

class CommentForm(forms.Form):
    #user_name          = forms.CharField(label=("user_name"), max_length=50)
    content       = forms.CharField(label=_('Comment'), widget=forms.Textarea(attrs={'cols':'50','rows':'15'}),
                                    max_length=COMMENT_MAX_LENGTH)
    content_type  = forms.CharField(widget=forms.HiddenInput)
    object_pk     = forms.CharField(widget=forms.HiddenInput)

    parent_id        = forms.IntegerField(widget = forms.HiddenInput, initial = 0)
    timestamp     = forms.IntegerField(widget = forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)

    def __init__(self, target_object, data=None, initial=None):
        self.target_object = target_object
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(CommentForm, self).__init__(data=data, initial=initial)

    def get_comment_object(self):



        """
        Return a new (unsaved) comment object based on the information in this
        form. Assumes that the form is already validated and will throw a
        ValueError if not.

        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``).
        """
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        new = Comment(


            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            #user_name    = self.cleaned_data["user_name"],
            content      = self.cleaned_data["content"],
            submit_date  = datetime.datetime.now(),
            is_public    = True,
            is_removed   = False,
            parent_id    = 0,
            site_id      = settings.SITE_ID,
        )

        # Check that this comment isn't duplicate. (Sometimes people post comments
        # twice by mistake.) If it is, fail silently by returning the old comment.
        possible_duplicates = Comment.objects.filter(
            content_type = new.content_type,
            object_pk = new.object_pk,
            user_name = new.user_name,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.content == new.content:
                return old

        return new

    def security_errors(self):
        """Return just those errors associated with security"""
        errors = ErrorDict()
        for f in ["honeypot", "timestamp", "security_hash"]:
            if f in self.errors:
                errors[f] = self.errors[f]
        return errors

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def clean_security_hash(self):
        """Check the security hash."""
        security_hash_dict = {
            'content_type' : self.data.get("content_type", ""),
            'object_pk' : self.data.get("object_pk", ""),
            'timestamp' : self.data.get("timestamp", ""),
        }
        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if expected_hash != actual_hash:
            raise forms.ValidationError("Security hash check failed.")
        return actual_hash

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (> 2 hours) in the past."""
        ts = self.cleaned_data["timestamp"]
        if time.time() - ts > (2 * 60 * 60):
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def clean_comment(self):
        """
        If COMMENTS_ALLOW_PROFANITIES is False, check that the comment doesn't
        contain anything in PROFANITIES_LIST.
        """
        content = self.cleaned_data["content"]
        if settings.COMMENTS_ALLOW_PROFANITIES == False:
            bad_words = [w for w in settings.PROFANITIES_LIST if w in content.lower()]
            if bad_words:
                plural = len(bad_words) > 1
                raise forms.ValidationError(ungettext(
                    "Watch your mouth! The word %s is not allowed here.",
                    "Watch your mouth! The words %s are not allowed here.", plural) % \
                    get_text_list(['"%s%s%s"' % (i[0], '-'*(len(i)-2), i[-1]) for i in bad_words], 'and'))
        return content

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'content_type'  : str(self.target_object._meta),
            'object_pk'     : str(self.target_object._get_pk_val()),
            'timestamp'     : str(timestamp),
            'security_hash' : self.initial_security_hash(timestamp),
        }
        return security_dict

    def initial_security_hash(self, timestamp):
        """
        Generate the initial security hash from self.content_object
        and a (unix) timestamp.
        """

        initial_security_dict = {
            'content_type' : str(self.target_object._meta),
            'object_pk' : str(self.target_object._get_pk_val()),
            'timestamp' : str(timestamp),
          }
        return self.generate_security_hash(**initial_security_dict)

    def generate_security_hash(self, content_type, object_pk, timestamp):
        """Generate a (SHA1) security hash from the provided info."""
        info = (content_type, object_pk, timestamp, settings.SECRET_KEY)
        return sha_constructor("".join(info)).hexdigest()

