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

    def test_success_default_markdown(self):
        self.assert_equals(u"<p>%s</p>" % self.mock_text, self.client.post(reverse("markup-transform"), {'text' : self.mock_text}).content.strip().decode('utf-8'))

    def test_get_returns_bad_method(self):
        self.assert_equals(405, self.client.get(reverse("markup-transform")).status_code)

    def test_empty_(self):
        self.assert_equals(u"<p>%s</p>" % self.mock_text, self.client.post(reverse("markup-transform"), {'text' : self.mock_text}).content.strip().decode('utf-8'))

    def test_success_czechtile(self):
        self.assert_equals(self.czechtile_text_transformed,
            self.client.post(reverse("markup-transform", kwargs={'syntax_processor_name' : "czechtile"}),
            {'text' : self.czechtile_text}).content.decode('utf-8')
        )
