"""The MIT License (MIT).

Copyright (c) 2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
import pytest

from eljson.exceptions import NodeNotFoundError
from eljson.json_doc import JsonDoc


@pytest.mark.parametrize(('json_str', 'path', 'expected'), [
    ('{"hello": {"world": "!"}}', '$.hello.world', ['!']),
    ('{"hello": {"world": 1}}', '$.hello.world', [1]),
    ('{"hello": {"world": null}}', '$.hello.world', [None]),
    ('{"hello": {"world": true}}', '$.hello.world', [True]),
    ('{"hello": {"world": [false]}}', '$.hello.world', [[False]]),
])
def test_path(json_str, path, expected):
    """Test fetching nodes by jsonpath."""
    got = JsonDoc.from_string(json_str).path(path)

    assert got == expected


def test_fail_path():
    """Test not exists node."""
    with pytest.raises(NodeNotFoundError):
        JsonDoc.from_string(
            '{"hello": {"world": "!"}}',
        ).path('$.hello.world.name')
