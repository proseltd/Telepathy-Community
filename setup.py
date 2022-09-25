from setuptools import setup

setup(
    name="telepathy",
    version='2.1.10',
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
        'click', 'requires == 7.1.2',
        'telethon', 'requires == 1.24.0',
        'pandas', 'requires == 1.4.2',
        'colorama', 'requires == 0.4.3',
        'alive_progress', 'requires == 2.4.1',
        'beautifulsoup4', 'requires == 4.9.3',
        'requests', 'requires == 2.28.1',
        'googletrans', 'requires == 3.1.0a0',
        'pprintpp', 'requires == 0.4.0'
    ],
    entry_points='''
        [console_scripts]
        telepathy=telepathy.telepathy:cli
    ''',
)
