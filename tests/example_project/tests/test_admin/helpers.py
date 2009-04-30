from djangosanetesting import SeleniumTestCase

class AdminTestCase(SeleniumTestCase):
    fixtures = ['example_admin_user']

    SUPERUSER_USERNAME = u"superman"
    SUPERUSER_PASSWORD = u"xxx"

    URI = "/admin/"

    def __init__(self):
        super(AdminTestCase, self).__init__()
        self.elements = {
            'navigation' : {
                'logout' : '//a[contains(@href, "%slogout/")]' % self.URI,
                'home' : '//div[@class="breadcrumbs"]/a[position()=1]',
            },
            'listing' : {
                'save' : '//input[@name="_save"]',
                'delete' : '//a[@class="deletelink"]',
                'delete_confirm' : '//div[@id="content"]//form/div/input[@type="submit"]',
                'list_first' : '//div[@id="changelist"]//table/tbody/tr[position()=1]/th[position()=1]/a',
                'list_second' : '//div[@id="changelist"]//table/tbody/tr[position()=2]/th[position()=1]/a',
                'count_field' : '//div[@id="changelist"]/form/p',
            },
            'pages' : {
                'welcome' : {
                    'exampleapp_article' : '//a[ends-with(@href, "exampleapp/article/")]',
                    'exampleapp_article_add' : '//a[contains(@href, "exampleapp/article/add/")]',
                    'djangomarkup_text_sources' : '//a[contains(@href, "djangomarkup/sourcetext/")]',
                },
                'login' : {
                    'submit' : "//input[@type='submit']"
                }
            }
        }

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.login_superuser()

    def tearDown(self):
        self.logout()
        super(AdminTestCase, self).tearDown()

    def login_superuser(self):
        self.selenium.open(self.URI)
        self.selenium.type("id_username", self.SUPERUSER_USERNAME)
        self.selenium.type("id_password", self.SUPERUSER_PASSWORD)
        self.selenium.click(self.elements['pages']['login']['submit'])

    def logout(self):
        self.selenium.click(self.elements['navigation']['logout'])
        self.selenium.wait_for_page_to_load(30000)

