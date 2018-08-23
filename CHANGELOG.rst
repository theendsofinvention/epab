Changelog
=========
2018.08.22.1 (2018-08-22)
-------------------------
- Autopep8 should run before flake8 (#63) [etcher]
2018.08.22.1a2+feature/fix_pytest-vcr_reqs (2018-08-22)
-------------------------------------------------------
- Update pipfile.lock. [132nd-etcher]
- Add missing pytest-vcr dependency to setup.py. [132nd-etcher]
- Add pip>=18 to Pipfile. [132nd-etcher]
2018.08.22.1a1+feature/lint_order (2018-08-21)
----------------------------------------------
- Autopep8 should run before flake8. [132nd-etcher]
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
2018.08.21.1a1+feature/add_pytest-vcr (2018-08-21)
--------------------------------------------------
- Update hypothesis hash so AV doesn't complain. [132nd-etcher]
- Add deadline setting for hypothesis. [132nd-etcher]
  Deprecation warning pending
- Add test for removal of htmlcov dir. [132nd-etcher]
- Disable VCR recording on AV. [132nd-etcher]
- Add test for data file freeze. [132nd-etcher]
- Fix exe_version for latest pefile. [132nd-etcher]
- Remove coverage of iSort unicode exception. [132nd-etcher]
- Update reqs. [132nd-etcher]
- Add pytest-vcr to reqs. [132nd-etcher]
2018.08.20.1 (2018-08-20)
-------------------------
Fix
~~~
- Fix line endings when using isort (#61) [etcher]
2018.08.20.1a1+feature/fix_isort_newlines (2018-08-20)
------------------------------------------------------
Fix
~~~
- Fix line endings when using isort. [132nd-etcher]
2018.08.19.1 (2018-08-19)
-------------------------
Changes
~~~~~~~
- Trivia (#60) [etcher]
  * chg: dev: sort imports
  * chg: pylint: ignore fstring logging errors
  * chg: add dummy except for iSort errors
2018.08.19.1a1+feature/trivia (2018-08-19)
------------------------------------------
Changes
~~~~~~~
- Add dummy except for iSort errors. [132nd-etcher]
- Pylint: ignore fstring logging errors. [132nd-etcher]
2018.06.17.5a2+feature/sort_only_project_files (2018-06-17)
-----------------------------------------------------------
- Fix freeze tests. [132nd-etcher]
- Disable freezeing. [132nd-etcher]
2018.06.17.5a1+feature/sort_only_project_files (2018-06-17)
-----------------------------------------------------------
- Fix isort tests. [132nd-etcher]
- Cleanup comments. [132nd-etcher]
2018.06.17.3 (2018-06-17)
-------------------------
Fix
~~~
- Fix isort encoding (#57) [132nd-etcher]
2018.06.17.3a1+feature/fix_isort_encoding (2018-06-17)
------------------------------------------------------
Fix
~~~
- Fix isort encoding. [132nd-etcher]
2018.06.15.2 (2018-06-15)
-------------------------
- Add mypy to setup.py. [132nd-etcher]
2018.06.15.1a1+feature/update_reqs (2018-06-15)
-----------------------------------------------
- Update reqs. [132nd-etcher]
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
2018.05.16.1a2+feature/mypy (2018-05-16)
----------------------------------------
- Fixed issue. [132nd-etcher]
- Linting. [132nd-etcher]
- Fixed mypy issues. [132nd-etcher]
- Marked a few tests as long. [132nd-etcher]
- Add BaseRepo for typing purposes. [132nd-etcher]
- Fix linters test. [132nd-etcher]
- Peppered a few ignore lines. [132nd-etcher]
- Cleanup gitignore. [132nd-etcher]
- Update git ignore. [132nd-etcher]
- Add git ignore util. [132nd-etcher]
- Add mypy linter. [132nd-etcher]
2018.05.16.1a1+feature/mypy (2018-05-16)
----------------------------------------
- Update reqs. [132nd-etcher]
2018.05.15.1 (2018-05-15)
-------------------------
New
~~~
- Compile qt resources (#51) [132nd-etcher]
  * new: add command to compile Qt resources
  * ignore coverage artifacts
  * linting
  * fix issues and add tests
2018.05.15.1a1+feature/compile_qt_resources (2018-05-15)
--------------------------------------------------------
New
~~~
- Add command to compile Qt resources. [132nd-etcher]
Other
~~~~~
- Fix issues and add tests. [132nd-etcher]
- Linting. [132nd-etcher]
- Ignore coverage artifacts. [132nd-etcher]
2018.05.13.1 (2018-05-13)
-------------------------
New
~~~
- Create sample config if it doesn't exist (#50) [132nd-etcher]
  * create sample config if it doesn't exist
  * oopsies
  * linting
  * fix lil' mistake
2018.05.11.2a1+feature/config_sample (2018-05-11)
-------------------------------------------------
- Fix lil' mistake. [132nd-etcher]
- Linting. [132nd-etcher]
- Oopsies. [132nd-etcher]
- Create sample config if it doesn't exist. [132nd-etcher]
2018.05.11.1 (2018-05-11)
-------------------------
Changes
~~~~~~~
- Clean after pyinstaller (#49) [132nd-etcher]
  * update reqs
  * rename config attributes for freezing
  * clean spec file
  * clean env after freeze
2018.05.11.1a1+feature/clean_after_pyinstaller (2018-05-11)
-----------------------------------------------------------
- Clean env after freeze. [132nd-etcher]
- Clean spec file. [132nd-etcher]
- Rename config attributes for freezing. [132nd-etcher]
- Update reqs. [132nd-etcher]
2018.04.28.1 (2018-04-28)
-------------------------
Changes
~~~~~~~
- Use pipfile.lock (#48) [132nd-etcher]
  * un-ignore pipfile.lock
  * do not delete pifile.lock during reqs update
  * update reqs
2018.04.28.1a1+feature/pipfile_lock (2018-04-28)
------------------------------------------------
- Update reqs. [132nd-etcher]
- Do not delete pifile.lock during reqs update. [132nd-etcher]
- Un-ignore pipfile.lock. [132nd-etcher]
2018.04.14.2 (2018-04-14)
-------------------------
Changes
~~~~~~~
- Switch to pyinstaller command (#47) [132nd-etcher]
  * chg: switch to pyinstaller command
  * linting
2018.04.14.2a1+feature/switch_to_pyinstaller_cmd (2018-04-14)
-------------------------------------------------------------
Changes
~~~~~~~
- Switch to pyinstaller command. [132nd-etcher]
Other
~~~~~
- Linting. [132nd-etcher]
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
Fix
~~~
- Fix freeze version (#46) [132nd-etcher]
  * ignore test artifact
  * write requirements in setup.py
  * update reqs
  * linting
  * fix: fix epab freeze version
  * switch calver to padded
0.3.34 (2018-03-03)
-------------------
New
~~~
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
Changes
~~~~~~~
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
Fix
~~~
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
Other
~~~~~
- Linting. [132nd-etcher]
- Update reqs. [132nd-etcher]
- Disable isort setup.py feature for now. [132nd-etcher]
- Add iPython. [132nd-etcher]
- Add entry point. [132nd-etcher]
- Create LICENSE. [132nd-etcher]
- Delete LICENSE. [132nd-etcher]
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
Fix
~~~
- Fix changelog write. [132nd-etcher]
- Fix unsafe YAML loading. [132nd-etcher]
- Fix ctx.obj initialization. [132nd-etcher]
- Fix error with no extended commit msg. [132nd-etcher]
Other
~~~~~
- Update requirements-dev.txt. [132nd-etcher]
- Update reqs-dev.txt [skip ci] [132nd-etcher]
- Update requirements-dev.txt. [132nd-etcher]
0.1.52 (2018-01-02)
-------------------
New
~~~
- Release tagged versions without bump. [132nd-etcher]
- Add "--long" option for pytest. [132nd-etcher]
- Add flake8 params as default. [132nd-etcher]
- Add appveyor command. [132nd-etcher]
- Add isort command. [132nd-etcher]
Changes
~~~~~~~
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
- Fix tagged release. [132nd-etcher]
- Omit versioneer files during coverage. [132nd-etcher]
- Skip ci only on AV builds. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
- Make sure all commands are run only once. [132nd-etcher]
- Remove 'EPAB: ' string from console output. [132nd-etcher]
- Pylint options. [132nd-etcher]
- Add site-package to pylint to include imports. [132nd-etcher]
- Run test suite from EPAB to generate coverage. [132nd-etcher]
- Sanitize console output. [132nd-etcher]
- Sanitize console output. [132nd-etcher]
- Appveyor release. [132nd-etcher]
- Install requirements using pip. [132nd-etcher]
- Fix runner options. [132nd-etcher]
- Spelling and imports. [132nd-etcher]
- Fix reqs ref. [132nd-etcher]
- Remove leftover appveyor.yml file. [132nd-etcher]
- Fix run_once. [132nd-etcher]
- Apparently, --all and --tags are incompatible ... [132nd-etcher]
- Push all refs after release. [132nd-etcher]
- Fix tests. [132nd-etcher]
- Fixed pre_build exiting early. [132nd-etcher]
- Fix package name for get_version. [132nd-etcher]
Other
~~~~~
- Trivia. [132nd-etcher]
- Chg do not write hashes to requirements. [132nd-etcher]
- Add pre_build, wheel, sdist and upload commands. [132nd-etcher]
- Clean build folder. [132nd-etcher]
- Add ctx obj. [132nd-etcher]
- Update changelog. [132nd-etcher]
- Update requirements. [132nd-etcher]
- Rename wheel -> build and add sdist command. [132nd-etcher]
- Added wheel command. [132nd-etcher]
- Add auto install of pip-tools. [132nd-etcher]
- Add auto install of pip-tools. [132nd-etcher]
- Initial commit. [132nd-etcher]