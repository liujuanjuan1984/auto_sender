import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rum_auto_sender",
    version="0.1.2",
    author="liujuanjuan1984",
    author_email="qiaoanlu@163.com",
    description="auto sender for local dirpath to rum group",
    keywords=["mininode", "rumsystem", "quorum"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liujuanjuan1984/auto_sender",
    project_urls={
        "Github Repo": "https://github.com/liujuanjuan1984/auto_sender",
        "Bug Tracker": "https://github.com/liujuanjuan1984/auto_sender/issues",
        "About Quorum": "https://github.com/rumsystem/quorum",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["example"]),
    python_requires=">=3.8",
    install_requires=[
        "mininode",
    ],
)
