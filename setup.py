from setuptools import setup
import versioneer

setup(name='ataglances',
      description='Custom dashboard for monitoring multiple machines',
      author='Gili "OpenBagTwo" Barlev',
      url='https://github.com/OpenBagTwo/ataglances',
      packages=['ataglances'],
      license='GPL v3',
      install_requires=['requests'],
      include_package_data=True,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass())
