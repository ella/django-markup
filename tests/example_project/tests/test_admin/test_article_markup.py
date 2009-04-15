
from helpers import AdminTestCase

class TestMarkup(AdminTestCase):

    def test_markup_saving(self):
        s = self.selenium
        text = u"An example text in markdown markup"


        s.click(self.elements['pages']['welcome']['exampleapp_article_add'])

        s.type('id_text', text)
        s.click(self.elements['listing']['save'])

        assert "<p>%s</p>" % text in s.get_text(self.elements['listing']['list_first'])

        s.click(self.elements['listing']['list_first'])

        self.assert_equals(text, s.get_value('id_text'))

