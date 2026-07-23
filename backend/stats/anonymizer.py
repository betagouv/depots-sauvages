import hashlib
from faker import Faker

fake = Faker("fr_FR")


def hash_value(value: str, salt: str = "ds_stats_salt_v1") -> str:
    if not value:
        return ""
    return hashlib.sha256(f"{salt}:{value.strip().lower()}".encode("utf-8")).hexdigest()[:16]


def anonymize_user_hash(user_id: int | str | None, record_id: int | str = None) -> str:
    if user_id is None or user_id == "":
        return ""
    return hash_value(str(user_id), salt="ds_user_hash_v1")


def anonymize_email(email: str, record_id: int | str = None) -> str:
    if not email or not email.strip():
        return ""
    h = hash_value(email)
    return f"anon_{h}@anonymized.local"


def anonymize_phone(phone: str, record_id: int | str = None) -> str:
    if not phone or not phone.strip():
        return ""
    return ""


def anonymize_text(text: str, record_id: int | str = None) -> str:
    if not text or not text.strip():
        return ""
    return "[ANONYMIZED]"


def anonymize_fake_name(name: str, record_id: int | str = None) -> str:
    if not name or not name.strip():
        return ""
    if record_id is not None:
        Faker.seed(hash(f"{record_id}:{name}"))
        return fake.last_name()
    return "[ANONYMIZED]"
