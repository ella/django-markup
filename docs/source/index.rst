====================
django-markup
====================

When writing article or adding a comment, one would like to add some formatting to his text. This can be done either by entering later-validated HTML (by hand or using some WYSIWYG editor), or by inserting text formatting character in some markup language.

django-markup is a Django application that lets you easily process various markup languages, storing text source separately and providing HTML output for your model. Published under `BSD license <http://www.opensource.org/licenses/bsd-license.php>`_, it can be used in almost any application.

Source code is available in `our github repository <http://github.com/ella/django-markup/tree/master>`_, project can be tracked on `ohloh <https://www.ohloh.net/p/django-markup>`_ and for feedback, you're welcomed in `ella maillist <http://groups.google.com/group/ella-project>`_.

If you prefer reading code (aka "who reads documentation?"), take a look at `example_project <http://github.com/ella/django-markup/tree/3ff050cb5e0f0e24ca6c9dff8385218ea80b7e6b/tests/example_project>`_; simple example describing how to incorporate django-markup in your project lives there.

django-markup requires django 1.1 to work, and library for Your favourite markup language to handle transformations. Build-ins are markdown (requires python-markdown2) and czechtile (TODO: not implemented yet).

.. toctree::
   :maxdepth: 2

----------------------------
Basic concept
----------------------------

Basic idea is simple: "Plain" (markup) text is a helper, used for better user experience and thus stored separately (in :class:`SourceText` model). Actual text is pre-rendered HTML (or whatever you want, though now only HTML is assumed), stored when expected (i.e. model attribute of Your model).

----------------------------
Attaching to existing class
----------------------------

As an example, consider this class: ::

	class Article(models.Model):
		text = models.TextField()

Now You want to let user edit this model in admin in markup of your choice and have HTML rendered in text attribute. For that, you must create your own :class:`ModelAdmin` and register it with your model. Using prepared one from django-markup, this is fairly easy: just create :mod:`admin.py` module in your application and insert something like this: ::

	from django.contrib.sites.admin import admin
	from djangomarkup.admin import RichTextOptions
	from exampleapp.models import Article

	class ArticleOptions(RichTextOptions):
		rich_text_field_names = ["text"]
		syntax_processor_name = "markdown"

	admin.site.register(Article, ArticleOptions)

Log in to admin, create new article and format it using markdown syntax. You should now see your content in :class:`SourceText` model, and when you insert :attr:`text` somewhere in your page, you should get generated HTML.

----------------------------
Using markup editor in admin
----------------------------

TODO: not implemented yet

----------------------------
Using unsupported markup
----------------------------
TODO: insert row in :class:`Processor` with function pointing to yours.