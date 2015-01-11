from distutils.core import setup

version = '0.2.9',

setup(
    name='crosservice',
    version=version,
    packages=['crosservice'],
    install_requires=open('requirements.txt').read(),
    license='GPL',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description='Gevent powered cross service communication tool',
    url='https://github.com/derfenix/crosservice',
    download_url='https://github.com/derfenix/crosservice/archive/v.{0}'
                 '.tar.gz'.format(version),
    keywords=['communication', 'gevent', 'socket'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
    ],
)
