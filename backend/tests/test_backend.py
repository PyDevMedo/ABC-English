import pytest
import asyncio
from app.core.security import (
    validate_tripartite_name, validate_phone_number, generate_student_id,
    verify_password, get_password_hash
)
from app.services.pronunciation_service import (
    get_phonemes_for_word, align_and_evaluate_phonemes, evaluate_pronunciation
)
from app.services.curriculum_50 import generate_50_levels

CURRICULUM_50_DATA = generate_50_levels()

def test_tripartite_name_validation():
    # Valid 3-part names
    assert validate_tripartite_name("محمد أحمد علي") is True
    assert validate_tripartite_name("Omar Khaled Hassan") is True
    assert validate_tripartite_name("سارة محمود عبد الرحمن") is True

    # Invalid names (< 3 parts or too short)
    assert validate_tripartite_name("محمد") is False
    assert validate_tripartite_name("محمد أحمد") is False
    assert validate_tripartite_name("") is False
    assert validate_tripartite_name(None) is False

def test_phone_validation():
    assert validate_phone_number("01012345678") == "01012345678"
    assert validate_phone_number("+20 10 1234 5678") == "201012345678"
    assert validate_phone_number("055-123-4567") == "0551234567"
    assert validate_phone_number("abc1234") is None
    assert validate_phone_number("123") is None

def test_student_id_generation():
    stu_id = generate_student_id()
    assert stu_id.startswith("STU-")
    assert len(stu_id) >= 12

def test_password_hashing():
    pwd = "childSecretPassword123"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongPassword", hashed) is False

def test_phonemes_mapping_and_alignment():
    # Test Phonemes for 'ship' -> ['SH', 'IH', 'P']
    p_ship = get_phonemes_for_word("ship")
    assert "SH" in p_ship
    assert "P" in p_ship

    # Test alignment: perfect match
    correct, errors, ratio = align_and_evaluate_phonemes(["SH", "IH", "P"], ["SH", "IH", "P"])
    assert len(correct) == 3
    assert len(errors) == 0
    assert ratio == 1.0

    # Test alignment: missed 'SH' (e.g. child said 'sip' -> S instead of SH)
    correct, errors, ratio = align_and_evaluate_phonemes(["SH", "IH", "P"], ["S", "IH", "P"])
    assert "SH" in errors
    assert ratio < 1.0

def test_curriculum_integrity():
    # Ensure all 50 levels are accurately configured
    assert len(CURRICULUM_50_DATA) == 50
    
    # Check Level 1 (S, A, T, P, I, N)
    l1 = CURRICULUM_50_DATA[0]
    l1_symbols = [x["symbol"] for x in l1["letters"]]
    for sym in ["S", "A", "T", "P", "I", "N"]:
        assert sym in l1_symbols
    assert "Sat" in [w["word"] for w in l1["words"]]
    assert l1["passage"]["title"] == "The Little Pin"
    assert len(l1["sentences"]) >= 3

    # Check Level 5 (SH, CH, TH)
    l5 = CURRICULUM_50_DATA[4]
    l5_symbols = [x["symbol"] for x in l5["letters"]]
    for sym in ["SH", "CH", "TH"]:
        assert sym in l5_symbols
    assert "Ship" in [w["word"] for w in l5["words"]]
    assert l5["passage"]["title"] == "At the Harbor Shop"

    # Check Level 8 (Word Families)
    l8 = CURRICULUM_50_DATA[7]
    assert "Pig" in [w["word"] for w in l8["words"]]
    assert l8["passage"]["title"] == "The Little Bunny"

    # Check Level 15 (Talking with Real People - Milestone)
    l15 = CURRICULUM_50_DATA[14]
    assert l15["level_number"] == 15
    assert "Real People" in l15["title"]
    assert "Speak" in [w["word"] for w in l15["words"]]
    assert l15["passage"]["title"] == "An Inspiring Conversation in London"

    # Check Level 50 (Native Bilingual Fluency - Final Mastery)
    l50 = CURRICULUM_50_DATA[49]
    assert l50["level_number"] == 50
    assert "Mastery" in l50["title"]
    assert l50["passage"]["title"] == "The Odyssey of Fluency: From Phonics to the Stars"
    assert len(CURRICULUM_50_DATA) == 50
