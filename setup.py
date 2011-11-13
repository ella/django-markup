from setuptools import setup, find_packages
import djangomarkup

setup(
    name = 'djangomarkup',
    version = djangomarkup.__versionstr__,
    description = 'Support for various markup languages in Django applications',
    long_description = 'Support for various markup languages in Django applications',
    author = 'Ella Development Team',
    author_email='dev@ella-cms.com',
    license = 'BSD',
    url='http://github.com/ella/django-markup',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
        'setuptools>=0.6b1',
        'Django',
        'markdown2',
    ],
)

