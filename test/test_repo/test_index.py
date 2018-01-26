# coding=utf-8


def test_stage_all(repo, file_set):
    for file in file_set:
        assert file.name in repo.untracked_files()
    repo.stage_all()
    assert not repo.untracked_files()
    for file in file_set:
        assert file.name in repo.list_staged_files()


def test_stage_subset(repo, file_set):
    for file in file_set:
        assert file.name in repo.untracked_files()
    repo.stage_subset(file_set[:3])
    assert repo.untracked_files()
    for file in file_set[:3]:
        assert file.name in repo.list_staged_files()
    for file in file_set[3:]:
        assert file.name not in repo.list_staged_files()


def test_stage_updated(repo, file_set):
    for file in file_set:
        assert file.name in repo.untracked_files()
    repo.stage_subset(file_set[:3])
    repo.repo.index.commit(message='test')
    for file in file_set[3:]:
        assert file.name not in repo.list_staged_files()
        assert file.name in repo.untracked_files()
    file_set[0].write_text('blob')
    repo.stage_modified()
    assert repo.list_staged_files() == [file_set[0].name]


def test__sanitize_files_to_add(repo):
    assert repo._sanitize_files_to_add([]) is None
    assert repo._sanitize_files_to_add('test') == ['test']
    assert repo._sanitize_files_to_add(['test']) == ['test']
    assert repo._sanitize_files_to_add(['test', 'test']) == ['test', 'test']
