import hashlib
import pytest

from ibanchecker import fetchdocument


def test_buildpath():
    content = b"tototiti"
    hex = hashlib.sha256(content).hexdigest()
    assert "/tmp/toto/%s.png" % hex == fetchdocument.build_path(
        content, "/toto/titi/lala.png", "/tmp/toto/"
    )
