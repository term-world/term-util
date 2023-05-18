import setuptools

setuptools.setup(
    name="gremlin",
    version="0.1",
    packages=['gremlin'],
    include_package_data=True,
    description='Thar be gremlins.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
