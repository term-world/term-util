import setuptools

setuptools.setup(
    name="helper",
    version="0.1",
    packages=['helper'],
    include_package_data=True,
    description='Global helper for python commands.',
    long_description=open('README.md', 'r').read(),
    install_requires=[line.strip() for line in open('requirements.txt', 'r').readlines()],
    entry_points = {
        'console_scripts': [
            'helper = helper:main',
        ],
    }
)
