#!/bin/sh

python3 setup.py sdist bdist_wheel

#test any long_description markdown errors (errors will prevent upload to pypi)
#twine check dist/*

#upload to test.pypi.org
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#upload to pypi.org
#twine upload dist/*