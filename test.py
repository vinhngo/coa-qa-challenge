import pytest
from validate_url import validate_url
from urllib import parse


# Example with our function
def test_identity():
    assert validate_url("www.austintexas.gov") == "www.austintexas.gov"

# Write your own tests below
# The names of your functions must be prefixed with "test_" in order for pytest
# to pick them up.


# Python dictionary cannot have dupe keys so this is a good way to kill dupes
def extract_params(url):
    return dict(parse.parse_qsl(parse.urlsplit(url).query))


"""
    Test input url match happy path, some commented out cases that don't pass
    but wasn't sure if in scope
"""


@pytest.mark.parametrize("url, expected", [
    ("www.austintexas.gov", "www.austintexas.gov"),
    # ("http://www.austintexas.gov", "http://www.austintexas.gov"),
    # ("www.austintexas.gov/help/stuff", "www.austintexas.gov"),
    # (None, None)
])
def test_basic_url_match(url, expected):
    assert validate_url(url) == expected


# Test that unique parameters persist
def test_unique_params_persistence():
    url = 'www.austintexas.gov?a=1&b=2&foo=bar&3=5&4=cats'
    params = extract_params(url)
    validated_url = validate_url(url)
    for p in params:
        assert (str(p) + "=" + str(params[p])) in validated_url


"""
    Test remove dupe parameters, note that I do not care which parameters are
    removed. If it is important to keep the first dupe parameter then this test
    can be rewritten to accommodate
"""


def test_remove_dupe_params():
    url = 'www.austintexas.gov?a=1&b=2&a=2&a=3'
    params = extract_params(url)
    validated_url = validate_url(url)
    validated_params = extract_params(validated_url)
    assert len(params) == len(validated_params)


# Test remove string parameters, include multiple params and empty params
@pytest.mark.parametrize("url, params_to_remove", [
    ('www.austintexas.gov?a=1&b=2&foo=bar&3=5&4=cats', ['a']),
    ('www.austintexas.gov?a=1&a=2&b=3', ['a']),
    ('www.austintexas.gov?a=1&b=3', ['a', 'b']),
    ('www.austintexas.gov?a=1&b=3&foo=bar&cats=fun', ['a', 'b', 'foo']),
    ('www.austintexas.gov?a=1&b=3&foo=bar&cats=fun', []),
])
def test_remove_params(url, params_to_remove):
    validated_url = validate_url(url, params_to_remove)
    url_params = extract_params(url)
    validated_params = extract_params(validated_url)
    assert len(url_params) == len(validated_params) + len(params_to_remove)


# Test remove string parameters that don't exist, which fails!
def test_remove_non_existant_params():
    url = 'www.austintexas.gov?a=1&b=2&foo=bar&3=5&4=cats'
    validated_url = validate_url(url, ['cookie'])
    url_params = extract_params(url)
    validated_params = extract_params(validated_url)
    assert len(url_params) == len(validated_params)


# Test convert domain suffix including non 3-letter domain and .gov persist
@pytest.mark.parametrize("url, expected", [
    ("www.austintexas.foo", "www.austintexas.gov"),
    ("www.foo.barbar", "www.foo.gov"),
    ("www.foo.gov", "www.foo.gov"),
    ("www.foo.bar.bar", "www.foo.gov"),
    ("www.foo.bar/", "www.foo.gov"),
    ("www.foo.bar/?a=1&b=2&c=3", "www.foo.gov?a=1&b=2&c=3")
])
def test_convert_domain_suffix(url, expected):
    assert validate_url(url) == expected
