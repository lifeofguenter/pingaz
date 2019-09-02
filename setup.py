import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pingaz',
    version='0.0.3',
    author='Gunter Grodotzki',
    author_email='gunter@grodotzki.co.za',
    description='Monitor latency between AZs with fping and cloudwatch.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lifeofguenter/pingaz',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
    install_requires=[
        'boto3',
        'click',
        'ec2-metadata',
    ],
    entry_points={
        'console_scripts': [
            'pingaz = pingaz.__main__:cli',
        ],
    },
)
