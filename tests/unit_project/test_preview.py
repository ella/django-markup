# -*- coding: utf-8 -*-
from djangosanetesting import DatabaseTestCase
from django.core.urlresolvers import reverse

class TestPreview(DatabaseTestCase):
    def setUp(self):
        super(TestPreview, self).setUp()
        self.processor_name = "markdown"
        self.mock_text = u"beer - 啤酒"
        self.czechtile_text = u"= Text =\n češťoučký texďýčšek"
        self.czechtile_text_transformed = u"<h1>Text</h1><p>češťoučký texďýčšek</p>"
        self.rest_text = u"Text:\n   * češťoučký texďýčšek"
        self.rest_text_transformed = u'<dl class="docutils">\n<dt>Text:</dt>\n<dd><ul class="first last simple">\n<li>češťoučký texďýčšek</li>\n</ul>\n</dd>\n</dl>\n'

    def test_success_default_markdown(self):
        self.assert_equals(u"<p>%s</p>" % self.mock_text, self.client.post(reverse("markup-transform"), {'text' : self.mock_text}).content.strip().decode('utf-8'))

    def test_get_returns_bad_method(self):
        self.assert_equals(405, self.client.get(reverse("markup-transform")).status_code)

    def test_empty_(self):
        self.assert_equals(u"<p>%s</p>" % self.mock_text, self.client.post(reverse("markup-transform"), {'text' : self.mock_text}).content.strip().decode('utf-8'))

    def test_success_rest(self):
        try:
            import docutils
        except ImportError:
            raise self.SkipTest("Docutils not installed, skipping")
        self.assert_equals(self.rest_text_transformed,
            self.client.post(reverse("markup-transform", kwargs={'syntax_processor_name' : "rest"}),
            {'text' : self.rest_text}).content.decode('utf-8')
        )
    def test_success_czechtile(self):
        try:
            import czechtile
        except ImportError:
            raise self.SkipTest("Czechtile not installed, skipping")
        self.assert_equals(self.czechtile_text_transformed,
            self.client.post(reverse("markup-transform", kwargs={'syntax_processor_name' : "czechtile"}),
            {'text' : self.czechtile_text}).content.decode('utf-8')
        )
