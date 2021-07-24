import pytest

from ibanchecker.validateiban import ValidateNameIban


def _check_values(test_input, expected, docpath):
    ibanc = ValidateNameIban(test_input["name"], test_input["iban"], docpath)
    ibanc.run()
    assert ibanc.valid == expected["valid"]
    assert ibanc.status["iban"] == expected["iban"]
    assert ibanc.status["name"] == expected["name"]


@pytest.mark.parametrize(
    ("iban"),
    [
        "DE97765500000008147423",
        " DE 97765500000008147423",
        "DE 97 7655 000 0000 814 74 23",
        "  D E9 7   765   5 0 000 0 0 0  8  1 474  2  3   ",
        "DE977655000 00008147423",
    ],
)
def test_validate_iban_variations(iban, docpath):
    test_input = {"name": "karin steiner", "iban": iban}
    expected = {"valid": True, "name": True, "iban": True}
    _check_values(test_input, expected, docpath)


@pytest.mark.parametrize(
    ("name"),
    [
        "Karin   Steiner",
        "KarinSteiner",
        "Karin steiner",
        "karin Steiner",
        "Karin STEINER",
        "KArIn    StEiner",
        "karinsteiner",
    ],
)
def test_validate_name_variations(name, docpath):
    test_input = {"name": name, "iban": "DE97765500000008147423"}
    expected = {"valid": True, "name": True, "iban": True}
    _check_values(test_input, expected, docpath)


def test_validate_reject_iban(docpath):
    test_input = {"name": "karin steiner", "iban": "DENOTGOOD"}
    expected = {"valid": False, "name": True, "iban": False}
    _check_values(test_input, expected, docpath)


def test_validate_reject_name(docpath):
    test_input = {"name": "Paul Goth", "iban": "DE97765500000008147423"}
    expected = {"valid": False, "name": False, "iban": True}
    _check_values(test_input, expected, docpath)


def test_validate_reject(docpath):
    test_input = {"name": "Paul Goth", "iban": "DE9770008147423"}
    expected = {"valid": False, "name": False, "iban": False}
    _check_values(test_input, expected, docpath)
