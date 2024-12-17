from setuptools import Extension, setup


# Modules to be compiled and include_dirs when necessary
c_extensions = [
    Extension(
        '_fastpickle',
        sources=['src/_fastpickle.c'],
        include_dirs=['include/internal', 'include'],
        extra_compile_args=[
            '-fno-strict-overflow',
            '-Wsign-compare',
            '-Wunreachable-code',
            '-DNDEBUG',
            '-g',
            '-O3',
            '-Wall',
        ],
    )
]


setup(
    ext_modules=[
        *c_extensions,  # TODO: Broken on LLVM
    ],
)