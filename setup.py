from setuptools import setup

setup(
    name="telepathy",
    version='2.1.3',
    author='Jordan Wildon',
    author_email='j.wildon@pm.me',
    packages=['telepathy'],
    url='https://pypi.python.org/pypi/telepathy/',
    license='LICENSE.txt',
    description='An OSINT toolkit for investigating Telegram chats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=['telepathy'],
    install_requires=[
        'click',
        'telethon',
        'pandas',
        'colorama',
        'alive_progress',
        'beautifulsoup4',
    ],
    entry_points='''
        [console_scripts]
        telepathy=telepathy.telepathy:cli
    ''',
)
