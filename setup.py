from setuptools import setup, find_packages

setup(name='kakapo',
      version='1.0.0',
      description='Copy journal information from pubmed to vivo',
      url='http://github.com/akash314/kakapo',
      author='Akash Agarwal',
      author_email='agarwala989@gmail.com',
      license='MIT',
      packages=find_packages(),
      scripts=['kakapo_run.py'],
      zip_safe=False)
