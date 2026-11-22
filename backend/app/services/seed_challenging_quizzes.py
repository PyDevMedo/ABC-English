# Script to generate rich, challenging, diverse quiz questions for all 50 levels
# Each question has 4 close, challenging options (minimal pairs, semantic distractors, grammar traps)

import sqlite3
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.services.curriculum_50 import generate_50_levels

def build_challenging_quiz_questions(level_item):
    lvl = level_item["level_number"]
    words = level_item.get("words", [])
    w1 = words[0]["word"] if words else "Learn"
    w2 = words[1]["word"] if len(words) > 1 else "Read"
    w3 = words[2]["word"] if len(words) > 2 else "Speak"
    w1_ar = words[0]["translation_ar"] if words else "يتعلم"

    questions = []

    # -------------------------------------------------------------
    # Question 1: Audio Discrimination / Minimal Pairs (الاستماع الدقيق)
    # -------------------------------------------------------------
    minimal_pairs_map = {
        1: ("Sit", ["Sit", "Sat", "Set", "Hit"]),
        2: ("Cat", ["Cat", "Cot", "Cut", "Bat"]),
        3: ("Bed", ["Bed", "Bad", "Bid", "Bud"]),
        4: ("Box", ["Box", "Fox", "Pox", "Six"]),
        5: ("Ship", ["Ship", "Sheep", "Shop", "Chip"]),
        6: ("Moon", ["Moon", "Noon", "Soon", "Mood"]),
        7: ("Boat", ["Boat", "Boot", "Bait", "Coat"]),
        8: ("Pig", ["Pig", "Peg", "Pug", "Big"]),
        9: ("Look", ["Look", "Took", "Book", "Cook"]),
        10: ("Story", ["Story", "Store", "Star", "Storm"]),
        11: ("Friend", ["Friend", "Field", "Front", "Fiend"]),
        12: ("Brother", ["Brother", "Bother", "Mother", "Father"]),
        13: ("Clock", ["Clock", "Block", "Flock", "Lock"]),
        14: ("Water", ["Water", "Waiter", "Winter", "Wafer"]),
        15: ("Speak", ["Speak", "Speech", "Speed", "Spoke"]),
        16: ("Where", ["Where", "There", "Were", "Wear"]),
        17: ("Shirt", ["Shirt", "Skirt", "Short", "Shift"]),
        18: ("Sunny", ["Sunny", "Funny", "Bunny", "Money"]),
        19: ("Excited", ["Excited", "Existed", "Exited", "Expected"]),
        20: ("Listen", ["Listen", "Lesson", "Lessen", "Little"]),
        21: ("Past", ["Past", "Passed", "Fast", "Last"]),
        22: ("Future", ["Future", "Feature", "Figure", "Failure"]),
        23: ("Travel", ["Travel", "Trouble", "Traveled", "Trail"]),
        24: ("Hobby", ["Hobby", "Happy", "Heavy", "Hubby"]),
        25: ("Health", ["Health", "Wealth", "Heal", "Help"]),
        26: ("Nature", ["Nature", "Mature", "Nation", "Notice"]),
        27: ("Technology", ["Technology", "Technique", "Technical", "Terminology"]),
        28: ("School", ["School", "Scholar", "Schedule", "Scheme"]),
        29: ("Music", ["Music", "Magic", "Museum", "Musician"]),
        30: ("Opinion", ["Opinion", "Option", "Operation", "Opponent"]),
        31: ("Agree", ["Agree", "Argue", "Degree", "Eager"]),
        32: ("Problem", ["Problem", "Program", "Promise", "Project"]),
        33: ("Cause", ["Cause", "Course", "Clause", "Case"]),
        34: ("Describe", ["Describe", "Prescribe", "Inscribe", "Subscribe"]),
        35: ("Culture", ["Culture", "Custom", "Current", "Curtain"]),
        36: ("Meeting", ["Meeting", "Meaning", "Melting", "Managing"]),
        37: ("Interview", ["Interview", "Overview", "Review", "Intervene"]),
        38: ("Formal", ["Formal", "Former", "Format", "Formula"]),
        39: ("Idiom", ["Idiom", "Ideal", "Idiot", "Item"]),
        40: ("Phraze", ["Phrase", "Praise", "Phase", "Prize"]),
        41: ("Debate", ["Debate", "Defeat", "Decide", "Delate"]),
        42: ("Negotiate", ["Negotiate", "Navigate", "Nominate", "Notice"]),
        43: ("Analyze", ["Analyze", "Analog", "Anatomy", "Anchor"]),
        44: ("Persuade", ["Persuade", "Pursue", "Pervade", "Presume"]),
        45: ("Leadership", ["Leadership", "Leader", "Relationship", "Hardship"]),
        46: ("Fluent", ["Fluent", "Fluid", "Frequent", "Fluent"]),
        47: ("Spontaneous", ["Spontaneous", "Simultaneous", "Continuous", "Courageous"]),
        48: ("Nuance", ["Nuance", "Nuisance", "Notice", "Nurture"]),
        49: ("Articulate", ["Articulate", "Accurate", "Article", "Activate"]),
        50: ("Mastery", ["Mastery", "Mystery", "Monster", "Muster"])
    }

    target_audio_word, minimal_options = minimal_pairs_map.get(lvl, (w1, [w1, w2, w3, "Learn"]))
    q1 = {
        "question_type": "listen_select",
        "question_text": "🎧 استمع جيداً إلى المقطع الصوتي التالي، ثم اختر الكلمة المطابقة له بدقة من بين الكلمات المتقاربة:",
        "audio_url": f"/static/audio/{target_audio_word.lower()}.mp3",
        "audio_text": target_audio_word,
        "options_json": minimal_options,
        "correct_answer": target_audio_word
    }
    questions.append(q1)

    # -------------------------------------------------------------
    # Question 2: Close Meaning Discrimination (التمييز الدلالي والمعاني المتقاربة)
    # -------------------------------------------------------------
    close_meaning_map = {
        1: ("ما هو المعنى الدقيق لكلمة 'Sit'؟", ["يجلس في مكانه", "يقف باعتدال", "يستلقي للراحة", "يتحرك للأمام"], "يجلس في مكانه"),
        2: ("ما هو المعنى الدقيق لكلمة 'Dog'؟", ["حيوان أليف وفيّ", "قطة صغيرة ناعمة", "ثعلب بري سريع", "أرنب أبيض لطيف"], "حيوان أليف وفيّ"),
        3: ("ما هو المعنى الدقيق لكلمة 'Bed'؟", ["سرير مريح للنوم", "أريكة للجلوس", "سجادة للأرضية", "طاولة خشبية"], "سرير مريح للنوم"),
        4: ("ما هو المعنى الدقيق لكلمة 'Fox'؟", ["ثعلب بري ماكر", "ذئب رمادي كبير", "كلب صيد سريع", "قط بري شرس"], "ثعلب بري ماكر"),
        5: ("ما هو المعنى الدقيق لكلمة 'Ship'؟", ["سفينة بحرية ضخمة", "قارب صيد صغير", "طائرة نفاثة سريعة", "غواصة تحت الماء"], "سفينة بحرية ضخمة"),
        6: ("ما هو المعنى الدقيق لكلمة 'Moon'؟", ["قمر مضيء في السماء ليلاً", "شمس ساطعة في الظهيرة", "نجم بعيد متلألئ", "سحابة بيضاء ممطرة"], "قمر مضيء في السماء ليلاً"),
        7: ("ما هو المعنى الدقيق لكلمة 'Rain'؟", ["قطرات ماء متساقطة من السحب", "رياح عاصفة قوية", "ثلج أبيض متراكم", "ضباب كثيف في الصباح"], "قطرات ماء متساقطة من السحب"),
        8: ("ما هو المعنى الدقيق لكلمة 'Hop'؟", ["يقفز قفزة قصيرة للأعلى", "يجري مسرعاً في الحقل", "يزحف ببطء على الأرض", "يمشي بهدوء وحذر"], "يقفز قفزة قصيرة للأعلى"),
        9: ("ما هو المعنى الدقيق لكلمة 'Help'؟", ["يمد يد العون والمساعدة", "يطلب النصيحة والإرشاد", "يتعلم بمفرده بهدوء", "يشارك في اللعب فقط"], "يمد يد العون والمساعدة"),
        10: ("ما هو المعنى الدقيق لكلمة 'Read'؟", ["يقرأ ويتفحص الكلمات المكتوبة", "يكتب بالقلم في الدفتر", "يستمع لصوت المعلم", "يرسم لوحة فنية"], "يقرأ ويتفحص الكلمات المكتوبة"),
        11: ("ما هو المعنى الدقيق لكلمة 'Friend'؟", ["صديق مخلص ومقرب", "زميل عابر في العمل", "شخص غريب نلتقيه", "معلم في الفصل"], "صديق مخلص ومقرب"),
        12: ("ما هو المعنى الدقيق لكلمة 'Smart'؟", ["ذكي وسريع البديهة والفهم", "طويل القامة ونحيف", "هادئ وقليل الكلام", "كثير المزاح والضحك"], "ذكي وسريع البديهة والفهم"),
        13: ("ما هو المعنى الدقيق لتعبير 'Wake up'؟", ["يستيقظ من نومه في الصباح", "يأوي إلى فراشه ليلاً", "يتناول وجبة الإفطار", "يستعد للخروج للمدرسة"], "يستيقظ من نومه في الصباح"),
        14: ("ما هو المعنى الدقيق لكلمة 'Order' في المطعم؟", ["يطلب وجبته أو مشروبه بأدب", "يدفع الحساب المالي", "يحجز طاولة مسبقاً", "يشكر النادل على الخدمة"], "يطلب وجبته أو مشروبه بأدب"),
        15: ("ما هو المعنى الدقيق لكلمة 'Speak' في التواصل؟", ["يتحدث ويعبر بطلاقة صوتياً", "يستمع للآخرين بصمت", "يكتب رسالة نصية", "يفكر في الفكرة داخلياً"], "يتحدث ويعبر بطلاقة صوتياً"),
        16: ("ما هو المعنى الدقيق لتعبير 'Turn right'؟", ["ينعطف باتجاه اليمين", "يتجه نحو اليسار مباشرة", "يواصل السير للأمام مستقيماً", "يعود إلى الخلف أدراجه"], "ينعطف باتجاه اليمين"),
        17: ("ما هو المعنى الدقيق لكلمة 'Price' عند الشراء؟", ["المبلغ المالي المطلوب لشراء السلعة", "مقاس وحجم قطعة الملابس", "لون ونوعية القماش المصنوع", "اسم المتجر والماركة"], "المبلغ المالي المطلوب لشراء السلعة"),
        18: ("ما هو المعنى الدقيق لكلمة 'Warm' في وصف الطقس؟", ["دافئ معتدل ومريح للجسم", "شديد الحرارة وحارق", "بارد وقارس البرودة", "عاصف ومحمل بالغبار"], "دافئ معتدل ومريح للجسم"),
        19: ("ما هو المعنى الدقيق لكلمة 'Confident'؟", ["واثق من نفسه وقدراته تماماً", "متردد ويخشى الخطأ", "متعب ويفضل الراحة", "غاضب من النتيجة"], "واثق من نفسه وقدراته تماماً"),
        20: ("ما هو المعنى الدقيق لكلمة 'Fluent' في اللغة؟", ["يتحدث بطلاقة وسلاسة دون تعثر", "يحفظ القواعد النظرية فقط", "يترجم في عقله قبل الحديث", "يتحدث ببطء وتردد مستمر"], "يتحدث بطلاقة وسلاسة دون تعثر"),
    }

    if lvl in close_meaning_map:
        q_text, opts, ans = close_meaning_map[lvl]
    else:
        # Default close meaning template for higher levels
        q_text = f"ما هو المعنى الأدق لكلمة '{w1}' في السياق اللغوي المتقدم؟"
        opts = [
            f"{w1_ar} بدقة واحترافية",
            f"عكس معنى {w1_ar} تماماً",
            f"مرادف فرعي غير دقيق لـ {w1_ar}",
            f"وصف عام غير مرتبط بسياق {w1_ar}"
        ]
        ans = opts[0]

    q2 = {
        "question_type": "word_match",
        "question_text": q_text,
        "audio_url": None,
        "audio_text": None,
        "options_json": opts,
        "correct_answer": ans
    }
    questions.append(q2)

    # -------------------------------------------------------------
    # Question 3: Contextual Sentence & Close Fill-in-the-Blank (سياق الجملة المتقارب)
    # -------------------------------------------------------------
    sentence_map = {
        1: ("I like to ______ quietly on the chair.", ["sit", "sat", "site", "seat"], "sit"),
        2: ("The hungry little ______ drank all the milk from the bowl.", ["cat", "cot", "cut", "kit"], "cat"),
        3: ("After a tiring day, I rested on my comfortable ______.", ["bed", "bad", "red", "bug"], "bed"),
        4: ("The clever ______ hid quietly behind the large tree.", ["fox", "box", "van", "jet"], "fox"),
        5: ("The captain sailed the giant ______ safely into the harbor.", ["ship", "chip", "shop", "chat"], "ship"),
        6: ("At night, the silver ______ illuminated the whole sky.", ["moon", "noon", "soon", "mood"], "moon"),
        7: ("We took our wooden ______ for a ride across the calm river.", ["boat", "coat", "car", "star"], "boat"),
        8: ("The happy little bunny can ______ gracefully across the grass.", ["hop", "top", "mop", "pop"], "hop"),
        9: ("Could you kindly ______ me carry this heavy luggage?", ["help", "hold", "hope", "hear"], "help"),
        10: ("I enjoy ______ short stories before going to sleep.", ["reading", "riding", "reding", "ready"], "reading"),
        11: ("It was really nice to ______ you this pleasant morning.", ["meet", "meat", "mete", "melt"], "meet"),
        12: ("My older ______ always supports and guides me with care.", ["brother", "bother", "mother", "father"], "brother"),
        13: ("The antique ______ in the living room chimed twelve times.", ["clock", "cloak", "click", "clerk"], "clock"),
        14: ("I always prefer to drink fresh ______ with my meals.", ["water", "waiter", "winter", "wafer"], "water"),
        15: ("When you have a conversation, it is important to listen and ______ clearly.", ["speak", "speech", "spoke", "speed"], "speak"),
        16: ("Excuse me, could you tell me ______ the public library is?", ["where", "were", "wear", "there"], "where"),
        17: ("He bought a clean white ______ for the school ceremony.", ["shirt", "skirt", "short", "shift"], "shirt"),
        18: ("Tomorrow's forecast predicts a bright and ______ afternoon.", ["sunny", "sun", "sunned", "sunning"], "sunny"),
        19: ("We are extremely ______ about our upcoming vacation to London!", ["excited", "exciting", "excite", "exited"], "excited"),
        20: ("Engaging in daily English talk makes you sound natural and ______.", ["fluent", "fluid", "flying", "flow"], "fluent")
    }

    if lvl in sentence_map:
        s_text, s_opts, s_ans = sentence_map[lvl]
        q_text3 = f"أكمل الفراغ في الجملة التالية بالكلمة الصحيحة دلالياً ونحوياً:\n\"{s_text}\""
    else:
        q_text3 = f"أكمل الجملة التالية بالصيغة التعبيرية الأنسب سياقياً:\n\"Regular practice with '{w1}' helps you become more ______.\""
        s_opts = ["fluent and natural", "fluent and slowly", "fluency and native", "fluently and shy"]
        s_ans = "fluent and natural"

    q3 = {
        "question_type": "fill_blank",
        "question_text": q_text3,
        "audio_url": None,
        "audio_text": None,
        "options_json": s_opts,
        "correct_answer": s_ans
    }
    questions.append(q3)

    # -------------------------------------------------------------
    # Question 4: Conversational Challenge / Phonics Trap (المحادثة والتحدي التفاعلي)
    # -------------------------------------------------------------
    stage_challenge_map = {
        1: ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /æ/ (مثل صوت حرف A في Apple)؟", ["Sat", "Sit", "Pin", "Tin"], "Sat"),
        2: ("أي من الكلمات التالية تنتهي بصوت الحرف /g/ الانفجاري النقي؟", ["Dog", "Dot", "Doc", "Don"], "Dog"),
        3: ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /e/ (مثل صوت حرف E في Elephant)؟", ["Bed", "Bad", "Bid", "Bud"], "Bed"),
        4: ("أي من الكلمات التالية تنتهي بصوت الحرفين المركبين /ks/ المكتوبين بـ X؟", ["Box", "Bog", "Bob", "Bot"], "Box"),
        5: ("أي من الكلمات التالية تبدأ بصوت /tʃ/ المهموس (مثل بداية كلمة Chair و Chocolate)؟", ["Chip", "Ship", "This", "Thin"], "Chip"),
        6: ("أي من الكلمات التالية تحتوي على صوت /iː/ الممدود (Long EE sound)؟", ["See", "Set", "Sit", "Sat"], "See"),
        7: ("أي من الكلمات التالية تحتوي على صوت /ɑː/ المفخم (R-controlled vowel AR)؟", ["Star", "Stir", "Store", "Steer"], "Star"),
        8: ("أي من الكلمات التالية تنتمي إلى عائلة القافية الصوتية (-at family)؟", ["Hat", "Hot", "Hit", "Hut"], "Hat"),
        9: ("أي كلمة من الكلمات البصرية تعبر عن تقديم المساعدة لشخص آخر؟", ["Help", "Look", "Play", "Come"], "Help"),
        10: ("ما هو الترتيب الصحيح لتكوين جملة إنجليزية مفهومة؟", ["I read my book.", "Read I book my.", "My book read I.", "I book read my."], "I read my book."),
        11: ("إذا قال لك زميلك: 'Nice to meet you!'، فما هو الرد الأكثر تهذيباً وألفة؟", ["Nice to meet you too!", "Yes, I meet you.", "You are welcome.", "Good night, friend."], "Nice to meet you too!"),
        12: ("كيف تصف أختك بأنها ذكية وتساعد الآخرين دائماً بجملة صحيحة؟", ["My sister is smart and helpful.", "My sister smart helpful is.", "Sister my is help smart.", "My sister does smart."], "My sister is smart and helpful."),
        13: ("إذا سألك شخص: 'What time is it now?'، فما هي الإجابة النموذجية الصحيحة؟", ["It is eight o'clock.", "It is clock eight.", "Time is eight clock.", "I have eight time."], "It is eight o'clock."),
        14: ("ما هي الصيغة الأكثر أدباً ولباقة لطلب كوب ماء في المطعم؟", ["Can I have a glass of water, please?", "Give me water now.", "I want water quickly.", "Water is for me."], "Can I have a glass of water, please?"),
        15: ("سألك شخص أجنبي في محادثة: 'Where are you from?'، فما هي الإجابة السليمة نحوياً وطبيعياً؟", ["I am from Egypt.", "I am in Egypt.", "I come to Egypt.", "I living from Egypt."], "I am from Egypt."),
        16: ("إذا سألك سائح عن مكان المتحف، وأردت إخباره أن ينعطف يميناً، ماذا تقول؟", ["Turn right at the corner.", "Turn the right corner.", "Go to right turn.", "Make right corner."], "Turn right at the corner."),
        17: ("عند السؤال عن سعر قميص في متجر الملابس، ما هو السؤال الصحيح؟", ["How much is this shirt?", "How many is this shirt?", "What price this shirt have?", "How cost this shirt is?"], "How much is this shirt?"),
        18: ("كيف تعبر عن أن الطقس اليوم مشمس وجميل بطريقة طبيعية؟", ["It is sunny and pleasant today.", "The sun is today making.", "Weather has sunny nice.", "It makes sun outside."], "It is sunny and pleasant today."),
        19: ("كيف تعبر عن شعورك بالحماس الشديد للمشاركة في مسابقة التحدث؟", ["I am really excited to participate!", "I have excited to speech.", "I feel excite competition.", "Exciting is me today."], "I am really excited to participate!"),
        20: ("ما هي أفضل استراتيجية للتحدث بطلاقة مع الناس دون خوف؟", ["Practice daily without worrying about minor errors.", "Never talk until your accent is 100% perfect.", "Memorize huge grammar books only.", "Avoid talking with native speakers."], "Practice daily without worrying about minor errors.")
    }

    if lvl in stage_challenge_map:
        c_text, c_opts, c_ans = stage_challenge_map[lvl]
    elif lvl <= 35:
        c_text = f"في سياق المحادثة المتقدمة (Level {lvl})، أي عبارة تمثل التعبير الطبيعي الأكثر دقة؟"
        c_opts = [
            f"I truly appreciate your perspective on {w1.lower()}.",
            f"I appreciate perspective on {w1.lower()} you.",
            f"Your perspective is appreciating {w1.lower()}.",
            f"Appreciation is my view for {w1.lower()}."
        ]
        c_ans = c_opts[0]
    else:
        c_text = f"في مستوى الطلاقة والإتقان الاحترافي (Level {lvl})، ما هو التعبير الاصطلاحي الأكثر بلاغة؟"
        c_opts = [
            f"To articulate ideas with precision and clarity",
            f"To articulate ideas with vague words",
            f"To speak quickly without clear meaning",
            f"To translate literally from native language"
        ]
        c_ans = c_opts[0]

    q4 = {
        "question_type": "phoneme_or_dialogue",
        "question_text": c_text,
        "audio_url": None,
        "audio_text": None,
        "options_json": c_opts,
        "correct_answer": c_ans
    }
    questions.append(q4)

    return questions

def update_database_quizzes():
    db_path = "english_journey.db"
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("SELECT id, level_id FROM quizzes ORDER BY level_id;")
    quizzes = cur.fetchall()

    curriculum = generate_50_levels()
    curriculum_by_lvl = {item["level_number"]: item for item in curriculum}

    total_inserted = 0
    for quiz_id, lvl_num in quizzes:
        lvl_item = curriculum_by_lvl.get(lvl_num)
        if not lvl_item:
            continue

        # Delete old questions for this quiz
        cur.execute("DELETE FROM quiz_questions WHERE quiz_id = ?;", (quiz_id,))

        # Build 4 new challenging questions
        questions = build_challenging_quiz_questions(lvl_item)

        for q in questions:
            cur.execute("""
                INSERT INTO quiz_questions (quiz_id, question_type, question_text, audio_url, options_json, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (
                quiz_id,
                q["question_type"],
                q["question_text"],
                q["audio_url"],
                json.dumps(q["options_json"], ensure_ascii=False),
                q["correct_answer"]
            ))
            total_inserted += 1

    con.commit()
    con.close()
    print(f"Successfully generated and inserted {total_inserted} challenging questions across {len(quizzes)} quizzes!")

if __name__ == "__main__":
    update_database_quizzes()
