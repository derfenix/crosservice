from distutils.core import setup


setup(
    name='crosservice',
    version='2.0',
    packages=['crosservice'],
    url='http://',
    install_requires=open('requirements.txt').read(),
    license='GPL',
    author='derfenix',
    author_email='derfenix@gmail.com',
    description='Cross-service comunication python library'
)
