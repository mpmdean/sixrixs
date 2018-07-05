from setuptools import setup
import versioneer

setup(name='sixrixs',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Python based analysis for RIXS images and spectra',
      url='https://github.com/mpmdean/sixrixs',
      author='Mark P. M. Dean',
      author_email='mdean@bnl.gov',
      license='MIT',
      packages=['sixrixs'],
      install_requires=['lmfit', 'pandas', 'h5py', 'ipywidgets', 'traitlets', 'ipympl', 'pillow'],
      zip_safe=False)
