from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='PinyinCopybook',
      version=version,
      description="拼音汉字田字格A4模版, 排版后生成Pillow Image",
      long_description="""\
""",
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3',
                   'Topic :: Text Processing :: Markup :: reStructuredText',
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords="'pinyin copybook'",
      author='Mike Song',
      author_email='',
      url='',
      license='Apache 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Pillow>=10.0.1',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
