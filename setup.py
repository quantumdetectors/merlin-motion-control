import setuptools
import time, os.path as path
from setuptools import setup, find_packages

major_ver = 2
minor_ver = 0
nano_ver = 0
branch = ''

version = "%d.%d.%d%s" % (major_ver, minor_ver, nano_ver, branch)

##### Get info from associated text files #####
# Write version.py
with open( "merlin_motion_control/__version__.py", 'w' ) as fh:
    fh.write( "__version__ = '" + version + "'\n" )

# Get the long description from the README file
try:
    with open(path.join('.', 'README.md'), encoding='utf-8') as f:
        readmerst = f.read()
except: # No long description
    readmerst = ""
    pass

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


def setup_module():
    metadata = dict(
                      name = "merlin_motion_control",
                      version = version,
                      description='Quantum Detectors Merlin Motion Control',
                      long_description = readmerst,
                      author='Richard Skogeby',
                      author_email='richard@quantumdetectors.com',
                      url='',
                      license='MIT',
                      packages=find_packages(),
                      install_requires=requirements,
                      setup_requires=requirements,
                      entry_points={
                          # 'gui_scripts' suppresses stdout, which we generally do not want
                          'console_scripts': ['mmc=merlin_motion_control:main',],
                          'gui_scripts': []
                          },
                      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
                      extras_require={
                        },
                    package_data={
                        '': ['*.json', '*.ico', 'dmc/*.dmc', '*.kv', '.env'],
                        },
                    classifiers=[
                            # How mature is this project? Common values are
                            #   3 - Alpha
                            #   4 - Beta
                            #   5 - Production/Stable
                            'Development Status :: 4 - Beta',
                    
                            # Indicate who your project is intended for
                            'Topic :: Scientific/Engineering :: Automation',
                    
                            # Pick your license as you wish (should match "license" above)
                            'License :: MIT',
                    
                            # Specify the Python versions you support here. In particular, ensure
                            # that you indicate whether you support Python 2, Python 3 or both.
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.7',
							
                            # OS
                            'Operating System :: Microsoft :: Windows',
                        ],
                    keywords=[''],
                    #zip_safe=False, # DLLs cannot be zipped
    )
    

    setup(**metadata)


if __name__ == '__main__':
    t0 = time.time()
    setup_module()
    t1 = time.time()
    print( "Completed: build/install time (s): %.3f" % (t1-t0) )
