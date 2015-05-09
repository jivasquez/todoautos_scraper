from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='Todoautos Scraper',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Juan Ignacio V\xc3\xa1squez',
      author_email='jivasquez0@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'beautifulsoup4',
          'nose'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
