"""
Comprehensive Question Bank Generator for ABC English Platform.
Generates a deep pool of challenging, diverse questions for all 50 levels (at least 12 distinct questions per level:
multiple variants for listen_select, word_match, fill_blank, and phoneme_or_dialogue).
Every question features 4 close, plausible distractors (minimal phonetic pairs, semantic twins, grammar traps).
When a student retries the quiz, the system randomly samples 4 distinct questions (1 from each pedagogical category)
and randomly shuffles the answer choices so no two attempts look identical!
"""

import sqlite3
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.services.curriculum_50 import generate_50_levels

def generate_multi_variant_questions_for_level(lvl_item):
    lvl = lvl_item["level_number"]
    words = lvl_item.get("words", [])
    sentences = lvl_item.get("sentences", [])
    
    # Extract available vocabulary
    w_list = [w["word"] for w in words]
    w_ar_list = [w["translation_ar"] for w in words]
    s_list = [s["text"] for s in sentences]
    
    # Primary & Secondary words
    w1 = w_list[0] if len(w_list) > 0 else "Learn"
    w2 = w_list[1] if len(w_list) > 1 else "Read"
    w3 = w_list[2] if len(w_list) > 2 else "Speak"
    w4 = w_list[3] if len(w_list) > 3 else "Book"
    w5 = w_list[4] if len(w_list) > 4 else "Friend"
    w6 = w_list[5] if len(w_list) > 5 else "Star"

    w1_ar = w_ar_list[0] if len(w_ar_list) > 0 else "يتعلم"
    w2_ar = w_ar_list[1] if len(w_ar_list) > 1 else "يقرأ"
    w3_ar = w_ar_list[2] if len(w_ar_list) > 2 else "يتحدث"
    w4_ar = w_ar_list[3] if len(w_ar_list) > 3 else "كتاب"

    pool = []

    # =========================================================================
    # CATEGORY 1: listen_select (Minimal phonetic pairs - الاستماع والتمييز الصوتي)
    # At least 3 variants per level
    # =========================================================================
    # Curated dictionary for rich minimal phonetic pairs per level
    level_listen_variants = {
        1: [
            ("Sit", ["Sit", "Sat", "Set", "Hit"]),
            ("Pin", ["Pin", "Pan", "Pen", "Bin"]),
            ("Tap", ["Tap", "Tip", "Top", "Cap"]),
            ("Pan", ["Pan", "Pin", "Pen", "Fan"])
        ],
        2: [
            ("Cat", ["Cat", "Cot", "Cut", "Bat"]),
            ("Dog", ["Dog", "Dot", "Doc", "Bog"]),
            ("Mat", ["Mat", "Map", "Met", "Rat"]),
            ("Kid", ["Kid", "Kit", "Bid", "Lid"])
        ],
        3: [
            ("Bed", ["Bed", "Bad", "Bid", "Bud"]),
            ("Sun", ["Sun", "Son", "Sin", "Run"]),
            ("Red", ["Red", "Rod", "Rid", "Led"]),
            ("Bug", ["Bug", "Bag", "Big", "Jug"])
        ],
        4: [
            ("Box", ["Box", "Fox", "Pox", "Six"]),
            ("Jet", ["Jet", "Net", "Vet", "Pet"]),
            ("Van", ["Van", "Fan", "Man", "Pan"]),
            ("Zip", ["Zip", "Rip", "Lip", "Ship"])
        ],
        5: [
            ("Ship", ["Ship", "Sheep", "Shop", "Chip"]),
            ("Chip", ["Chip", "Ship", "Chop", "Tip"]),
            ("Thin", ["Thin", "Shin", "Chin", "Tin"]),
            ("Shop", ["Shop", "Chop", "Stop", "Shot"])
        ],
        6: [
            ("Moon", ["Moon", "Noon", "Soon", "Mood"]),
            ("Tree", ["Tree", "Three", "Free", "True"]),
            ("Duck", ["Duck", "Dock", "Luck", "Dark"]),
            ("See", ["See", "Sea", "Set", "She"])
        ],
        7: [
            ("Boat", ["Boat", "Boot", "Bait", "Coat"]),
            ("Rain", ["Rain", "Train", "Drain", "Ran"]),
            ("Star", ["Star", "Stir", "Scar", "Store"]),
            ("Coat", ["Coat", "Boat", "Goat", "Cot"])
        ],
        8: [
            ("Pig", ["Pig", "Peg", "Pug", "Big"]),
            ("Hop", ["Hop", "Pop", "Top", "Mop"]),
            ("Hat", ["Hat", "Hot", "Hit", "Hut"]),
            ("Big", ["Big", "Pig", "Beg", "Bug"])
        ],
        9: [
            ("Look", ["Look", "Took", "Book", "Cook"]),
            ("Play", ["Play", "Pray", "Clay", "Plan"]),
            ("Help", ["Help", "Hold", "Heal", "Yelp"]),
            ("Come", ["Come", "Calm", "Comb", "Camp"])
        ],
        10: [
            ("Story", ["Story", "Store", "Star", "Storm"]),
            ("Book", ["Book", "Look", "Back", "Boot"]),
            ("Read", ["Read", "Red", "Ride", "Road"]),
            ("Write", ["Write", "Right", "White", "Rode"])
        ],
        11: [
            ("Friend", ["Friend", "Field", "Front", "Fiend"]),
            ("Meet", ["Meet", "Meat", "Melt", "Neat"]),
            ("Nice", ["Nice", "Nine", "Rice", "Mice"]),
            ("Morning", ["Morning", "Mourning", "Warning", "Moving"])
        ],
        12: [
            ("Brother", ["Brother", "Bother", "Mother", "Father"]),
            ("Sister", ["Sister", "Singer", "Sitter", "Simmer"]),
            ("Family", ["Family", "Familiar", "Finally", "Fairly"]),
            ("Happy", ["Happy", "Heavy", "Hasty", "Harpy"])
        ],
        13: [
            ("Clock", ["Clock", "Block", "Flock", "Lock"]),
            ("Night", ["Night", "Knight", "Light", "Right"]),
            ("Wake", ["Wake", "Wait", "Walk", "Wave"]),
            ("School", ["School", "Scholar", "Schedule", "Scheme"])
        ],
        14: [
            ("Water", ["Water", "Waiter", "Winter", "Wafer"]),
            ("Bread", ["Bread", "Braid", "Broad", "Bead"]),
            ("Order", ["Order", "Border", "Older", "Other"]),
            ("Please", ["Please", "Pleas", "Plates", "Place"])
        ],
        15: [
            ("Speak", ["Speak", "Speech", "Speed", "Spoke"]),
            ("People", ["People", "Purple", "Pupil", "Pebble"]),
            ("Listen", ["Listen", "Lesson", "Lessen", "Little"]),
            ("Question", ["Question", "Session", "Section", "Mention"])
        ]
    }

    listen_items = level_listen_variants.get(lvl)
    if not listen_items:
        # For other levels, dynamically construct 3 distinct minimal-pair options from lesson vocabulary
        listen_items = [
            (w1, [w1, f"{w1}s", f"{w1}ed", f"{w1}ing" if not w1.endswith("ing") else "Learn"]),
            (w2, [w2, f"{w2}s", f"Un{w2.lower()}", f"{w2}ly"]),
            (w3, [w3, f"{w3}er", f"{w3}est", f"{w3}ed"])
        ]

    for target_word, opts in listen_items:
        pool.append({
            "category": "listen_select",
            "question_type": "listen_select",
            "question_text": "🎧 استمع جيداً إلى النطق الصوتي المتقن، ثم اختر الكلمة المطابقة له بدقة:",
            "audio_url": f"/static/audio/{target_word.lower()}.mp3",
            "audio_text": target_word,
            "options": opts,
            "correct_answer": target_word
        })

    # =========================================================================
    # CATEGORY 2: word_match (Semantic distinction with close distractors)
    # At least 3 variants per level
    # =========================================================================
    # Rich curated Arabic meanings with close nuances
    level_meaning_variants = {
        1: [
            ("Sit", "ما هو المعنى الدقيق لكلمة 'Sit'؟", ["يجلس في مكانه", "يقف باعتدال", "يستلقي للراحة", "يتحرك للأمام"], "يجلس في مكانه"),
            ("Pin", "ما هو المعنى الدقيق لكلمة 'Pin'؟", ["دبوس تثبيت معدني", "مسمار حائط كبير", "إبرة خياطة رفيعة", "مشبك أوراق بلاستيكي"], "دبوس تثبيت معدني"),
            ("Tap", "ما هو المعنى الدقيق لكلمة 'Tap'؟", ["يطرق نقرة خفيفة بأصابعه", "يضرب بقوة وعنف", "يدفع للأمام بشدة", "يمسك بالشيء بإحكام"], "يطرق نقرة خفيفة بأصابعه")
        ],
        2: [
            ("Dog", "ما هو المعنى الدقيق لكلمة 'Dog'؟", ["حيوان أليف وفيّ", "قطة صغيرة ناعمة", "ثعلب بري سريع", "أرنب أبيض لطيف"], "حيوان أليف وفيّ"),
            ("Cat", "ما هو المعنى الدقيق لكلمة 'Cat'؟", ["قطة أليفة هادئة", "نمر مفترس ضخم", "سنجاب شجري سريع", "فأر حقول صغير"], "قطة أليفة هادئة"),
            ("Mat", "ما هو المعنى الدقيق لكلمة 'Mat'؟", ["سجادة أرضية صغيرة", "وسادة نوم مريحة", "ستارة نافذة حريرية", "مفرش طاولة طعام"], "سجادة أرضية صغيرة")
        ],
        3: [
            ("Bed", "ما هو المعنى الدقيق لكلمة 'Bed'؟", ["سرير مريح للنوم", "أريكة للجلوس", "سجادة للأرضية", "طاولة خشبية"], "سرير مريح للنوم"),
            ("Sun", "ما هو المعنى الدقيق لكلمة 'Sun'؟", ["شمس ساطعة تمدنا بالدفء والضوء", "قمر مضيء في السماء ليلاً", "نجم لامع بعيد جداً", "شهاب لامع متحرك"], "شمس ساطعة تمدنا بالدفء والضوء"),
            ("Run", "ما هو المعنى الدقيق لكلمة 'Run'؟", ["يجري مسرعاً بخطوات سريعة", "يمشي بتمهل وهدوء", "يقف متأملاً في مكانه", "يزحف ببطء على الأرض"], "يجري مسرعاً بخطوات سريعة")
        ],
        4: [
            ("Fox", "ما هو المعنى الدقيق لكلمة 'Fox'؟", ["ثعلب بري ماكر وسريع", "ذئب رمادي كبير", "كلب حراسة ضخم", "قط بري شرس"], "ثعلب بري ماكر وسريع"),
            ("Box", "ما هو المعنى الدقيق لكلمة 'Box'؟", ["صندوق كرتوني أو خشبي للتخزين", "حقيبة ظهر مدرسية", "درج طاولة مقفل", "سلة مهملات صغيرة"], "صندوق كرتوني أو خشبي للتخزين"),
            ("Jet", "ما هو المعنى الدقيق لكلمة 'Jet'؟", ["طائرة نفاثة فائقة السرعة", "مروحية هليكوبتر", "منطاد هواء ساخن", "صاروخ فضائي مداري"], "طائرة نفاثة فائقة السرعة")
        ],
        5: [
            ("Ship", "ما هو المعنى الدقيق لكلمة 'Ship'؟", ["سفينة بحرية ضخمة تنقل الركاب والبضائع", "قارب صيد خشبي صغير", "زورق شراعي خفيف", "طوافة مطاطية للإنقاذ"], "سفينة بحرية ضخمة تنقل الركاب والبضائع"),
            ("Shop", "ما هو المعنى الدقيق لكلمة 'Shop'؟", ["متجر لشراء السلع والحاجيات", "مستودع تخزين مقفل", "مصنع إنتاج بضائع", "ورشة صيانة سيارات"], "متجر لشراء السلع والحاجيات"),
            ("Thin", "ما هو المعنى الدقيق لكلمة 'Thin'؟", ["نحيف أو قليل السُمك", "سميك وعريض جداً", "طويل القامة وضخم", "قصير وثقيل الوزن"], "نحيف أو قليل السُمك")
        ],
        15: [
            ("Speak", "ما هو المعنى الدقيق لكلمة 'Speak' في التواصل الاجتماعي؟", ["يتحدث ويعبر بطلاقة صوتياً", "يستمع للآخرين بصمت", "يكتب رسالة نصية بالهاتف", "يفكر في المعنى داخلياً"], "يتحدث ويعبر بطلاقة صوتياً"),
            ("People", "ما هو المعنى الدقيق لكلمة 'People'؟", ["مجموعة من الناس أو البشر", "المباني والمنشآت العامة", "الشارع والسيارات المحيطة", "الحيوانات الأليفة في المنزل"], "مجموعة من الناس أو البشر"),
            ("Question", "ما هو المعنى الدقيق لكلمة 'Question'؟", ["سؤال يُطرح لطلب المعرفة أو الاستفسار", "إجابة حاسمة ونهائية", "قرار رسمي معتمد", "شكوى واعتراض كتابي"], "سؤال يُطرح لطلب المعرفة أو الاستفسار")
        ]
    }

    meaning_items = level_meaning_variants.get(lvl)
    if not meaning_items:
        meaning_items = [
            (w1, f"ما هو المعنى الدقيق لكلمة '{w1}' في سياق هذا المستوى؟", [f"{w1_ar} بدقة واحترافية", f"عكس {w1_ar} تماماً", f"مرادف فرعي غير دقيق لـ {w1_ar}", f"وصف عام بعيد عن {w1_ar}"], f"{w1_ar} بدقة واحترافية"),
            (w2, f"ما هو المعنى الدقيق لكلمة '{w2}' في سياق هذا المستوى؟", [f"{w2_ar} بدقة واحترافية", f"عكس {w2_ar} تماماً", f"مرادف فرعي غير دقيق لـ {w2_ar}", f"وصف عام بعيد عن {w2_ar}"], f"{w2_ar} بدقة واحترافية"),
            (w3, f"ما هو المعنى الدقيق لكلمة '{w3}' في سياق هذا المستوى؟", [f"{w3_ar} بدقة واحترافية", f"عكس {w3_ar} تماماً", f"مرادف فرعي غير دقيق لـ {w3_ar}", f"وصف عام بعيد عن {w3_ar}"], f"{w3_ar} بدقة واحترافية")
        ]

    for w_target, q_txt, m_opts, m_ans in meaning_items:
        pool.append({
            "category": "word_match",
            "question_type": "word_match",
            "question_text": q_txt,
            "audio_url": None,
            "audio_text": None,
            "options": m_opts,
            "correct_answer": m_ans
        })

    # =========================================================================
    # CATEGORY 3: fill_blank (Contextual grammar & semantics in sentences)
    # At least 3 variants per level
    # =========================================================================
    level_sentence_variants = {
        1: [
            ("I like to ______ quietly on the chair.", ["sit", "sat", "site", "seat"], "sit"),
            ("Use this sharp little ______ to fix the paper.", ["pin", "pan", "pen", "pun"], "pin"),
            ("He gave a gentle ______ on my shoulder.", ["tap", "tip", "top", "tape"], "tap")
        ],
        2: [
            ("The hungry little ______ drank all the milk from the bowl.", ["cat", "cot", "cut", "kit"], "cat"),
            ("Our friendly ______ barked happily when I arrived home.", ["dog", "dot", "doc", "dug"], "dog"),
            ("Please wipe your shoes on the welcome ______ before entering.", ["mat", "map", "met", "mit"], "mat")
        ],
        3: [
            ("After a long tiring day, I rested on my comfortable ______.", ["bed", "bad", "bid", "bud"], "bed"),
            ("The bright morning ______ shone through my window.", ["sun", "son", "sin", "soon"], "sun"),
            ("Every morning, athletes like to ______ around the open park.", ["run", "ran", "rain", "ring"], "run")
        ],
        4: [
            ("The clever wild ______ hid quietly behind the large tree.", ["fox", "box", "fix", "fax"], "fox"),
            ("He stored his old toys safely inside a sturdy wooden ______.", ["box", "fox", "bog", "bot"], "box"),
            ("The modern military ______ flew at supersonic speed.", ["jet", "net", "vet", "pet"], "jet")
        ],
        5: [
            ("The captain steered the giant ______ safely into the harbor.", ["ship", "chip", "shop", "sheet"], "ship"),
            ("My mother went to the local grocery ______ to buy fresh bread.", ["shop", "ship", "chop", "stop"], "shop"),
            ("She wore a ______ cotton jacket because the weather was warm.", ["thin", "shin", "chin", "then"], "thin")
        ],
        15: [
            ("When you participate in a dialogue, it is essential to listen and ______ clearly.", ["speak", "speech", "spoke", "speed"], "speak"),
            ("Many friendly ______ gathered in the city square to celebrate.", ["people", "person", "pupil", "purple"], "people"),
            ("If you do not understand the lesson, do not hesitate to ask a ______.", ["question", "answer", "statement", "remark"], "question")
        ]
    }

    sentence_items = level_sentence_variants.get(lvl)
    if not sentence_items:
        sentence_items = [
            (f"Daily practice with '{w1}' helps students speak more ______.", ["fluent and natural", "fluent and slowly", "fluency and native", "fluently and shy"], "fluent and natural"),
            (f"To express your thoughts using '{w2}', you must pronounce it ______.", ["accurately and clearly", "accurate and fast", "accuracy and silent", "accurately and vague"], "accurately and clearly"),
            (f"In real conversations, knowing how to use '{w3}' gives you ______.", ["high confidence", "high confuse", "higher confusing", "most confide"], "high confidence")
        ]

    for sent, s_opts, s_ans in sentence_items:
        pool.append({
            "category": "fill_blank",
            "question_type": "fill_blank",
            "question_text": f"أكمل الفراغ في الجملة التالية بالكلمة الصحيحة دلالياً ونحوياً:\n\"{sent}\"",
            "audio_url": None,
            "audio_text": None,
            "options": s_opts,
            "correct_answer": s_ans
        })

    # =========================================================================
    # CATEGORY 4: phoneme_or_dialogue (Conversational mastery / Phonics trap)
    # At least 3 variants per level
    # =========================================================================
    level_challenge_variants = {
        1: [
            ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /æ/ (مثل صوت A في Apple)؟", ["Sat", "Sit", "Pin", "Tin"], "Sat"),
            ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /ɪ/ (مثل صوت I في Ink)؟", ["Sit", "Sat", "Tan", "Pan"], "Sit"),
            ("أي من الكلمات التالية تبدأ بصوت الحرف الشفوي /p/ الانفجاري النقي؟", ["Pin", "Tin", "Sin", "Tan"], "Pin")
        ],
        2: [
            ("أي من الكلمات التالية تنتهي بصوت الحرف /g/ الانفجاري النقي؟", ["Dog", "Dot", "Doc", "Don"], "Dog"),
            ("أي من الكلمات التالية تبدأ بصوت الحرف /k/ الانفجاري (صوت C في Cat)؟", ["Cat", "Mat", "Fat", "Sat"], "Cat"),
            ("أي من الكلمات التالية تنتمي إلى عائلة القافية الصوتية (-at family)؟", ["Mat", "Map", "Mop", "Man"], "Mat")
        ],
        3: [
            ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /e/ (صوت E في Elephant)؟", ["Bed", "Bad", "Bid", "Bud"], "Bed"),
            ("أي من الكلمات التالية تحتوي على صوت الحركة القصيرة /ʌ/ (صوت U في Umbrella)؟", ["Sun", "Sin", "Son", "Set"], "Sun"),
            ("أي من الكلمات التالية تنتهي بصوت الحرف /d/ المجهور؟", ["Red", "Run", "Rug", "Rut"], "Red")
        ],
        4: [
            ("أي من الكلمات التالية تنتهي بصوت الحرفين المركبين /ks/ المكتوبين بحرف X؟", ["Box", "Bog", "Bob", "Bot"], "Box"),
            ("أي من الكلمات التالية تبدأ بصوت الحرف /dʒ/ الانفجاري الاحتكاكي (صوت J في Jet)؟", ["Jet", "Net", "Vet", "Pet"], "Jet"),
            ("أي من الكلمات التالية تبدأ بصوت الشفة والأسنان /v/ المجهور؟", ["Van", "Fan", "Pan", "Ban"], "Van")
        ],
        5: [
            ("أي من الكلمات التالية تبدأ بصوت /ʃ/ المهموس (صوت SH في Shell)؟", ["Ship", "Chip", "This", "Thin"], "Ship"),
            ("أي من الكلمات التالية تبدأ بصوت /tʃ/ المركب (صوت CH في Chair و Chocolate)؟", ["Chip", "Ship", "Tip", "Slip"], "Chip"),
            ("أي من الكلمات التالية تبدأ بصوت /θ/ اللثوي غير المجهور (صوت TH في Thin و Think)؟", ["Thin", "This", "That", "Then"], "Thin")
        ],
        15: [
            ("سألك شخص أجنبي في محادثة واقعية: 'Where are you from?'، فما هي الإجابة النموذجية؟", ["I am from Egypt.", "I am in Egypt.", "I come to Egypt.", "I living from Egypt."], "I am from Egypt."),
            ("إذا قال لك شخص في محادثة: 'Could you please speak a little slower?'، كيف ترد بأدب؟", ["Certainly! I will slow down.", "No, you listen fast.", "Why do you not hear?", "English is fast for me."], "Certainly! I will slow down."),
            ("كيف تبدأ محادثة ودية مع شخص تقابله لأول مرة بأسلوب طبيعي ومقبول؟", ["Excuse me, do you mind if I join you?", "Give me your name now.", "Why are you sitting here?", "Tell me everything about you."], "Excuse me, do you mind if I join you?")
        ]
    }

    challenge_items = level_challenge_variants.get(lvl)
    if not challenge_items:
        if lvl <= 20:
            challenge_items = [
                (f"إذا أردت تقديم نفسك لمتحدث أصلي في Level {lvl}، ما هي العبارة الأكثر لباقة؟", [f"Hello, my name is Ahmed and I am glad to meet you.", f"Me is Ahmed, you meet me.", f"Name my Ahmed is, see you.", f"I am name Ahmed, fine."], "Hello, my name is Ahmed and I am glad to meet you."),
                (f"ما هو الرد الطبيعي الأكثر ملاءمة عند سماع: 'Thank you for your valuable help'؟", ["You are very welcome! Anytime.", "Yes, I help you.", "No need to speak.", "I took your thanks."], "You are very welcome! Anytime."),
                (f"كيف تسأل باحترافية عن رأي الطرف الآخر في موضوع المحادثة؟", ["What do you think about this idea?", "You think what this idea?", "Give me idea of your mind.", "Why your thought is here?"], "What do you think about this idea?")
            ]
        elif lvl <= 35:
            challenge_items = [
                (f"في سياق المحادثة المتقدمة (Level {lvl})، أي عبارة تمثل التعبير الطبيعي الأكثر دقة؟", [f"I truly appreciate your perspective on {w1.lower()}.", f"I appreciate perspective on {w1.lower()} you.", f"Your perspective is appreciating {w1.lower()}.", f"Appreciation is my view for {w1.lower()}."], f"I truly appreciate your perspective on {w1.lower()}."),
                (f"كيف تعبر عن اتفاقك مع شخص في نقاش جاد بطريقة دبلوماسية وراقية؟", ["I completely see your point, and I share that view.", "I agree because you say so.", "Your talk is fine yes.", "No doubt I am like you."], "I completely see your point, and I share that view."),
                (f"كيف تعبر عن اختلافك في الرأي باحترام دون إحراج الطرف الآخر؟", ["I see where you are coming from, but I look at it slightly differently.", "You are wrong completely.", "That idea makes no sense.", "I do not accept your words."], "I see where you are coming from, but I look at it slightly differently.")
            ]
        else:
            challenge_items = [
                (f"في مستوى الطلاقة والإتقان الاحترافي (Level {lvl})، ما هو التعبير الاصطلاحي الأكثر بلاغة؟", ["To articulate ideas with precision and clarity", "To articulate ideas with vague words", "To speak quickly without clear meaning", "To translate literally from native language"], "To articulate ideas with precision and clarity"),
                (f"في المقابلات الرسمية والخطاب القيادي، ما هو التعبير الأقوى لوصف تخطي الصعوبات؟", ["We have overcome complex challenges through strategic collaboration.", "We beat problems because we are good.", "Hard things went away easily.", "Big trouble was solved without work."], "We have overcome complex challenges through strategic collaboration."),
                (f"ما هو التعبير الاصطلاحي الإنجليزي (Idiom) الذي يعني الوصول إلى جوهر الموضوع مباشرة؟", ["To cut to the chase", "To beat around the bush", "To burn the midnight oil", "To bark up the wrong tree"], "To cut to the chase")
            ]

    for c_txt, c_opts, c_ans in challenge_items:
        pool.append({
            "category": "phoneme_or_dialogue",
            "question_type": "phoneme_or_dialogue",
            "question_text": c_txt,
            "audio_url": None,
            "audio_text": None,
            "options": c_opts,
            "correct_answer": c_ans
        })

    return pool

def populate_database_with_multi_variants():
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

        # Clear existing questions
        cur.execute("DELETE FROM quiz_questions WHERE quiz_id = ?;", (quiz_id,))

        # Build multi-variant question pool (at least 12 questions per quiz)
        pool = generate_multi_variant_questions_for_level(lvl_item)

        for q in pool:
            cur.execute("""
                INSERT INTO quiz_questions (quiz_id, question_type, question_text, audio_url, options_json, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (
                quiz_id,
                q["question_type"],
                q["question_text"],
                q["audio_url"],
                json.dumps(q["options"], ensure_ascii=False),
                q["correct_answer"]
            ))
            total_inserted += 1

    con.commit()
    con.close()
    print(f"Successfully generated and inserted {total_inserted} multi-variant questions across {len(quizzes)} quizzes!")

if __name__ == "__main__":
    populate_database_with_multi_variants()
