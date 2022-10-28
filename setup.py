from setuptools import setup, find_packages

setup(
    name="telepathy",
    version='2.3.2',
    author='Jordan Wildon',
    author_email='j.wildon@pm.me',
    packages=['telepathy'],
    package_dir={'':'src'},
    url='https://pypi.python.org/pypi/telepathy/',
    license='LICENSE.txt',
    description='An OSINT toolkit for investigating Telegram chats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'click ~= 7.1.2',
        'telethon == 1.25.2',
        'pandas == 1.4.2',
        'colorama ~= 0.4.3',
        'alive_progress == 2.4.1',
        'beautifulsoup4 == 4.11.1',
        'requests ~= 2.28.1',
        'googletrans == 4.0.0rc1',
        'pprintpp == 0.4.0',
    ],
    entry_points='''
        [console_scripts]
        telepathy=telepathy.telepathy:cli
    ''',
)
