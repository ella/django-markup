
from example_project.tests.test_admin.helpers import AdminTestCase

class TestArticleBasics(AdminTestCase):

    # FIXME: remove
    def test_simple_login(self):
        self.login_superuser()
        self.logout()
