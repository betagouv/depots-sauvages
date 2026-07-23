from backend.stats.anonymizer import (
    anonymize_email,
    anonymize_fake_name,
    anonymize_phone,
    anonymize_text,
    anonymize_user_hash,
    hash_value,
)


def test_hash_value_deterministic():
    val1 = hash_value("Test@Example.com")
    val2 = hash_value("test@example.com")
    assert val1 == val2
    assert len(val1) == 16
    assert hash_value("") == ""


def test_anonymize_user_hash():
    h1 = anonymize_user_hash(42)
    h2 = anonymize_user_hash(42)
    assert h1 == h2
    assert len(h1) == 16
    assert "42" not in h1
    assert anonymize_user_hash(None) == ""


def test_anonymize_email():
    email = "jean.dupont@example.fr"
    anon = anonymize_email(email)
    assert "jean.dupont" not in anon
    assert "example.fr" not in anon
    assert anon.startswith("anon_")
    assert anon.endswith("@anonymized.local")
    assert anonymize_email("") == ""


def test_anonymize_phone():
    assert anonymize_phone("0612345678") == ""
    assert anonymize_phone("") == ""


def test_anonymize_text():
    assert anonymize_text("Private address line") == "[ANONYMIZED]"
    assert anonymize_text("") == ""


def test_anonymize_fake_name_deterministic():
    fake1 = anonymize_fake_name("Dupont", record_id=123)
    fake2 = anonymize_fake_name("Dupont", record_id=123)
    assert fake1 == fake2
    assert fake1 != "Dupont"
    assert anonymize_fake_name("") == ""
