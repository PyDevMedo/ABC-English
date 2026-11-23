"""
Full Curriculum Seeder for ABC English.
Populates all 50 levels with:
1. Level metadata (title, subtitle, description, icon)
2. Primary Lesson per level
3. 6 Lesson Sections per lesson:
   - 'intro': Lesson story and pedagogical objective in Arabic
   - 'phonics': Sound breakdown, phonemes, and letters
   - 'words': Target vocabulary with definitions and phonemes breakdown
   - 'sentences': Contextual sentence patterns with Arabic translation
   - 'reading': Full passage/article (title, English text, Arabic translation, audio)
   - 'pronunciation': AI pronunciation lab targets
4. Words table populated with all target words per level
5. Real educational Assignment prompt tailored to level type (handwriting / essay)
6. Quizzes link

Preserves existing Users, StudentProfiles, TeacherAccounts, and Student progress.
"""

import os
import sys
import json
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(ROOT_DIR, "english_journey.db")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.services.curriculum_50 import generate_50_levels

def seed_full_50_curriculum():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    levels_data = generate_50_levels()
    print(f"Loaded {len(levels_data)} levels from curriculum generator.")

    # 1. Clear curriculum tables while keeping users, student_profiles, submissions, progress
    c.execute("DELETE FROM words")
    c.execute("DELETE FROM lesson_sections")
    c.execute("DELETE FROM lessons")
    c.execute("DELETE FROM assignments")
    c.execute("DELETE FROM levels")
    c.execute("DELETE FROM quizzes")
    c.execute("DELETE FROM quiz_questions")

    print("Cleared previous curriculum rows. Inserting 50 authentic progressive levels...")

    for item in levels_data:
        lvl_num = item["level_number"]
        title = item["title"]
        subtitle = item["subtitle"]
        description = item["description"]
        icon = item.get("icon", "🌟")
        
        # Insert Level
        c.execute("""
            INSERT INTO levels (id, level_number, title, subtitle, description, icon, min_passing_score, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 80, 1)
        """, (lvl_num, lvl_num, title, subtitle, description, icon))

        # Insert Lesson
        c.execute("""
            INSERT INTO lessons (id, level_id, lesson_number, title, description, order_index)
            VALUES (?, ?, 1, ?, ?, 1)
        """, (lvl_num, lvl_num, f"Lesson 1: {subtitle}", description))
        lesson_id = lvl_num

        # Lesson Sections
        # 1. Intro
        s_intro_json = json.dumps({"text_ar": item.get("intro_ar", description)})
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'intro', 'المقدمة والهدف التعليمي', 'Welcome & Objective', ?, 1)
        """, (lesson_id, s_intro_json))

        # 2. Phonics / Sounds / Rhetoric Focus
        s_phonics_json = json.dumps({"letters": item.get("letters", [])})
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'phonics', 'أصوات ومفاتيح المستوى', 'Phonics & Core Keys', ?, 2)
        """, (lesson_id, s_phonics_json))

        # 3. Words
        s_words_json = json.dumps({"words": item.get("words", [])})
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'words', 'تركيب المفردات اللغوية', 'Vocabulary Mastery', ?, 3)
        """, (lesson_id, s_words_json))

        # 4. Sentences
        s_sentences_json = json.dumps({
            "sentences": item.get("sentences", []),
            "sight_words": item.get("sight_words", [])
        })
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'sentences', 'بناء الجمل والتراكيب', 'Sentence Construction', ?, 4)
        """, (lesson_id, s_sentences_json))

        # 5. Reading Passage / Article (True Progressive Reading: Stories to Articles & Debates)
        passage = item.get("passage", {
            "title": f"Reading Practice - Level {lvl_num}",
            "text": "Practice reading this text carefully.",
            "translation_ar": "اقرأ هذا النص بعناية وفهم."
        })
        s_reading_json = json.dumps({
            "passage": passage,
            "level_type": item.get("level_type", "reading")
        })
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'reading', 'قراءة النص / المقال والتدبر', 'Reading Passage & Article', ?, 5)
        """, (lesson_id, s_reading_json))

        # 6. AI Pronunciation Lab
        practice_words = [w["word"] for w in item.get("words", [])]
        practice_sentences = [s["text"] for s in item.get("sentences", [])]
        s_lab_json = json.dumps({
            "practice_words": practice_words,
            "practice_sentences": practice_sentences
        })
        c.execute("""
            INSERT INTO lesson_sections (lesson_id, section_type, title_ar, title_en, content_json, order_index)
            VALUES (?, 'pronunciation', 'مختبر النطق مع المدرس الذكي', 'AI Pronunciation Lab', ?, 6)
        """, (lesson_id, s_lab_json))

        # Populate Words table
        for w in item.get("words", []):
            c.execute("""
                INSERT INTO words (level_id, lesson_id, word, phonemes_breakdown, translation_ar, audio_url, is_sight_word)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """, (lvl_num, lesson_id, w["word"], w.get("phonemes", w["word"]), w.get("translation_ar", ""), f"/static/audio/{w['word'].lower()}.mp3"))

        for sw in item.get("sight_words", []):
            c.execute("""
                INSERT INTO words (level_id, lesson_id, word, phonemes_breakdown, translation_ar, is_sight_word)
                VALUES (?, ?, ?, ?, 'كلمة بصرية أساسية', 1)
            """, (lvl_num, lesson_id, sw, sw))

        # Populate Assignment tailored to stage
        hw_words = practice_words[:4]
        hw_sentences = practice_sentences[:2]
        prompt = item.get("homework_prompt", f"اكتب كلمات الدرس في كراسة اللغة الإنجليزية وارفع صورة واضحة.")
        
        c.execute("""
            INSERT INTO assignments (level_id, title, description, instructions_ar, assignment_type, target_words_json, target_sentences_json)
            VALUES (?, ?, ?, ?, 'handwriting_photo', ?, ?)
        """, (
            lvl_num,
            f"واجب كتابة وتطبيق {title}",
            f"كتابة وتطبيق محتوى {subtitle} في الدفتر وتصوير الصفحة.",
            prompt,
            json.dumps(hw_words),
            json.dumps(hw_sentences)
        ))

        # Populate Quiz container
        c.execute("""
            INSERT INTO quizzes (id, level_id, lesson_id, title, passing_score, time_limit_minutes)
            VALUES (?, ?, ?, ?, 80, 15)
        """, (lvl_num, lvl_num, lesson_id, f"اختبار إتقان {title}"))

    conn.commit()
    conn.close()
    print("Successfully seeded all 50 levels and lessons with Reading Passage sections!")

if __name__ == "__main__":
    seed_full_50_curriculum()
