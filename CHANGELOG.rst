Changelog
=========
(unreleased)
------------
Changes
~~~~~~~
- Remove flake8. [etcher]
  It requires pycodestyle and that makes Pipenv go nuts
2018.10.24.1 (2018-10-24)
-------------------------
Fix
~~~
- Fix release description (#114) [etcher]
  * fix: fix release description
  Set an OS environ variable that'll be used to assign the release
  long description instead of relying on the commit extended message
  only.
  Fixes #108
  * fix: dev: simplify code
2018.10.23.4 (2018-10-23)
-------------------------
- Build(deps): bump hypothesis from 3.79.0 to 3.79.2 (#112)
  [dependabot[bot]]
  Bumps [hypothesis](https://github.com/HypothesisWorks/hypothesis) from 3.79.0 to 3.79.2.
  - [Release notes](https://github.com/HypothesisWorks/hypothesis/releases)
  - [Commits](https://github.com/HypothesisWorks/hypothesis/compare/hypothesis-python-3.79.0...hypothesis-python-3.79.2)
2018.10.23.1 (2018-10-23)
-------------------------
- Build(deps): bump pytest from 3.9.1 to 3.9.2. [dependabot[bot]]
  Bumps [pytest](https://github.com/pytest-dev/pytest) from 3.9.1 to 3.9.2.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/3.9.1...3.9.2)
2018.10.22.1 (2018-10-22)
-------------------------
- Build(deps): bump elib-run from 2018.10.17.1 to 2018.10.21.1.
  [dependabot[bot]]
  Bumps [elib-run](https://github.com/etcher-be/elib_run) from 2018.10.17.1 to 2018.10.21.1.
  - [Release notes](https://github.com/etcher-be/elib_run/releases)
  - [Commits](https://github.com/etcher-be/elib_run/compare/2018.10.17.1...2018.10.21.1)
2018.10.21.4 (2018-10-21)
-------------------------
- Build(deps): bump elib-run from 2018.9.9.1 to 2018.10.17.1 (#103)
  [dependabot[bot]]
  Bumps [elib-run](https://github.com/etcher-be/elib_run) from 2018.9.9.1 to 2018.10.17.1.
  - [Release notes](https://github.com/etcher-be/elib_run/releases)
  - [Commits](https://github.com/etcher-be/elib_run/commits/2018.10.17.1)
2018.10.21.3 (2018-10-21)
-------------------------
- Build(deps): bump hypothesis from 3.78.0 to 3.79.0. [dependabot[bot]]
  Bumps [hypothesis](https://github.com/HypothesisWorks/hypothesis) from 3.78.0 to 3.79.0.
  - [Release notes](https://github.com/HypothesisWorks/hypothesis/releases)
  - [Commits](https://github.com/HypothesisWorks/hypothesis/compare/hypothesis-python-3.78.0...hypothesis-python-3.79.0)
2018.10.21.2 (2018-10-21)
-------------------------
- Build(deps): bump wheel from 0.32.1 to 0.32.2. [dependabot[bot]]
  Bumps [wheel](https://github.com/pypa/wheel) from 0.32.1 to 0.32.2.
  - [Release notes](https://github.com/pypa/wheel/releases)
  - [Changelog](https://github.com/pypa/wheel/blob/master/docs/news.rst)
  - [Commits](https://github.com/pypa/wheel/compare/0.32.1...0.32.2)
2018.10.21.1 (2018-10-21)
-------------------------
Fix
~~~
- Remove existing graph files (#105) [etcher]
2018.10.15.1 (2018-10-15)
-------------------------
Fix
~~~
- Revert latest elib_run update. [etcher]
  shutil.which is broken for me, that'll need a bit more work
2018.10.14.2 (2018-10-14)
-------------------------
Changes
~~~~~~~
- Strip down console logging verbosity. [etcher]
2018.10.14.1 (2018-10-14)
-------------------------
Changes
~~~~~~~
- Add support for site package data files (#100) [etcher]
  * chg: add support for site-package data files
  * chg: dev: update reqs
  * chg: dev: linting
2018.10.01.1 (2018-10-01)
-------------------------
Fix
~~~
- Pytest arg fix (#97) [etcher]
  * fix pytest args for latest click
  * fix tests for new version of click
  * update reqs
2018.09.16.2 (2018-09-16)
-------------------------
Changes
~~~~~~~
- Disable autopep8 (#95) [etcher]
  * disable autopep8
  * chg: dev: linting
  * chg: dev: linting
  * chg: dev: update reqs
2018.09.12.1 (2018-09-12)
-------------------------
Changes
~~~~~~~
- Update pyinstaller (#91) [etcher]
  * use pyinstaller 3.4 for freezing
  * update reqs
2018.09.09.2 (2018-09-09)
-------------------------
Fix
~~~
- Fix freeze (#90) [etcher]
  * fix pyinstaller installation for freezing
  * fix pyinstaller timeout
  * add a bit of logging
  * fix tests for freezing
  * linting
2018.09.02.4 (2018-09-02)
-------------------------
Changes
~~~~~~~
- Prepush order (#88) [etcher]
  * update reqs should happen first
  * dev: remove unused entry in .gitignore
2018.09.02.3 (2018-09-02)
-------------------------
Fix
~~~
- Fix conftest.py (#87) [etcher]
  * fix conftest.py
  * fix: fix fixtures names in conftest.py
  * update reqs
2018.09.02.2 (2018-09-02)
-------------------------
Fix
~~~
- Fix missing req in setup.py (#86) [etcher]
2018.09.02.1 (2018-09-02)
-------------------------
New
~~~
- Add graphs (#85) [etcher]
  * add graphs command
2018.08.31.3 (2018-08-31)
-------------------------
- Update reqs (#84) [etcher]
2018.08.28.7 (2018-08-28)
-------------------------
New
~~~
- Pipenv commands and prepush (#80) [etcher]
  * add pipenv and prepush commands
  * update chglog
2018.08.28.6 (2018-08-28)
-------------------------
Fix
~~~
- Fix removal of htmlcov (#79) [etcher]
  * fix: ignore missing htmlcov when removing it
  * chg: made removal of htmlcov optional
  Useful with pytest-watch in between runs
2018.08.28.5 (2018-08-28)
-------------------------
Fix
~~~
- Fix gitchangelog tag regex (#78) [etcher]
  * fix: fix gitchangelog tag regex
  * fix error in chglog command
2018.08.28.3 (2018-08-28)
-------------------------
New
~~~
- Add bandit (#74) [etcher]
  * add bandit to reqs
  * add bandit command
  * re-add bandit to Pipfile
  * add bandit click command
  * add test for bandit
  * linting
  * update reqs
  * fix linter tests
  * remove duplicate code
Changes
~~~~~~~
- Increase pytest cmd timeout (#76) [etcher]
  * increase pytest cmd timeout
  For those super long tests I like =)
  * update pipfile.lock
2018.08.28.2 (2018-08-28)
-------------------------
Fix
~~~
- Fix README.md [skip ci] [etcher]
2018.08.27.4 (2018-08-27)
-------------------------
Fix
~~~
- Fix missing reqs in setup.py. [etcher]
2018.08.27.3 (2018-08-27)
-------------------------
- Fix config (#71) [etcher]
  Config setup should happen before writing the example file
2018.08.27.2 (2018-08-27)
-------------------------
New
~~~
- Pytest deadfixtures (#70) [etcher]
  * update reqs
  * add pytest_deadfixture as a linter
  * add basic test for pytest_deadfixture
  * update reqs
  * fix tests
  Fixes #10
Other
~~~~~
- Fix pipfile.lock. [etcher]
2018.08.27.1 (2018-08-27)
-------------------------
Fix
~~~
- Fix config setup (#69) [etcher]
  * update reqs
  * check for "pyproject.toml" existence
  * write examples before potentially raising
2018.08.26.2 (2018-08-26)
-------------------------
Changes
~~~~~~~
- Sarge runner (#68) [etcher]
  * restore newline to stdout func
  * update reqs
  * linting
2018.08.26.1 (2018-08-26)
-------------------------
Changes
~~~~~~~
- New config (#67) [etcher]
  * move version inference to root __init__.py
  * remove old test
  * add ruamel.yaml to reqs
  * update .gitignore
  * update reqs
  * switch to elib_config
  * Merge branch 'master' into feature/new_config
  * update .gitignore
  * ignore root venv during flake8 run
  * linting
  * add BCH config
  * fix console tests
2018.08.25.2 (2018-08-25)
-------------------------
Changes
~~~~~~~
- Disable iSort (#66) [etcher]
  * disable iSort during linting
  * remove iSort altogether
2018.08.25.1 (2018-08-25)
-------------------------
Changes
~~~~~~~
- Flake8 ignore venv (#65) [etcher]
  * update gitignore
  * ingore local .venv during flake8 check
2018.08.22.1 (2018-08-22)
-------------------------
- Autopep8 should run before flake8 (#63) [etcher]
2018.08.21.1 (2018-08-21)
-------------------------
New
~~~
- Add pytest vcr (#62) [etcher]
  * add pytest-vcr to reqs
  * update reqs
  * remove coverage of iSort unicode exception
  * fix exe_version for latest pefile
  * add test for data file freeze
  * disable VCR recording on AV
  * add test for removal of htmlcov dir
  * add deadline setting for hypothesis
  Deprecation warning pending
  * update hypothesis hash so AV doesn't complain
2018.08.20.1 (2018-08-20)
-------------------------
Fix
~~~
- Fix line endings when using isort (#61) [etcher]
2018.08.19.1 (2018-08-19)
-------------------------
Changes
~~~~~~~
- Trivia (#60) [etcher]
  * chg: dev: sort imports
  * chg: pylint: ignore fstring logging errors
  * chg: add dummy except for iSort errors
2018.06.17.3 (2018-06-17)
-------------------------
Fix
~~~
- Fix isort encoding (#57) [132nd-etcher]
2018.06.15.2 (2018-06-15)
-------------------------
- Add mypy to setup.py. [132nd-etcher]
2018.05.16.1 (2018-05-16)
-------------------------
New
~~~
- Add MyPY linter (#52) [132nd-etcher]
  * update reqs
  * add mypy linter
  * add git ignore util
  * update git ignore
  * cleanup gitignore
  * peppered a few ignore lines
  * fix linters test
  * add BaseRepo for typing purposes
  * marked a few tests as long
  * fixed mypy issues
  * linting
  * fixed issue
2018.05.15.1 (2018-05-15)
-------------------------
New
~~~
- Compile qt resources (#51) [132nd-etcher]
  * new: add command to compile Qt resources
  * ignore coverage artifacts
  * linting
  * fix issues and add tests
2018.05.13.1 (2018-05-13)
-------------------------
New
~~~
- Create sample config if it doesn't exist (#50) [132nd-etcher]
  * create sample config if it doesn't exist
  * oopsies
  * linting
  * fix lil' mistake
2018.05.11.1 (2018-05-11)
-------------------------
Changes
~~~~~~~
- Clean after pyinstaller (#49) [132nd-etcher]
  * update reqs
  * rename config attributes for freezing
  * clean spec file
  * clean env after freeze
2018.04.28.1 (2018-04-28)
-------------------------
Changes
~~~~~~~
- Use pipfile.lock (#48) [132nd-etcher]
  * un-ignore pipfile.lock
  * do not delete pifile.lock during reqs update
  * update reqs
2018.04.14.2 (2018-04-14)
-------------------------
Changes
~~~~~~~
- Switch to pyinstaller command (#47) [132nd-etcher]
  * chg: switch to pyinstaller command
  * linting
2018.04.14.1 (2018-04-14)
-------------------------
New
~~~
- Flat freeze (#42) [132nd-etcher]
  * add flat freeze
  * add test for freeze
  * cleanup __main__
  * simplify pyinstaller build commands
  * simplify __main__ further
  * linting
  * linting
  * add upload of coverage to scrutinizer
  * fix issue with freeze command
  * fix test_runner test
  * fix test_runner test
  * fix test_runner test
  * testing ocular
  * test for scrut token
  * linting
  * remove unused import
  * stop toying with ENV
  * oops
  * test for scrut token
  * nevermind, I'll fix it myself
  * fix ocular coverage source
  * install pyinstaller only if needed
  * move codacy to pytest cmd
  * add exception for when an exe is not found
  * update tests
  * linting
  * linting
  * disable ocular coverage
  * fix tests
- Freeze (#34) [132nd-etcher]
  * add methods to retrieve version from exe
  * add certifi as a req
  * add verpatch as vendor
  * add app.ico as resource
  * use sys.exit for pyinstaller
  * use AV to push tag back
  * add resources
  * lint exe version
  * tweak package description
  * add resource_path
  * add raw git version
  * add freeze
  * linting
  * update reqs
  * fix tests
  * fix patch
  * simplify release
- Config options to exclude files from flake8 linting. [132nd-etcher]
- Add push command. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
  update requirements [auto]
  update changelog [auto]
- Add status cmd to Repo. [132nd-etcher]
- Chglog: add option to infer next version. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
  update requirements [auto]
  update changelog [auto]
- Add "stage" options for autopep8 and isort. [132nd-etcher]
- Create artifacts on AV. [132nd-etcher]
- Release tagged versions without bump. [132nd-etcher]
- Add "--long" option for pytest. [132nd-etcher]
- Add flake8 params as default. [132nd-etcher]
- Add appveyor command. [132nd-etcher]
- Add isort command. [132nd-etcher]
Changes
~~~~~~~
- Disable pylint wrong import order check (#45) [132nd-etcher]
- Switch from semver to calver (#43) [132nd-etcher]
  * fix license issue in setup.py
  * add missing test for find_exe
  * add repo.list_of_tags
  * add test for repo.short_sha
  * remove dummy test file
  * comment out scrutinizer coverage upload
  * fix error in find_exe
  * fix repo.get_latest_tag
  * switch to calver
  * update reqs
  * sanitize AV output
  * make console prefix a variable
  * update reqs
  * remove unused file
  * fix assertions
  * add name of skipped tests
- Disable logging-format-interpolation (#33) [132nd-etcher]
- Re-enable isort (#29) [132nd-etcher]
- Be more specific with autopep8 (#28) [132nd-etcher]
  When he project folder is bloated (EDLM?), autopep8 takes ages
  to parse through all the junk.
  All we really want is to check:
    1. The package itself
    2. The tests
- Disable isort linter (#27) [132nd-etcher]
  * disable isort linter
  * disable isort linter
  * disable isort linter
- Overwrite exiting tag on release (#26) [132nd-etcher]
  * overwrite exiting tag on release
  * fix tests
- Disable auto stash (#25) [132nd-etcher]
  * disable auto stash
  * fix tests
- Reorder linters (#20) [132nd-etcher]
  * chg: dev: move classifiers to a raw string
  * chg: reorder linters
- Update readme (#19) [132nd-etcher]
  * chg: update readme
  * chg: update README
  * chg: update README
  * chg: update README
- Update readme (reverted from commit
  e64f8cb4b81caea005485c9b4362dcecf994f14c) [132nd-etcher]
- Update readme. [132nd-etcher]
- Add feature name in tag (#18) [132nd-etcher]
  * chg: simplify gitversion config
  * chg: change tagging scheme
- Print status on checkout when repo is dirty. [132nd-etcher]
- Release should push tags only (#16) [132nd-etcher]
  chg: release should push tags only
- Disable changelog during release. [132nd-etcher]
- Upload to Pypi only from master. [132nd-etcher]
- Eliminate remote commits. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
- Set new version based on AV tag. [132nd-etcher]
- Bump pylint jobs from 2 to 8. [132nd-etcher]
- Add faker to reqs. [132nd-etcher]
- Run linters even when not on develop. [132nd-etcher]
- Tweak pylint settings. [132nd-etcher]
- Auto-add [skip ci] to cmiit msg when on AV. [132nd-etcher]
- Git reset changes before adding specific files. [132nd-etcher]
- Add line length to autopep8. [132nd-etcher]
- Pylint: pass FIXME and TODO. [132nd-etcher]
- Tweaking pylint options. [132nd-etcher]
- Do not install the current package during AV release. [132nd-etcher]
- Reqs update should not skip ci. [132nd-etcher]
- Using external AV config. [132nd-etcher]
- Add "EPAB:" in front of all output. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
- Show files when repo is dirty. [132nd-etcher]
- Add vendored config for pylint and pytest + coverage. [132nd-etcher]
- Remove pytest-pep8 as it's covered by the linters. [132nd-etcher]
- Return short tag. [132nd-etcher]
- Commit only subset of files for chglog and reqs. [132nd-etcher]
- Do not write hashes to reqs (reverted from commit
  de3078b4bb3d0438dc76333c8ddd8331f367ab1c) [132nd-etcher]
- Do not write hashes to reqs. [132nd-etcher]
- Use pip instead of pipenv for setup.py requirements. [132nd-etcher]
- Rename AV build after succesfull release. [132nd-etcher]
- Remove bogus av file. [132nd-etcher]
- Release only on develop. [132nd-etcher]
- Update AV build number. [132nd-etcher]
- Add switch to develop branch on AV to keep commits. [132nd-etcher]
- Add twine info. [132nd-etcher]
- Remove linters install cmd and add them as reqs. [132nd-etcher]
- Do not re-ionstall current package if it's epab. [132nd-etcher]
- Add wheel to AV install. [132nd-etcher]
- Add command to install linters. [132nd-etcher]
- Exit gracefully when releasing from foreign branch. [132nd-etcher]
- Add auto-commit after requirements update. [132nd-etcher]
- Add option to allow dirty repo. [132nd-etcher]
- Using pipenv to declare setup.py deps. [132nd-etcher]
- Automatically push tags to remote. [132nd-etcher]
- Add check so EPAB does not try reinstalling itself. [132nd-etcher]
Fix
~~~
- Fix freeze version (#46) [132nd-etcher]
  * ignore test artifact
  * write requirements in setup.py
  * update reqs
  * linting
  * fix: fix epab freeze version
  * switch calver to padded
- Skipping freeze should not raise SystemExit (#38) [132nd-etcher]
- Fix app.ico (#37) [132nd-etcher]
  * move app.ico to vendor subfolder
  * fix av build info string
  * remove dupe logging
  * forgot to remove resource from epab.yml
- Frozen version (#35) [132nd-etcher]
  * fix missing resource
  * trying to fix av issue with tag name
  * fix frozen version
- Fix isort issues (#31) [132nd-etcher]
  * fixing isort 1st party
  * add isort setup.py check
  * ignore bacth
  * update reqs
  * fix tests
  * linting
- Sort linting (#24) [132nd-etcher]
- Fix sorting of imports (#22) [132nd-etcher]
  Due to iSort update, a bunch of double line endings were inserted.
  I switched to programmatic iSort instead of calling the cmd line.
  * fix: dev: fix isort
  * convert line endings
  * fix tests
  * fix one more test
- Fix changelog write. [132nd-etcher]
- Fix unsafe YAML loading. [132nd-etcher]
- Fix ctx.obj initialization. [132nd-etcher]
- Fix error with no extended commit msg. [132nd-etcher]
- Fix tagged release. [132nd-etcher]
- Omit versioneer files during coverage. [132nd-etcher]
- Skip ci only on AV builds. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
- Make sure all commands are run only once. [132nd-etcher]