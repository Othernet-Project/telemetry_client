from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='telemetry_client',
      version='1.0',
      description='Outernet Telemetry Client',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)'
        'Programming Language :: Python :: 2.7',
      ],
      keywords='Outernet Telemetry Client',
      url='https://github.com/Outernet-Project/telemetry_client',
      author='Outernet Inc',
      author_email='abhishek@outernet.is',
      license='GPL',
      packages=['telemetry_client'],
      install_requires=[
          'ondd_ipc',
          'netifaces'
      ],
      entry_points={
          'console_scripts': ['telemetry_client=telemetry_client.main:main'],
      },
      include_package_data=True,
      zip_safe=False)

