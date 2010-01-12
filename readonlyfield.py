from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django import forms

class ReadOnlyWidget(forms.Widget):
    
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
            return mark_safe("<p %s>%s</p>" % (flatatt(final_attrs), escape(value) or ''))

    def _has_changed(self, initial, data):
        return False

class ReadOnlyField(forms.Field):
    widget = ReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        super(type(self), self).__init__(self, label=label, initial=initial, 
            help_text=help_text, widget=widget)
        self.widget.initial = initial

    def clean(self, value):
        return self.widget.initial
    
class ReadOnlyWidget2(forms.Widget):

    def __init__(self, original_value, display_value):
        self.original_value = original_value
        self.display_value = display_value
        super(ReadOnlyWidget2, self).__init__()
        
    def _has_changed(self, initial, data):
        return False
        
    def render(self, name, value, attrs=None):
        if self.display_value is not None:
            return unicode(self.display_value)
        return unicode(self.original_value)

    def value_from_datadict(self, data, files, name):
        return self.original_value