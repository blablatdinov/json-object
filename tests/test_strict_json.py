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
from pathlib import Path

import pytest
from jsonschema import ValidationError

from eljson.json_doc import JsonDoc
from eljson.strict_json import StrictJson


def test_validation():
    """Test validating json document by json-schema."""
    json_doc = JsonDoc.from_string('{"hello": {"world": "!"}}')
    got = StrictJson.from_string(
        json_doc,
        (Path(__file__).parent / 'fixtures' / 'valid_shm.json').read_text(),
    ).path('$')

    assert got == json_doc.path('$')


def test_fail_validation():
    """Test fail validation."""
    with pytest.raises(ValidationError):
        StrictJson.from_string(
            JsonDoc.from_string('{"hello": {"world": "!"}}'),
            (Path(__file__).parent / 'fixtures' / 'invalid_shm.json').read_text(),
        ).path('$')
