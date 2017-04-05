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
    install_requires=[
        'Jinja2==2.9.5',
        'Pygments==2.2.0',
        'SQLAlchemy==1.1.6',
        'WTForms==2.1',
        'aiopg==0.13.0',
        'alembic==0.9.1',
        'click==6.7',
        'limits==1.2.1',
        'websockets==3.2',

        # Rwmove the following on the next Sanic release (and add Sanic).
        'httptools>=0.0.9',
        'uvloop>=0.5.3',
        'ujson>=1.35',
        'aiofiles>=0.3.0',
    ],
    entry_points={
        'pygments.lexers': [
            'mistral = discode_server.utils.highlight:MistralLexer',
        ],
        'console_scripts': [
            'discode-server = discode_server.__main__:cli',
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
