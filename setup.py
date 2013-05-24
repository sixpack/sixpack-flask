"""
Flask-Sixpack
-------------
"""
from setuptools import setup


setup(
    name='Flask-Sixpack',
    version='0.0.1',
    url='http://sixpack.seatgeek.com/',
    license='BSD',
    author='Zack Kitzmiller',
    author_email='Zack Kitzmiller',
    description='Flask wrapper for Sixpack',
    long_description=__doc__,
    py_modules=['flask_sixpack'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'sixpack-client'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
