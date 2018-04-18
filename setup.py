from setuptools import setup

setup(
    name='basecampy3',
    version='0.1.0',
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
    scripts=['scripts/bc3.py'],
    entry_points={
        'console_scripts': [
            'bc3 = bc3:main',
        ],
    },
    url='',
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
    )
)
