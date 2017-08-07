import numpy
import os

try:
    from setuptools import setup, Extension
    from setuptools_scm import get_version
    use_setuptools = True
    print("setuptools is used.")
except ImportError:
    from distutils.core import setup, Extension
    use_setuptools = False
    print("distutils is used.")

include_dirs_numpy = [numpy.get_include()]
cc = None
if 'CC' in os.environ:
    if 'clang' in os.environ['CC']:
        cc = 'clang'
    if 'gcc' in os.environ['CC']:
        cc = 'gcc'

# Workaround Python issue 21121
import sysconfig
config_var = sysconfig.get_config_var("CFLAGS")
if config_var is not None and "-Werror=declaration-after-statement" in config_var:
    os.environ['CFLAGS'] = config_var.replace(
        "-Werror=declaration-after-statement", "")    

######################
# _phonopy extension #
######################
include_dirs_phonopy = ['c/harmonic_h', 'c/kspclib_h'] + include_dirs_numpy
sources_phonopy = ['c/_phonopy.c',
                   'c/harmonic/dynmat.c',
                   'c/harmonic/derivative_dynmat.c',
                   'c/kspclib/kgrid.c',
                   'c/kspclib/tetrahedron_method.c']

if __name__ == '__main__':
    extra_compile_args_phonopy = []
    extra_link_args_phonopy = []
else:
    extra_compile_args_phonopy = ['-fopenmp',]
    if cc == 'gcc':
        extra_link_args_phonopy = ['-lgomp',]
    elif cc == 'clang':
        extra_link_args_phonopy = []
    else:
        extra_link_args_phonopy = ['-lgomp',]

extension_phonopy = Extension(
    'phonopy._phonopy',
    extra_compile_args=extra_compile_args_phonopy,
    extra_link_args=extra_link_args_phonopy,
    include_dirs=include_dirs_phonopy,
    sources=sources_phonopy)


#####################
# _spglib extension #
#####################
if __name__ == '__main__':
    extra_compile_args_spglib=[]
    extra_link_args_spglib=[]
else:
    extra_compile_args_spglib=['-fopenmp',]
    if cc == 'gcc':
        extra_link_args_spglib=['-lgomp',]
    elif cc == 'clang':
        extra_link_args_spglib=[]
    else:
        extra_link_args_spglib=['-lgomp',]

extension_spglib = Extension(
    'phonopy._spglib',
    include_dirs=['c/spglib_h'] + include_dirs_numpy,
    extra_compile_args=extra_compile_args_spglib,
    extra_link_args=extra_link_args_spglib,
    sources=['c/_spglib.c',
             'c/spglib/arithmetic.c',
             'c/spglib/cell.c',
             'c/spglib/delaunay.c',
             'c/spglib/hall_symbol.c',
             'c/spglib/kgrid.c',
             'c/spglib/kpoint.c',
             'c/spglib/mathfunc.c',
             'c/spglib/niggli.c',
             'c/spglib/pointgroup.c',
             'c/spglib/primitive.c',
             'c/spglib/refinement.c',
             'c/spglib/sitesym_database.c',
             'c/spglib/site_symmetry.c',
             'c/spglib/spacegroup.c',
             'c/spglib/spg_database.c',
             'c/spglib/spglib.c',
             'c/spglib/spin.c',
             'c/spglib/symmetry.c'])

ext_modules_phonopy = [extension_phonopy, extension_spglib]
packages_phonopy = ['phonopy',
                    'phonopy.cui',
                    'phonopy.gruneisen',
                    'phonopy.harmonic',
                    'phonopy.interface',
                    'phonopy.phonon',
                    'phonopy.qha',
                    'phonopy.spectrum',
                    'phonopy.structure',
                    'phonopy.unfolding']
scripts_phonopy = ['scripts/phonopy',
                   'scripts/phonopy-qha',
                   'scripts/phonopy-FHI-aims',
                   'scripts/bandplot',
                   'scripts/outcar-born',
                   'scripts/propplot',
                   'scripts/tdplot',
                   'scripts/dispmanager',
                   'scripts/gruneisen',
                   'scripts/pdosplot']

if __name__ == '__main__':
    ver = get_version().split('.')
    if len(ver)>3 :
        # Post release version:
        #  - add patchlevel at the end
        #  - decrease back last number
        print('Version from SCM:',ver)
        try:
            pl=int(ver[3].split('+')[0][3:])
            ver[2]=str(int(ver[2])-1)
            ver=ver[:3]
            ver.append(str(pl))
        except ValueError:
            # This is probably build from pypi source
            # Just keep the version from setuptools_scm and hope for the best
            pass

    ver='.'.join(ver)

    if use_setuptools:
        setup(name='phonopy',
              version=ver,
              description='This is the phonopy module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://atztogo.github.io/phonopy/',
              packages=packages_phonopy,
              install_requires=['numpy', 'PyYAML', 'matplotlib', 'h5py'],
              provides=['phonopy'],
              scripts=scripts_phonopy,
              ext_modules=ext_modules_phonopy)
    else:
        setup(name='phonopy',
              version=ver,
              description='This is the phonopy module.',
              author='Atsushi Togo',
              author_email='atz.togo@gmail.com',
              url='http://atztogo.github.io/phonopy/',
              packages=packages_phonopy,
              requires=['numpy', 'PyYAML', 'matplotlib', 'h5py'],
              provides=['phonopy'],
              scripts=scripts_phonopy,
              ext_modules=ext_modules_phonopy)


