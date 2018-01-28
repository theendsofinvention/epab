Changelog
=========
0.3.3 (2018-01-28)
------------------
Changes
~~~~~~~
- Release should push tags only (#16) [132nd-etcher]
  chg: release should push tags only
0.3.3a2 (2018-01-28)
--------------------
Changes
~~~~~~~
- Release should push tags only. [132nd-etcher]
0.3.2a1 (2018-01-28)
--------------------
New
~~~
- Config options to exclude files from flake8 linting. [132nd-etcher]
0.3.1 (2018-01-28)
------------------
New
~~~
- Add push command. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
  update requirements [auto]
  update changelog [auto]
0.2.5 (2018-01-28)
------------------
New
~~~
- Add status cmd to Repo. [132nd-etcher]
- Chglog: add option to infer next version. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
  update requirements [auto]
  update changelog [auto]
- Add "stage" options for autopep8 and isort. [132nd-etcher]
- Create artifacts on AV. [132nd-etcher]
Changes
~~~~~~~
- Disable changelog during release. [132nd-etcher]
- Upload to Pypi only from master. [132nd-etcher]
- Eliminate remote commits. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
0.2.5a19 (2018-01-27)
---------------------
New
~~~
- Package artifacts on AV. [132nd-etcher]
0.2.5b5 (2018-01-27)
--------------------
Fix
~~~
- Fix changelog write. [132nd-etcher]
0.2.4a198 (2018-01-26)
----------------------
Changes
~~~~~~~
- Git push should only push the current branch. [132nd-etcher]
Fix
~~~
- Fix git push command. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
0.2.4a189 (2018-01-26)
----------------------
Changes
~~~~~~~
- Dev almost got it ... [132nd-etcher]
Other
~~~~~
- Chg. dev. still those strqnge i;port issues. [132nd-etcher]
0.2.4a170 (2018-01-23)
----------------------
New
~~~
- Add pre-commit hook for reqs and chglog. [132nd-etcher]
- Add "--no-stash" command to prevent stashing. [132nd-etcher]
- Add a few options to the pytest runner. [132nd-etcher]
- Create tests for Repo.stash. [132nd-etcher]
- Add "stashed" and "amend" logic to isort. [132nd-etcher]
  pep8 [auto]
- Repo: add stash and unstash. [132nd-etcher]
- Add "stashed" decorator. [132nd-etcher]
- Add test for __main__.cli. [132nd-etcher]
- Add test for _pytest. [132nd-etcher]
- Add tests for _run. [132nd-etcher]
- Add delegator.py to reqs. [132nd-etcher]
- Add quiet and verbose options. [132nd-etcher]
- Add global CTX. [132nd-etcher]
- Add install_hooks command. [132nd-etcher]
- Add a bunch of tests. [132nd-etcher]
- In_tmp_dir fixture. [132nd-etcher]
- Context fixture. [132nd-etcher]
- _global_tear_down. [132nd-etcher]
  Unstub all mockito fixtures
  Make sure we're back in the original working directory
- Add dummy property to sys while running tests. [132nd-etcher]
- Test__sanitize_files_to_add. [132nd-etcher]
- Test__sanitize_amend_commit_message. [132nd-etcher]
- Add possibility to stage requirements and changelog instead of
  committing. [132nd-etcher]
- Add optinal pytest options to test runner. [132nd-etcher]
- Add option to test_runner to show result after successful run. [132nd-
  etcher]
Changes
~~~~~~~
- Change hooks so they do not stash changes. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
- Do not re-append same message to commit multiple times. [132nd-etcher]
  update requirements [auto]
  update changelog [auto]
  release 0.2.4a147
- Linters: rename commit option to amend. [132nd-etcher]
- Changed the release process. [132nd-etcher]
- Add stashed logic to reqs and chglog. [132nd-etcher]
- "--version" and "--new-version" commands will now print bare output to
  console. [132nd-etcher]
- Pep8 amends last commit. [132nd-etcher]
- Prettify Repmo.ensure() output. [132nd-etcher]
- Mark all repo tests as long. [132nd-etcher]
- __main__: made commands and linters lists. [132nd-etcher]
- __main__: remove click context from main cli. [132nd-etcher]
- __main__: comment out pyinstaller section for the time being. [132nd-
  etcher]
- Remove passing random args to pytest from test_runner. [132nd-etcher]
- Ignore click commands in coverage. [132nd-etcher]
- New run method using hacked delegator. [132nd-etcher]
- Lint: use CONFIG in linters. [132nd-etcher]
- Mark repo tests as long. [132nd-etcher]
- Use CONFIG in test_runner. [132nd-etcher]
- Use standard newline in changelog. [132nd-etcher]
- Encode changelog in UTF8. [132nd-etcher]
- Skip Git hooks during commit amend. [132nd-etcher]
- New config management. [132nd-etcher]
- Console: multiplt changes. [132nd-etcher]
  Factor out Colors
  Rename args to kwargs
  All commands return the emitted text
  Remove process name
- Add a few badges to readme. [132nd-etcher]
- Switch from versioneer to setuptools_scm. [132nd-etcher]
- Remove gitchangelog tag from reqs commit msg. [132nd-etcher]
Fix
~~~
- Fix requirement tests. [132nd-etcher]
  update requirements [auto]
  update changelog [auto]
  release 0.2.4a149
- Fix filtering reqs output. [132nd-etcher]
  pep8 [auto]
  sorting imports [auto]
- Tests: fix tests. [132nd-etcher]
- Fix tests. [132nd-etcher]
- Remove test files that made their way into the repo. [132nd-etcher]
- Fix linters tests for amend. [132nd-etcher]
- Fix pylint command. [132nd-etcher]
- Fix stashing of empty index. [132nd-etcher]
- Fix tests according to latest changes. [132nd-etcher]
  update requirements [auto]
  update requirements [auto]
- _reqs: fix reqs output. [132nd-etcher]
- _run: fix filters string list. [132nd-etcher]
- Fix changelog output. [132nd-etcher]
  update changelog [auto]
- Epab.utils.run now returns output verbatim. [132nd-etcher]
- Add console output during (un)stashing. [132nd-etcher]
- Fix gitconfig config file not vendored. [132nd-etcher]
- __main__: set CTX.dry_run at start. [132nd-etcher]
- Sanitize os.environ between tests. [132nd-etcher]
- Fix come issues in _repo.py. [132nd-etcher]
- Config: do not cast None or False values. [132nd-etcher]
- Fix all tests for latest changes. [132nd-etcher]
- Use new repo logic in _lint. [132nd-etcher]
- Remove relative import. [132nd-etcher]
- Add a little delay after switching Git branch in tests. [132nd-etcher]
- Fix test_repo screwing up cwd. [132nd-etcher]
- Fix amend_commit. [132nd-etcher]
- Add dry run logic for requirements. [132nd-etcher]
Other
~~~~~
- Fix fix pytest runner. [132nd-etcher]
- Fix fix _sanitize_commit_msg. [132nd-etcher]
0.2.4 (2018-01-23)
------------------
Fix
~~~
- Fix unsafe YAML loading. [132nd-etcher]
- Fix ctx.obj initialization. [132nd-etcher]
Other
~~~~~
- Update reqs-dev.txt [skip ci] [132nd-etcher]
0.2.3 (2018-01-18)
------------------
- Update requirements-dev.txt. [132nd-etcher]
- Update requirements-dev.txt. [132nd-etcher]
0.2.1 (2018-01-02)
------------------
Fix
~~~
- Fix error with no extended commit msg. [132nd-etcher]
0.1.52 (2018-01-02)
-------------------
Changes
~~~~~~~
- Set new version based on AV tag. [132nd-etcher]
0.1.49 (2018-01-02)
-------------------
Fix
~~~
- Fix tagged release. [132nd-etcher]
0.1.48 (2018-01-02)
-------------------
New
~~~
- Release tagged versions without bump. [132nd-etcher]
Other
~~~~~
- Trivia. [132nd-etcher]
0.1.47 (2017-12-28)
-------------------
Changes
~~~~~~~
- Bump pylint jobs from 2 to 8. [132nd-etcher]
0.1.46 (2017-12-27)
-------------------
New
~~~
- Add "--long" option for pytest. [132nd-etcher]
0.1.45 (2017-12-26)
-------------------
Changes
~~~~~~~
- Add faker to reqs. [132nd-etcher]
0.1.44 (2017-12-25)
-------------------
Changes
~~~~~~~
- Run linters even when not on develop. [132nd-etcher]
0.1.43 (2017-12-25)
-------------------
Changes
~~~~~~~
- Tweak pylint settings. [132nd-etcher]
0.1.42 (2017-12-24)
-------------------
Changes
~~~~~~~
- Auto-add [skip ci] to cmiit msg when on AV. [132nd-etcher]
0.1.38 (2017-12-23)
-------------------
Changes
~~~~~~~
- Git reset changes before adding specific files. [132nd-etcher]
0.1.37 (2017-12-23)
-------------------
Fix
~~~
- Omit versioneer files during coverage. [132nd-etcher]
0.1.36 (2017-12-17)
-------------------
Fix
~~~
- Skip ci only on AV builds. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
0.1.35 (2017-12-17)
-------------------
Fix
~~~
- Remove 'EPAB: ' string from console output. [132nd-etcher]
0.1.34 (2017-12-17)
-------------------
Changes
~~~~~~~
- Add line length to autopep8. [132nd-etcher]
0.1.33 (2017-12-17)
-------------------
Fix
~~~
- Make sure all commands are run only once. [132nd-etcher]
0.1.32 (2017-12-17)
-------------------
Fix
~~~
- Remove 'EPAB: ' string from console output. [132nd-etcher]
0.1.31 (2017-12-17)
-------------------
Changes
~~~~~~~
- Pylint: pass FIXME and TODO. [132nd-etcher]
0.1.30 (2017-12-17)
-------------------
Changes
~~~~~~~
- Tweaking pylint options. [132nd-etcher]
0.1.29 (2017-12-17)
-------------------
Fix
~~~
- Pylint options. [132nd-etcher]
0.1.28 (2017-12-17)
-------------------
Changes
~~~~~~~
- Do not install the current package during AV release. [132nd-etcher]
0.1.27 (2017-12-17)
-------------------
Fix
~~~
- Add site-package to pylint to include imports. [132nd-etcher]
0.1.26 (2017-12-17)
-------------------
Changes
~~~~~~~
- Reqs update should not skip ci. [132nd-etcher]
- Using external AV config. [132nd-etcher]
- Add "EPAB:" in front of all output. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
- Using appveyor release process. [132nd-etcher]
Fix
~~~
- Run test suite from EPAB to generate coverage. [132nd-etcher]
- Sanitize console output. [132nd-etcher]
- Sanitize console output. [132nd-etcher]
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
- Add pre_build, wheel, sdist and upload commands. [132nd-etcher]
- Clean build folder. [132nd-etcher]
- Add ctx obj. [132nd-etcher]
0.1.5 (2017-08-24)
------------------
- Update changelog. [132nd-etcher]
- Update requirements. [132nd-etcher]
- Rename wheel -> build and add sdist command. [132nd-etcher]
0.1.4 (2017-08-22)
------------------
- Added wheel command. [132nd-etcher]
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
- Initial commit. [132nd-etcher]