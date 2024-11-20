# setup.py
from setuptools import setup, Extension
import sys


is_debug = False  

compile_args = ['-fno-strict-overflow', '-Wsign-compare', '-Wunreachable-code', '-Wall', '-lpthread']
link_args = []

if is_debug:
    compile_args += ['-g', '-O0', '-fsanitize=address', '-fno-omit-frame-pointer']
    link_args += ['-fsanitize=address']
else:
    compile_args += ['-DNDEBUG', '-O3']

pickle_module = Extension(
    '_pickle',
    sources=['src/_pickle.c', 'src/threadpool.c'],
    include_dirs=['Include/internal', 'Include/custom' ,'Include'],
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
