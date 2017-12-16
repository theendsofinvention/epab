Changelog
=========


0.1.25 (2017-12-16)
-------------------

Fix
~~~
- Appveyor release. [132nd-etcher]


0.1.24 (2017-12-16)
-------------------

New
~~~
- Add flake8 params as default. [132nd-etcher]
- Add appveyor command. [132nd-etcher]

Changes
~~~~~~~
- Show files when repo is dirty. [132nd-etcher]
- Add vendored config for pylint and pytest + coverage. [132nd-etcher]
- Remove pytest-pep8 as it's covered by the linters. [132nd-etcher]
- Return short tag. [132nd-etcher]
- Commit only subset of files for chglog and reqs. [132nd-etcher]
- Do not write hashes to reqs (reverted from commit
  de3078b4bb3d0438dc76333c8ddd8331f367ab1c) [132nd-etcher]
- Do not write hashes to reqs. [132nd-etcher]
- Use pip instead of pipenv for setup.py requirements. [132nd-etcher]

Fix
~~~
- Install requirements using pip. [132nd-etcher]
- Fix runner options. [132nd-etcher]
- Spelling and imports. [132nd-etcher]
- Fix reqs ref. [132nd-etcher]

Other
~~~~~
- Chg do not write hashes to requirements. [132nd-etcher]


0.1.23 (2017-12-16)
-------------------

Fix
~~~
- Remove leftover appveyor.yml file. [132nd-etcher]


0.1.22 (2017-12-16)
-------------------

Changes
~~~~~~~
- Rename AV build after succesfull release. [132nd-etcher]


0.1.21 (2017-12-16)
-------------------

Changes
~~~~~~~
- Remove bogus av file. [132nd-etcher]
- Release only on develop. [132nd-etcher]
- Update AV build number. [132nd-etcher]


0.1.20 (2017-12-16)
-------------------

Changes
~~~~~~~
- Add switch to develop branch on AV to keep commits. [132nd-etcher]


0.1.18 (2017-12-16)
-------------------

Changes
~~~~~~~
- Add twine info. [132nd-etcher]
- Remove linters install cmd and add them as reqs. [132nd-etcher]
- Do not re-ionstall current package if it's epab. [132nd-etcher]
- Add wheel to AV install. [132nd-etcher]
- Add command to install linters. [132nd-etcher]
- Exit gracefully when releasing from foreign branch. [132nd-etcher]

Fix
~~~
- Fix run_once. [132nd-etcher]


0.1.17 (2017-12-16)
-------------------

Changes
~~~~~~~
- Add auto-commit after requirements update. [132nd-etcher]


0.1.16 (2017-12-06)
-------------------

Changes
~~~~~~~
- Add option to allow dirty repo. [132nd-etcher]


0.1.15 (2017-12-06)
-------------------

Fix
~~~
- Apparently, --all and --tags are incompatible ... [132nd-etcher]


0.1.14 (2017-12-06)
-------------------

Fix
~~~
- Push all refs after release. [132nd-etcher]


0.1.13 (2017-12-06)
-------------------

Changes
~~~~~~~
- Using pipenv to declare setup.py deps. [132nd-etcher]


0.1.12 (2017-12-05)
-------------------

Changes
~~~~~~~
- Automatically push tags to remote. [132nd-etcher]


0.1.10 (2017-12-05)
-------------------

Changes
~~~~~~~
- Add check so EPAB does not try reinstalling itself. [132nd-etcher]


0.1.9 (2017-09-02)
------------------

Fix
~~~
- Fix tests. [132nd-etcher]


0.1.8 (2017-08-27)
------------------

Fix
~~~
- Fixed pre_build exiting early. [132nd-etcher]


0.1.7 (2017-08-26)
------------------

New
~~~
- Add isort command. [132nd-etcher]


0.1.6 (2017-08-24)
------------------
- Merge branch 'master' into develop. [132nd-etcher]
- Add pre_build, wheel, sdist and upload commands. [132nd-etcher]
- Add pre_build, wheel, sdist and upload commands. [132nd-etcher]
- Add pre_build, wheel, sdist and upload commands. [132nd-etcher]
- Clean build folder. [132nd-etcher]
- Add ctx obj. [132nd-etcher]


0.1.5 (2017-08-24)
------------------
- Merge branch 'master' into develop. [132nd-etcher]
- Rename wheel -> build and add sdist command. [132nd-etcher]
- Rename wheel -> build and add sdist command. [132nd-etcher]
- Update changelog. [132nd-etcher]
- Update requirements. [132nd-etcher]
- Rename wheel -> build and add sdist command. [132nd-etcher]


0.1.4 (2017-08-22)
------------------
- Add wheel command. [132nd-etcher]
- Added wheel command. [132nd-etcher]
- Merge branch 'master' into develop. [132nd-etcher]


0.1.3 (2017-08-21)
------------------

Fix
~~~
- Fix package name for get_version. [132nd-etcher]


0.1.2 (2017-08-20)
------------------
- Add auto install of pip-tools. [132nd-etcher]
- Add auto install of pip-tools. [132nd-etcher]


0.1.0 (2017-08-19)
------------------
- Initial release. [132nd-etcher]
- Merge branch 'develop' [132nd-etcher]
- Finish 0.1.1. [132nd-etcher]
- Initial release. [132nd-etcher]
- Initial commit. [132nd-etcher]