from setuptools import setup, find_packages

setup(
    name = 'readlineio',
    description = 'Python client for readline.io',
    packages = find_packages(),
    author = 'Albert Sheu',
    author_email = 'albert.sheu [at] gmail.com',
    url = 'https://github.com/readlineio/rio-py',
    license = 'MIT',
    version = '0.0.0',
    install_requires=['requests'],
    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Internal Tools',
      'License :: OSI Approved :: MIT License',
      'Program Language :: Python :: 2.7',
      'Program Language :: Python :: 3.5',
    ]
)