from setuptools import setup

VERSION = "0.1.5"


with open('README.md', 'r') as infile:
    long_description = infile.read()

setup(
    name='basecampy3',
    version=VERSION,
    packages=[
        'basecampy3',
        'basecampy3.endpoints'
    ],
    install_requires=[
        "beautifulsoup4==4.6.0",
        "certifi>=2018.1.18",
        "chardet==3.0.4",
        "idna==2.6",
        "python-dateutil==2.7.2",
        "requests==2.18.4",
        "six==1.11.0",
        "urllib3==1.22",
    ],
    entry_points={
        'console_scripts': [
            'bc3 = basecampy3.bc3_cli:main',
        ],
    },
    url='https://github.com/phistrom/basecampy3',
    license='MIT',
    author='Phillip Stromberg',
    author_email='phillip@4stromberg.com',
    description='Aims to be the easiest to use version of the Basecamp 3 API',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ),
    long_description=long_description,
    long_description_content_type="text/markdown"
)
