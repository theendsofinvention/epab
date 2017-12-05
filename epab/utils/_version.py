# coding=utf-8

import semver

from ._versioneer import get_version


def bump_version(ctx, new_version):
    if 'new_version' in ctx.obj:
        return
    version = get_version()
    if new_version is None:
        new_version = semver.bump_patch(version)
    ctx.obj['new_version'] = new_version
    return new_version
