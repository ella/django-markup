from django import forms

class RichTextAreaWidget(forms.Textarea):
    """
    TextArea that is extendable to contain markup-specific editor.
    """

#    def __init__(self, height=None, attrs={}):
#        css_class = CLASS_RICHTEXTAREA
#        if height:
#            css_class += ' %s' % height
#        super(RichTextAreaWidget, self).__init__(attrs={'class': css_class})

    def render(self, name, value, attrs=None):
        if value:
            src_text = self._field.get_source_text()
        else:
            src_text = value
        return super(RichTextAreaWidget, self).render(name, src_text, attrs)
