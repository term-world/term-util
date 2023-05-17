import setuptools

setuptools.setup(
    name="cookies",
    version="0.1",
    packages=['cookies'],
    include_package_data=True,
    description='Marketing cookies. Because...why not?',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
