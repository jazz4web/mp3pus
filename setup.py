from setuptools import setup, find_packages

from mp3pus import version


setup(
    name='mp3pus',
    version=version,
    packages=find_packages(),
    python_requires='~=3.7',
    install_requires=['mutagen>=1.40'],
    zip_safe=False,
    scripts=['bin/mp3pus'],
    author='AndreyVM',
    author_email='webmaster@codej.ru',
    description='A simple mp3 to opus converter.',
    license='GNU GPLv3',
    keywords='mp3 opus converter',
    url='https://codej.ru/QjK4rbVk')
