from setuptools import setup,find_packages
from codecs import open
from os import path
here=path.abspath(path.dirname(__file__))
with open(path.join(here,'README.rst'),encoding='utf-8')as f:
	long_description=f.read()
setup(name='gtkapplication',version='2021.5.19',description='The PyPhone',long_description=long_description,url='https://www.thepyphone.com',author='PyPhone Author',author_email='author@thepyphone.com',license='None',classifiers=['Development Status :: 4 - Beta','Intended Audience :: Developers','Topic :: Software Development :: Phone','License :: OSI Approved :: None License','Programming Language :: Python :: 3'],keywords='raspberry pi python phone',packages=find_packages(exclude=['devworkstation/','dist/','docs/','downloads/','gtkapplication.egg-info/','logs/','pi/','releases/','tests/','tests_gtk/','venv/','voicemail/']),package_data={'':['*.glade','*.css','*.xml'],'gtkapplication.data':['config_data.py','ring.mp3'],},entry_points={'gui_scripts':['gtkapplication=gtkapplication.main:main',],},)