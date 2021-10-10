from codecs import open
import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as infile:
    long_description = infile.read()

about = {}
with open(os.path.join(here, 'basecampy3', '__version__.py'), 'r', encoding='utf-8') as infile:
    exec(infile.read(), about)

setup(
    name='basecampy3',
    version=about['__version__'],
    packages=find_packages(),
    install_requires=[
        "python-dateutil",
        "pytz",
        "requests",
        "six",
    ],
    entry_points={
        'console_scripts': [
            'bc3 = basecampy3.bc3_cli:main',
        ],
    },
    url='https://github.com/phistrom/basecampy3',
    license='MIT',
    author='Phillip Stromberg',
    author_email='phillip@strombergs.com',
    description='Aims to be the easiest to use version of the Basecamp 3 API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown"
)
