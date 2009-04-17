
from helpers import AdminTestCase

class TestMarkup(AdminTestCase):

    def test_markup_successfull_saving(self):
        s = self.selenium
        text = u"An example text in markdown markup"


        s.click(self.elements['pages']['welcome']['exampleapp_article_add'])

        s.type('id_text', text)
        s.type('id_email', 'examplemail@example.com')
        s.click(self.elements['listing']['save'])
        s.wait_for_page_to_load(3000)

        assert "<p>%s</p>" % text in s.get_text(self.elements['listing']['list_first'])

        s.click(self.elements['listing']['list_first'])

        self.assert_equals(text, s.get_value('id_text'))

    def test_unsuccessfull_save_do_not_generate_sourcetext(self):
        s = self.selenium
        text = u"An example text in markdown markup"

        s.click(self.elements['pages']['welcome']['exampleapp_article_add'])

        s.type('id_text', text)
        s.click(self.elements['listing']['save'])
        s.wait_for_page_to_load(3000)

        s.click(self.elements['navigation']['home'])

        s.click(self.elements['pages']['welcome']['djangomarkup_text_sources'])

        self.assert_equals(u"0 Text sources", s.get_text(self.elements['listing']['count_field']))
