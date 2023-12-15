import setuptools

setuptools.setup(
    name="persona",
    version="0.1",
    packages=['persona'],
    include_package_data=True,
    description='Base client for OpenAI API and term-world personae.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()]
)
