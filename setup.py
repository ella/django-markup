from setuptools import setup, find_packages
import djangomarkup

setup(
    name = 'django-markup',
    version = djangomarkup.__version__,
    description = 'Support for various markup languages in Django applications',
    long_description = '\n'.join((
        '(TODO)',
    )),
    author = 'centrum holdings s.r.o',
    license = 'BSD',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    install_requires = [
        'setuptools>=0.6b1',
    ],
)

