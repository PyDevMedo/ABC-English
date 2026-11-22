# 50-Level English Curriculum Generator for ABC English Platform
# From Phonics (Level 1) to Conversational Fluency (Level 15) to Native Mastery (Level 50)

def generate_50_levels():
    levels = []

    # 1. First 10 Levels: Phonics & Early Reading Foundation
    stage1_meta = [
        (1, "Letter Sounds", "أصوات الحروف الأولى", ["S", "A", "T", "P", "I", "N"], [("Sat", "S-A-T", "جلس"), ("Sit", "S-I-T", "يجلس"), ("Tap", "T-A-P", "يطرق"), ("Pin", "P-I-N", "دبوس"), ("Pan", "P-A-N", "مقلاة"), ("Tan", "T-A-N", "أسمر")], ["I sit.", "I tap.", "A pin.", "A pan.", "I see a pin."], "اكتب حروف S, A, T, P, I, N ثلاث مرات بخط النسخ في كراسة الأسطر الأربعة."),
        (2, "CVC Words", "الكلمات الثلاثية CVC", ["M", "D", "G", "O", "C", "K"], [("Cat", "C-A-T", "قطة"), ("Dog", "D-O-G", "كلب"), ("Mat", "M-A-T", "سجادة"), ("Map", "M-A-P", "خريطة"), ("Kid", "K-I-D", "طفل"), ("Cot", "C-O-T", "سرير")], ["A cat.", "A dog.", "The cat sat.", "A kid and a dog.", "The map is on the mat."], "اكتب الكلمات الثلاثية Cat, Dog, Mat ثلاث مرات في كراستك."),
        (3, "Short Vowels", "الحركات القصيرة Short Vowels", ["E", "U", "R", "H", "B", "F"], [("Bed", "B-E-D", "سرير"), ("Red", "R-E-D", "أحمر"), ("Sun", "S-U-N", "شمس"), ("Run", "R-U-N", "يجري"), ("Bug", "B-U-G", "حشرة"), ("Hot", "H-O-T", "ساخن")], ["The sun is hot.", "A red bed.", "I run.", "The bug is on the bed.", "The bed is red."], "اكتب جملة: The sun is hot مرتين بخط جميل بين الأسطر الأربعة."),
        (4, "More Letter Sounds", "استكمال الحروف الأبجدية", ["L", "J", "V", "W", "X", "Y", "Z", "Q"], [("Box", "B-O-X", "صندوق"), ("Fox", "F-O-X", "ثعلب"), ("Web", "W-E-B", "شبكة"), ("Jet", "J-E-T", "طائرة نفاثة"), ("Van", "V-A-N", "شاحنة"), ("Zip", "Z-I-P", "سحاب")], ["A fox in a box.", "The jet is fast.", "A red van.", "Yes, I can zip.", "I see a web."], "اكتب الكلمات: Box, Fox, Jet مع رسم توضيحي بسيط بجانب كل كلمة."),
        (5, "Digraphs (SH, CH, TH)", "الأصوات المركبة الأساسية", ["SH", "CH", "TH"], [("Ship", "SH-I-P", "سفينة"), ("Shop", "SH-O-P", "متجر"), ("Chip", "CH-I-P", "رقاقة"), ("Chat", "CH-A-T", "محادثة"), ("Thin", "TH-I-N", "نحيف"), ("This", "TH-I-S", "هذا")], ["The ship is big.", "I chat with friends.", "This is thin.", "A chip in the shop.", "The shop is open."], "اكتب الكلمات: Ship, Chip, Thin وحدد الصوت المركب بلون مختلف."),
        (6, "Advanced Phonics", "تراكيب صوتية متقدمة (CK, NG, EE, OO)", ["CK", "NG", "EE", "OO"], [("Duck", "D-U-CK", "بطة"), ("Song", "S-O-NG", "أغنية"), ("See", "S-EE", "يرى"), ("Tree", "T-R-EE", "شجرة"), ("Moon", "M-OO-N", "قمر"), ("Food", "F-OO-D", "طعام")], ["I see a duck.", "The moon is up.", "A big tree.", "The food is good.", "A duck and a song."], "اكتب الجملتين: I see a big tree و The moon is up بخطك في كراستك."),
        (7, "Vowel Teams", "فرق الحركات الصوتية (AI, OA, AR, OR)", ["AI", "OA", "AR", "OR"], [("Rain", "R-AI-N", "مطر"), ("Train", "T-R-AI-N", "قطار"), ("Boat", "B-OA-T", "قارب"), ("Coat", "C-OA-T", "معطف"), ("Car", "C-AR", "سيارة"), ("Star", "S-T-AR", "نجمة")], ["I see a train.", "The boat is on water.", "A red car.", "A coat in the rain.", "The train is fast."], "اكتب الكلمات: Rain, Boat, Star مع كتابة المعنى العربي بجانب كل كلمة."),
        (8, "Word Families", "عائلات الكلمات والدمج المتقدم", ["-at", "-an", "-ig", "-op"], [("Pig", "P-I-G", "خنزير بري"), ("Big", "B-I-G", "كبير"), ("Hop", "H-O-P", "يقفز"), ("Top", "T-O-P", "قمة"), ("Hat", "H-A-T", "قبعة"), ("Bat", "B-A-T", "مضرب")], ["A big hat.", "I can hop.", "The bat is big.", "He sat on the mat.", "A hat on the top."], "اكتب عائلة الكلمات: Hat, Cat, Bat, Mat في عمود مرتب."),
        (9, "Sight Words & Fluency", "الكلمات البصرية السريعة", ["the", "and", "they", "have", "you"], [("Look", "L-OO-K", "ينظر"), ("Play", "P-L-AY", "يلعب"), ("Come", "C-O-M-E", "يأتي"), ("Like", "L-I-K-E", "يحب"), ("Good", "G-OO-D", "جيد"), ("Help", "H-E-L-P", "يساعد")], ["Look at me.", "I like to play.", "They have a dog.", "Can you help me?", "We play together."], "اكتب 3 جمل كاملة تحتوي على: I like, You have, Look at."),
        (10, "First Reading Paragraph", "قراءة أول فقرة كاملة", ["Reading", "Writing", "Flow"], [("Story", "S-T-O-R-Y", "قصة"), ("Book", "B-OO-K", "كتاب"), ("Read", "R-EA-D", "يقرأ"), ("Write", "W-R-I-T-E", "يكتب"), ("Learn", "L-EA-R-N", "يتعلم"), ("Start", "S-T-AR-T", "يبدأ")], ["I read my book.", "I can write stories.", "Learning English is fun.", "Every day I learn more.", "I read and write."], "انسخ الفقرة القصيرة كاملة في كراستك وصورها بوضوح.")
    ]

    for num, title, subtitle, letters_list, words_list, sentences_list, hw in stage1_meta:
        letters_data = [{"symbol": l, "sound": f"/{l.lower()}/", "name": l, "sound_name": f"{l} sound", "arabic_desc": f"صوت {l} النقي"} for l in letters_list]
        words_data = [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_list]
        sentences_data = [{"text": s, "translation_ar": s} for s in sentences_list]
        levels.append({
            "level_number": num,
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": f"إتقان مهارات {subtitle} مع الاستماع والنطق والتطبيق العملي في كراسة الخط.",
            "icon": "sparkles",
            "letters": letters_data,
            "words": words_data,
            "sentences": sentences_data,
            "sight_words": [w[0] for w in words_list[:3]],
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"أهلاً بك في {title}. استمع بتركيز، كرر الكلمات ثلاث مرات، وأكمل كتابة الواجب في كراستك."
        })

    # 2. Stage 2: Levels 11-20 — Everyday Communication (Level 15: Speak with People!)
    stage2_meta = [
        (11, "Daily Greetings & Introductions", "التحيات اليومية والتعريف بالنفس", [("Hello", "H-E-LL-O", "مرحباً"), ("Name", "N-A-M-E", "اسم"), ("Nice", "N-I-C-E", "لطيف"), ("Meet", "M-EE-T", "يلتقي"), ("Morning", "M-OR-N-I-NG", "صباح"), ("Friend", "F-R-IE-N-D", "صديق")], ["Hello, my name is John.", "Nice to meet you.", "Good morning, friend.", "How are you today?", "I am doing great."], "اكتب محادثة تعارف بين شخصين: (Hello, What is your name? My name is...) في كراستك."),
        (12, "Family & Relationships", "العائلة والأقارب والوصف", [("Mother", "M-O-TH-ER", "أم"), ("Father", "F-A-TH-ER", "أب"), ("Brother", "B-R-O-TH-ER", "أخ"), ("Sister", "S-I-S-T-ER", "أخت"), ("Family", "F-A-M-I-L-Y", "عائلة"), ("Happy", "H-A-PP-Y", "سعيد")], ["This is my family.", "I love my mother and father.", "My brother is tall.", "We are a happy family.", "My sister is smart."], "اكتب 4 جمل تصف فيها أفراد عائلتك بالإنجليزية."),
        (13, "Time, Numbers & Routine", "الوقت، الأرقام والروتين اليومي", [("Clock", "C-L-O-CK", "ساعة"), ("Morning", "M-OR-N-I-NG", "صباح"), ("Night", "N-IGH-T", "ليل"), ("Wake", "W-A-K-E", "يستيقظ"), ("School", "S-CH-OO-L", "مدرسة"), ("Today", "T-O-D-AY", "اليوم")], ["I wake up at seven.", "It is eight o'clock.", "I go to school every day.", "Time to study.", "Good night, see you tomorrow."], "اكتب جدول روتينك اليومي: (I wake up at... I eat breakfast at...)."),
        (14, "Food, Ordering & Café", "المطعم، الطعام والطلب بأدب", [("Water", "W-A-T-ER", "ماء"), ("Bread", "B-R-EA-D", "خبز"), ("Apple", "A-PP-L-E", "تفاحة"), ("Please", "P-L-EA-S-E", "من فضلك"), ("Thank", "TH-A-N-K", "شكراً"), ("Order", "OR-D-ER", "يطلب")], ["Can I have water, please?", "I would like an apple.", "Thank you very much.", "The food is delicious.", "Here is your order."], "اكتب حوار طلب وجبة في مطعم باستخدام: (Can I have... please?)."),
        (15, "Talking with People (Conversations!)", "محادثة الناس والتواصل الاجتماعي التلقائي", [("Speak", "S-P-EA-K", "يتحدث"), ("Talk", "T-A-L-K", "يتكلم"), ("People", "P-EO-P-L-E", "الناس"), ("Question", "QU-E-S-T-I-ON", "سؤال"), ("Answer", "A-N-S-W-ER", "إجابة"), ("Listen", "L-I-S-T-EN", "يستمع")], ["Where are you from?", "I like talking in English.", "Can you tell me more?", "It is wonderful to meet you.", "Let us talk again tomorrow."], "اكتب محادثة حقيقية كاملة من 6 أسطر يمكنك استخدامها للتحدث مع أي شخص أجنبي."),
        (16, "Asking for Directions & Places", "السؤال عن الأماكن والاتجاهات", [("Where", "WH-E-R-E", "أين"), ("Right", "R-IGH-T", "يمين"), ("Left", "L-E-F-T", "يسار"), ("Street", "S-T-R-EE-T", "شارع"), ("Near", "N-EA-R", "قريب"), ("City", "C-I-T-Y", "مدينة")], ["Where is the library?", "Turn right at the corner.", "Go straight ahead.", "It is next to the park.", "Thank you for directions."], "ارسم خريطة بسيطة واكتب الاتجاهات: Turn left, Go straight, Turn right."),
        (17, "Shopping & Clothes", "التسوق، الأسعار والملابس", [("Shirt", "SH-IR-T", "قميص"), ("Shoes", "SH-OE-S", "حذاء"), ("Price", "P-R-I-C-E", "سعر"), ("Much", "M-U-CH", "كمية"), ("Color", "C-O-L-OR", "لون"), ("Store", "S-T-OR-E", "متجر")], ["How much is this shirt?", "I like this blue color.", "Do you have size medium?", "I will take these shoes.", "Can I pay by card?"], "اكتب حوار شراء قطعة ملابس والسؤال عن سعرها ومقاسها."),
        (18, "Weather & Seasons", "الطقس، الفصول والأنشطة", [("Sunny", "S-U-NN-Y", "مشمس"), ("Rainy", "R-AI-N-Y", "ممطر"), ("Windy", "W-I-N-D-Y", "عاصف"), ("Cold", "C-O-L-D", "بارد"), ("Warm", "W-AR-M", "دافئ"), ("Season", "S-EA-S-ON", "فصل")], ["It is sunny today.", "Take an umbrella, it is raining.", "Winter is cold in our city.", "I love the spring flowers.", "What is the weather like?"], "اكتب وصفاً لحالة الطقس اليوم وفصلك المفضل ولماذا."),
        (19, "Emotions & Expressing Needs", "التعبير عن المشاعر والاحتياجات", [("Happy", "H-A-PP-Y", "سعيد"), ("Tired", "T-I-R-ED", "متعب"), ("Excited", "EX-C-I-T-ED", "متحمس"), ("Need", "N-EE-D", "يحتاج"), ("Feel", "F-EE-L", "يشعر"), ("Help", "H-E-L-P", "مساعدة")], ["I feel very happy today.", "I am tired, I need to sleep.", "We are excited for the trip.", "Do you need any help?", "I feel confident speaking."], "اكتب 4 جمل تعبر فيها عن مشاعرك في مواقف مختلفة."),
        (20, "Hobbies & Free Time", "الهوايات والأنشطة الترفيهية", [("Read", "R-EA-D", "يقرأ"), ("Music", "M-U-S-I-C", "موسيقى"), ("Sport", "S-P-OR-T", "رياضة"), ("Draw", "D-R-AW", "يرسم"), ("Watch", "W-A-T-CH", "يشاهد"), ("Hobby", "H-O-BB-Y", "هواية")], ["My favorite hobby is reading.", "I play football on weekends.", "She loves listening to music.", "What do you do in your free time?", "Practicing English is my hobby."], "اكتب فقرة عن هوايتك المفضلة وكيف تقضي وقت فراغك.")
    ]

    for num, title, subtitle, words_list, sentences_list, hw in stage2_meta:
        letters_data = [{"symbol": w[0][:2].upper(), "sound": f"/{w[0][:2].lower()}/", "name": w[0], "sound_name": w[0], "arabic_desc": w[2]} for w in words_list[:4]]
        words_data = [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_list]
        sentences_data = [{"text": s, "translation_ar": s} for s in sentences_list]
        levels.append({
            "level_number": num,
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": f"تطوير الطلاقة والتواصل العملي: {subtitle}.",
            "icon": "users",
            "letters": letters_data,
            "words": words_data,
            "sentences": sentences_data,
            "sight_words": [w[0] for w in words_list[:3]],
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"مرحباً بك في المستوى {num}! هدفك اليوم هو التحدث والتواصل بطلاقة حول {subtitle}."
        })

    # 3. Stage 3: Levels 21-35 — Intermediate Fluency & Grammar Mastery
    stage3_topics = [
        (21, "Present Continuous Tense", "المضارع المستمر ووصف اللحظة الحالية"),
        (22, "Past Simple Tense", "الماضي البسيط ورواية ما حدث بالأمس"),
        (23, "Future with Will & Going to", "المستقبل والتخطيط للأيام القادمة"),
        (24, "Health & Medical Visits", "الصحة ومراجعة الطبيب وشرح الأعراض"),
        (25, "School & Study Conversations", "المحادثات المدرسية والجامعية والدراسية"),
        (26, "Phone Calls & Voice Notes", "المكالمات الهاتفية والرسائل الصوتية بطلاقة"),
        (27, "Jobs, Careers & Workplaces", "المهن وبيئة العمل والمهام اليومية"),
        (28, "Polite Requests & Disagreements", "إبداء الرأي والطلب بأدب والاختلاف الراقي"),
        (29, "Travel, Airports & Hotels", "السفر والمطارات وحجوزات الفنادق"),
        (30, "Storytelling & Expressive Flow", "سرد القصص والتتابع الزمني المعبر"),
        (31, "Giving Advice with Should & Could", "تقديم النصائح والاقتراحات الذكية"),
        (32, "Technology & Digital Communication", "التكنولوجيا والتواصل الرقمي الحديث"),
        (33, "Environment & Global World", "البيئة والطبيعة والتحديات العالمية"),
        (34, "Comparisons & Superlatives", "المقارنة والتفضيل بين الأشياء والأفكار"),
        (35, "Certainty & Probability", "التعبير عن التأكيد والاحتمالية والشك")
    ]

    for num, title, subtitle in stage3_topics:
        w_sample = [("Express", "EX-P-R-E-SS", "يعبر"), ("Context", "C-O-N-T-EX-T", "سياق"), ("Fluent", "F-L-U-E-N-T", "فصيح/طلق"), ("Practice", "P-R-A-C-T-I-C-E", "ممارسة"), ("Improve", "I-M-P-R-O-V-E", "يطور"), ("Succeed", "S-U-CC-EE-D", "ينجح")]
        s_sample = [f"I am mastering {title}.", "Practice makes my English fluent.", "I can explain my thoughts clearly.", "Speaking English is becoming natural.", "Every level brings more confidence."]
        levels.append({
            "level_number": num,
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": f"بناء الطلاقة التعبيرية والتراكيب اللغوية: {subtitle}.",
            "icon": "book-open",
            "letters": [{"symbol": "EN", "sound": "/en/", "name": "Grammar", "sound_name": "Grammar Structure", "arabic_desc": subtitle}],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in w_sample],
            "sentences": [{"text": s, "translation_ar": s} for s in s_sample],
            "sight_words": ["Because", "Although", "Therefore"],
            "homework_prompt": f"اكتب فقرة من 5 أسطر في كراستك تطبق فيها موضوع {title} مع نطقها 3 مرات.",
            "repetition_count": 3,
            "intro_ar": f"مستوى متقدم جديد! في المستوى {num} ستنتقل لخطوة احترافية في {subtitle}."
        })

    # 4. Stage 4: Levels 36-45 — Advanced Professional Fluency
    stage4_topics = [
        (36, "Essential English Idioms", "التعبيرات الاصطلاحية الإنجليزية الدارجة"),
        (37, "Phrasal Verbs in Action (Part 1)", "الأفعال المركبة الشائعة في الحياة اليومية"),
        (38, "Phrasal Verbs in Action (Part 2)", "الأفعال المركبة المتقدمة"),
        (39, "Job Interviews & Pitching", "المقابلات الشخصية والتقديم الاحترافي"),
        (40, "Professional Business Meetings", "اجتماعات العمل والمراسلات المهنية"),
        (41, "Critical Thinking & Analysis", "التفكير النقدي وتحليل الأفكار المعقدة"),
        (42, "Debating & Persuasion", "المناظرات والإقناع وبناء الحجج القوية"),
        (43, "Fast Native Accents & Slang", "الاستماع السريع للهجات وتفهم النطق المتصل"),
        (44, "Formal vs Informal English", "التمييز بين الأسلوب الرسمي والعفوي"),
        (45, "Cultural Nuances & Humor", "الفكاهة والتلميحات الثقافية في الإنجليزية")
    ]

    for num, title, subtitle in stage4_topics:
        w_sample = [("Persuade", "P-ER-S-UA-D-E", "يقنع"), ("Analyze", "A-N-A-L-Y-Z-E", "يحلل"), ("Negotiate", "N-E-G-O-T-I-A-T-E", "يفاوض"), ("Professional", "P-R-O-F-E-SS-I-O-N-A-L", "محترف"), ("Dialogue", "D-I-A-L-O-G-UE", "حوار"), ("Advanced", "A-D-V-A-N-C-ED", "متقدم")]
        s_sample = [f"This concept is crucial for {title}.", "In my opinion, we should analyze the options.", "I completely see your point.", "Let us explore an alternative approach.", "Speaking with natural cadence is key."]
        levels.append({
            "level_number": num,
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": f"الطلاقة الاحترافية ومحاكاة المتحدثين الأصليين: {subtitle}.",
            "icon": "award",
            "letters": [{"symbol": "ADV", "sound": "/ædv/", "name": "Idiom", "sound_name": "Advanced Concept", "arabic_desc": subtitle}],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in w_sample],
            "sentences": [{"text": s, "translation_ar": s} for s in s_sample],
            "sight_words": ["Furthermore", "Nevertheless", "Consequently"],
            "homework_prompt": f"اكتب مقالاً قصيراً أو حواراً متقدماً عن {title} يتضمن 3 تعبيرات اصطلاحية.",
            "repetition_count": 3,
            "intro_ar": f"مرحباً بك في المستوى الاحترافي {num}. اليوم ستتعلم كيف يفكر ويتحدث أصحاب اللغة الأصليون في {subtitle}."
        })

    # 5. Stage 5: Levels 46-50 — Native Mastery (Bilingual Native Fluency)
    stage5_topics = [
        (46, "Complex Discourse & Connectors", "الخطاب المعقد وأدوات الربط البلاغية"),
        (47, "Public Speaking & Presentations", "الخطابة الجماهيرية والإلقاء المؤثر"),
        (48, "Subtle Nuances & Colloquialisms", "الدلالات الدقيقة والتعابير العامية العميقة"),
        (49, "Spontaneous High-Stakes Negotiation", "التفاوض الارتجالي وحل النزاعات المعقدة"),
        (50, "Native Mastery & Bilingual Fluency", "الطلاقة التامة والتحدث كمتحدث أصلي (Native)")
    ]

    for num, title, subtitle in stage5_topics:
        w_sample = [("Eloquent", "E-L-O-QU-E-N-T", "بليغ"), ("Mastery", "M-A-S-T-ER-Y", "إتقان تام"), ("Spontaneous", "S-P-O-N-T-A-N-E-OU-S", "تلقائي/ارتجالي"), ("Nuance", "N-U-A-N-C-E", "فارق دقيق"), ("Bilingual", "B-I-L-I-N-G-U-A-L", "ثنائي اللغة"), ("Native", "N-A-T-I-V-E", "أصلي")]
        s_sample = [f"Achieving {title} requires true immersion.", "I can effortlessly express complex emotions in English.", "My accent, rhythm, and vocabulary reflect native intuition.", "Language is now a window to global knowledge.", "I speak English with absolute natural confidence."]
        levels.append({
            "level_number": num,
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": f"المرحلة الختامية العليا: {subtitle} للوصول للتحدث بالإنجليزية كأنها لغتك الأم.",
            "icon": "trophy",
            "letters": [{"symbol": "NAT", "sound": "/neɪt/", "name": "Mastery", "sound_name": "Native Mastery", "arabic_desc": subtitle}],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in w_sample],
            "sentences": [{"text": s, "translation_ar": s} for s in s_sample],
            "sight_words": ["Effortlessly", "Intuition", "Spontaneous"],
            "homework_prompt": f"اكتب خطاباً أو تسجيلاً مكتوباً من صفحة كاملة تلخص فيه رحلتك التعليمية وصولاً للمستوى {num} بالإنجليزية الكاملة.",
            "repetition_count": 3,
            "intro_ar": f"تهانينا! أنت في قمة الهرم اللغوي (المستوى {num}). هدفنا الآن هو الطلاقة العفوية المطلقة كمتحدث أصلي."
        })

    return levels

CURRICULUM_50 = generate_50_levels()
