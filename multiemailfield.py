from django import forms
from django.forms.fields import email_re
import re

email_regex = re.compile(email_re)

class MultiEmailField(forms.Field):
    def clean(self, value):
        """
        Check that the field contains one or more comma-separated emails
        and normalizes the data to a list of the email strings.
        """
        if not value:
            raise forms.ValidationError('Enter at least one e-mail address.')
        emails = value.split(',')
        emails = [el.strip() for el in emails]
        for email in emails:
            if not is_valid_email(email):
                raise forms.ValidationError('%s is not a valid e-mail address.' % email)

        # Always return the cleaned data.
        return emails
    
def is_valid_email(email):
    if email == u'':
        return email
    return True if email_regex.search(email) else False
    