import setuptools

setuptools.setup(
    name="couchsurf",
    version="0.3",
    packages=['couchsurf'],
    include_package_data=True,
    description='Limited API for basic CouchDB operations.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
 )
