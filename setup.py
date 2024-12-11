
# setup.py
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
import sys

is_debug = True  

compile_args = [
    '-fno-strict-overflow',
    '-Wsign-compare',
    '-Wunreachable-code',
    '-Wall',
    '-lpthread',
    '-fno-inline',         
    '-fvisibility=default',
]
link_args = []

if is_debug:
    compile_args += ['-g', '-O0', '-fno-omit-frame-pointer']
    # ['-g', '-O0', '-fno-omit-frame-pointer', '-fsanitize=address']
    # Uncomment below if address sanitization is needed
    # link_args += ['-fsanitize=address']
else:
    compile_args += ['-DNDEBUG', '-O3']

pickle_module = Extension(
    '_fastpickle',
    sources=['src/_pickle.c', 'src/threadpool.c'],
    include_dirs=['Include/internal', 'Include/custom', 'Include'],
    extra_compile_args=compile_args,
    extra_link_args=link_args,
)

setup(
    name='faster_pickle',
    version='1.0',
    description='A pickle module extension',
    ext_modules=[pickle_module],
    py_modules=['pickle'],
)
