import setuptools

setuptools.setup(
    name="discode-server",
    version="0.0.1",
    url="https://github.com/d0ugal/discode-server",
    license="BSD",
    description="Quick code review",
    long_description="TODO",
    author="Dougal Matthews",
    author_email="dougal@dougalmatthews.com",
    keywords='code review codereview discussion',
    packages=setuptools.find_packages(),
    include_package_date=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'discode-server = discode_server.__main__:cli',
        ],
        'pygments.lexers': [
            'mistral = discode_server.lexers.mistral:MistralLexer',
        ]
    },
    classifier=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Utilities'
    ],
)
