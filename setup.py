from distutils.core import setup
import os

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-js-initial-bootstrap',
    version='',
    packages=['django_js_initial_bootstrap'],
    url='',
    license='MIT',
    author='Shaun Stanworth',
    author_email='',
    description='',
    install_requires=[
        'Django >= 1.3',
        'djangorestframework >= 2.3.6',
    ]
)
