"""
Comprehensive 50-Level Progressive English Curriculum Generator.
Pedagogical Blueprint:
- Levels 1-10 (Foundation): Letters, phonics, CVC blending, short vowels, consonant digraphs, basic sight words.
- Levels 11-20 (Words to Sentences): Functional everyday vocabulary, sentence building blocks, questions & greetings, conversation.
- Levels 21-30 (Sentences to Short Paragraphs): Grammar tenses (Present/Past/Future), daily life, routines, short multi-sentence stories.
- Levels 31-40 (Short Paragraphs to Extended Articles): Opinions, technology, culture, science, connectors, reading comprehension.
- Levels 41-50 (Advanced Essays, Debates & Native Fluency): Formal rhetoric, argumentation, critical thinking, full essays/articles, idioms & public discourse.
"""

def get_50_levels_data():
    levels = []

    # =========================================================================
    # STAGE 1: LEVELS 1 - 10 (الحروف والأصوات وتركيب الكلمات الأولى)
    # =========================================================================
    stage1 = [
        (
            1, "Letter Sounds & First Blends", "أصوات الحروف الأولى (S, A, T, P, I, N)",
            "تأسيس أصوات الحروف الإنجليزية النقية والتمييز السمعي للأصوات الأولى.",
            [("S", "/s/", "صوت الصفير S مثل Snake"), ("A", "/æ/", "حركة الفتح القصيرة مثل Apple"), ("T", "/t/", "الصوت الانفجاري T مثل Tiger"), ("P", "/p/", "صوت الشفاه الانفجاري P مثل Pan"), ("I", "/ɪ/", "حركة الكسر الخفيفة I مثل Ink"), ("N", "/n/", "الصوت الأنفي N مثل Net")],
            [("Sat", "S-A-T", "جلس"), ("Sit", "S-I-T", "يجلس"), ("Tap", "T-A-P", "يطرق"), ("Pin", "P-I-N", "دبوس"), ("Pan", "P-A-N", "مقلاة"), ("Tan", "T-A-N", "أسمر")],
            [("I sit.", "أنا أجلس."), ("I tap.", "أنا أطرق."), ("A pin.", "دبوس صغير."), ("A pan.", "مقلاة طعام."), ("I see a pin.", "أنا أرى دبوساً.")],
            {"title": "The Little Pin", "text": "I sit by the pan. I see a pin. I tap the pin.", "translation_ar": "أنا أجلس بجانب المقلاة. أرى دبوساً. أنقر على الدبوس نقرة خفيفة."},
            "اكتب حروف S, A, T, P, I, N ثلاث مرات واكتب كلمتي Sit و Pan بخط جميل في كراسة الأسطر الأربعة."
        ),
        (
            2, "CVC Consonant-Vowel-Consonant Words", "الكلمات الثلاثية CVC (M, D, G, O, C, K)",
            "دمج الحروف الساكنة مع المتحركة لنطق كلمات ثلاثية بسيطة وفهم معناها.",
            [("M", "/m/", "صوت الشفتين M مثل Monkey"), ("D", "/d/", "صوت D الانفجاري مثل Dog"), ("G", "/g/", "صوت G الحلقي مثل Girl"), ("O", "/ɒ/", "حركة الضم القصيرة مثل Orange"), ("C", "/k/", "صوت الكاف الصلب C مثل Cat"), ("K", "/k/", "صوت K مثل Kite")],
            [("Cat", "C-A-T", "قطة"), ("Dog", "D-O-G", "كلب"), ("Mat", "M-A-T", "سجادة"), ("Map", "M-A-P", "خريطة"), ("Kid", "K-I-D", "طفل"), ("Cot", "C-O-T", "سرير صغير")],
            [("A cat.", "قطة."), ("A dog.", "كلب."), ("The cat sat.", "جلست القطة."), ("A kid and a dog.", "طفل وكلب."), ("The map is on the mat.", "الخريطة على السجادة.")],
            {"title": "Cat and Dog", "text": "A cat sat on a mat. A dog ran to the cat. The kid smiled.", "translation_ar": "جلست قطة على سجادة. جرى كلب نحو القطة. ابتسم الطفل الصغير."},
            "اكتب الكلمات الثلاثية Cat, Dog, Mat ثلاث مرات واكتب جملة: The cat sat on the mat."
        ),
        (
            3, "Short Vowels in Action", "الحركات القصيرة (E, U, R, H, B, F)",
            "التمييز الصوتي بين حركات الكسر والضم والفتح السريعة.",
            [("E", "/e/", "كسرة خفيفة مثل Elephant"), ("U", "/ʌ/", "ضمة مفتوحة مثل Umbrella"), ("R", "/r/", "صوت الراء الإنجليزية مثل Rabbit"), ("H", "/h/", "صوت الهاء الهوائي مثل Hat"), ("B", "/b/", "صوت الباء المجهور مثل Ball"), ("F", "/f/", "صوت الفاء مثل Fish")],
            [("Bed", "B-E-D", "سرير"), ("Red", "R-E-D", "أحمر"), ("Sun", "S-U-N", "شمس"), ("Run", "R-U-N", "يجري"), ("Bug", "B-U-G", "حشرة"), ("Hot", "H-O-T", "ساخن")],
            [("The sun is hot.", "الشمس حارة."), ("A red bed.", "سرير أحمر."), ("I can run.", "أستطيع أن أجري."), ("The bug is on the bed.", "الحشرة على السرير."), ("The bed is warm and red.", "السرير دافئ وأحمر.")],
            {"title": "A Hot Day", "text": "The sun is hot today. The red bug is on the bed. I run and play in the sun.", "translation_ar": "الشمس حارة اليوم. الحشرة الحمراء على السرير. أنا أجري وألعب في الشمس."},
            "اكتب جملة: The sun is hot مرتين واكتب الكلمات Bed, Red, Sun بخط متناسق."
        ),
        (
            4, "Alphabet Completion & Sound Exploration", "استكمال الحروف والأصوات الأبجدية",
            "إتمام باقي أصوات الحروف (J, L, V, W, X, Y, Z) وتطبيقها في مفردات حية.",
            [("L", "/l/", "صوت اللام مثل Lion"), ("J", "/dʒ/", "صوت الجيم المعطشة مثل Jam"), ("V", "/v/", "صوت الفاء المجهورة مثل Van"), ("W", "/w/", "صوت الواو مثل Wind"), ("X", "/ks/", "صوت الكاف والسين مثل Box"), ("Z", "/z/", "صوت الزاي مثل Zebra")],
            [("Box", "B-O-X", "صندوق"), ("Fox", "F-O-X", "ثعلب"), ("Web", "W-E-B", "شبكة"), ("Jet", "J-E-T", "طائرة نفاثة"), ("Van", "V-A-N", "شاحنة"), ("Zip", "Z-I-P", "سحاب")],
            [("A fox in a box.", "ثعلب في صندوق."), ("The jet is fast.", "الطائرة النفاثة سريعة."), ("A red van.", "شاحنة حمراء."), ("I see a spider web.", "أرى شبكة عنكبوت."), ("Yes, I can zip my bag.", "نعم، أستطيع إغلاق سحاب حقيبتي.")],
            {"title": "The Fox and the Box", "text": "A quick fox saw a big box. The fox jumped in the box. A fast jet flew above.", "translation_ar": "رأى ثعلب سريع صندوقاً كبيراً. قفز الثعلب في الصندوق. وطارت طائرة نفاثة سريعة في الأعلى."},
            "اكتب الكلمات: Box, Fox, Jet, Van واكتب جملة: The jet is fast."
        ),
        (
            5, "Consonant Digraphs (SH, CH, TH)", "الأصوات المركبة الأساسية",
            "إتقان الأصوات الناتجة عن دمج حرفين ساكنين: الشين، التاء شين، والذال/الثاء.",
            [("SH", "/ʃ/", "صوت الشين مثل Ship و Sheep"), ("CH", "/tʃ/", "صوت التاء شين مثل Chair و Chocolate"), ("TH", "/θ/ /ð/", "صوت الثاء والذال مثل Thin و This")],
            [("Ship", "SH-I-P", "سفينة"), ("Shop", "SH-O-P", "متجر"), ("Chip", "CH-I-P", "رقاقة"), ("Chat", "CH-A-T", "محادثة"), ("Thin", "TH-I-N", "نحيف"), ("This", "TH-I-S", "هذا")],
            [("The ship is big.", "السفينة كبيرة."), ("I chat with friends.", "أنا أتحادث مع أصدقائي."), ("This is very thin.", "هذا نحيف جداً."), ("A potato chip in the shop.", "رقاقة بطاطس في المتجر."), ("The shop is open now.", "المتجر مفتوح الآن.")],
            {"title": "At the Harbor Shop", "text": "We see a big ship at sea. We walk to the harbor shop. We chat and eat a fresh chip.", "translation_ar": "نرى سفينة ضخمة في البحر. نمشي إلى متجر الميناء. نتحدث ونأكل رقاقة طازجة."},
            "اكتب الكلمات المركبة: Ship, Chip, Thin وحدد الصوت المركب الأول بلون مميز."
        ),
        (
            6, "Double Vowels & End Blends (CK, NG, EE, OO)", "التراكيب الصوتية المتقدمة",
            "نطق أصوات المد الطويلة EE و OO والأصوات الحلقية في نهاية الكلمات NG و CK.",
            [("EE", "/iː/", "ياء المد الطويلة مثل See و Tree"), ("OO", "/uː/", "واو المد الطويلة مثل Moon و Food"), ("CK", "/k/", "صوت الكاف الحاسم مثل Duck و Clock"), ("NG", "/ŋ/", "الغنة الأنفية مثل Song و Ring")],
            [("Duck", "D-U-CK", "بطة"), ("Song", "S-O-NG", "أغنية"), ("See", "S-EE", "يرى"), ("Tree", "T-R-EE", "شجرة"), ("Moon", "M-OO-N", "قمر"), ("Food", "F-OO-D", "طعام")],
            [("I see a duck.", "أنا أرى بطة."), ("The moon is up in the sky.", "القمر مرتفع في السماء."), ("A tall green tree.", "شجرة خضراء طويلة."), ("The healthy food is good.", "الطعام الصحي لذيذ."), ("They sing a lovely song.", "هم يغنون أغنية جميلة.")],
            {"title": "Under the Night Sky", "text": "At night, we see the bright moon. A small duck sleeps by the tree. The night is quiet and sweet.", "translation_ar": "في الليل، نرى القمر الساطع. بطة صغيرة تنام بجانب الشجرة. الليل هادئ وجميل."},
            "انسخ الجملتين: I see a tall green tree و The bright moon is up بخط النسخ."
        ),
        (
            7, "Vowel Teams & R-Controlled Vowels", "فرق الحركات الصوتية (AI, OA, AR, OR)",
            "فهم كيف تغير الحروف المتحركة المزدوجة وحرف R صوت الكلمة ونطقها.",
            [("AI", "/eɪ/", "صوت المد الإيمائي مثل Rain و Train"), ("OA", "/oʊ/", "صوت الواو الممدودة مثل Boat و Coat"), ("AR", "/ɑːr/", "صوت الآر المفخم مثل Car و Star"), ("OR", "/ɔːr/", "صوت الأور مثل Storm و Fork")],
            [("Rain", "R-AI-N", "مطر"), ("Train", "T-R-AI-N", "قطار"), ("Boat", "B-OA-T", "قارب"), ("Coat", "C-OA-T", "معطف"), ("Car", "C-AR", "سيارة"), ("Star", "S-T-AR", "نجمة")],
            [("I see a fast train.", "أرى قطاراً سريعاً."), ("The wooden boat floats on water.", "القارب الخشبي يطفو على الماء."), ("A shiny red car.", "سيارة حمراء لامعة."), ("Wear a warm coat in the rain.", "ارتدِ معطفاً دافئاً في المطر."), ("Look at that bright star.", "انظر إلى تلك النجمة اللامعة.")],
            {"title": "A Journey in the Rain", "text": "Rain falls softly on the road. We ride the fast train to the coast. Through the window, we see a boat on the water.", "translation_ar": "يسقط المطر بهدوء على الطريق. نركب القطار السريع إلى الساحل. عبر النافذة، نرى قارباً على الماء."},
            "اكتب الكلمات: Rain, Train, Boat, Star مع كتابة معناها العربي المقابل."
        ),
        (
            8, "Word Families & Rapid Rhyming", "عائلات الكلمات والقوافي الصوتية",
            "تسريع طلاقة القراءة عبر التعرف التلقائي على أوزان الكلمات المتشابهة في القافية.",
            [("-at", "/æt/", "عائلة وزن at مثل Cat, Hat, Bat"), ("-ig", "/ɪg/", "عائلة وزن ig مثل Pig, Big, Dig"), ("-op", "/ɒp/", "عائلة وزن op مثل Hop, Top, Mop"), ("-an", "/æn/", "عائلة وزن an مثل Pan, Fan, Van")],
            [("Pig", "P-I-G", "حيوان أليف"), ("Big", "B-I-G", "كبير"), ("Hop", "H-O-P", "يقفز"), ("Top", "T-O-P", "قمة"), ("Hat", "H-A-T", "قبعة"), ("Bat", "B-A-T", "مضرب")],
            [("A big friendly pig.", "حيوان كبير وأليف."), ("I can hop high.", "أستطيع أن أقفز عالياً."), ("The baseball bat is long.", "مضرب البيسبول طويل."), ("He put his hat on the top.", "وضع قبعته في القمة."), ("The bunny can hop and stop.", "الأرنب يستطيع أن يقفز ويتوقف.")],
            {"title": "The Little Bunny", "text": "A big happy bunny can hop. He hops to the top of the hill. He has a tiny green hat.", "translation_ar": "أرنب كبير وسعيد يستطيع القفز. يقفز إلى قمة التل. ولديه قبعة خضراء صغيرة."},
            "اكتب عائلة الكلمات: Hat, Cat, Bat وعائلة Pig, Big في عمودين متناسقين."
        ),
        (
            9, "Sight Words & Instant Recognition", "الكلمات البصرية السريعة والطلاقة الأولى",
            "قراءة الكلمات الإنجليزية الأكثر تكراراً بالعين فوراً دون الحاجة لتهجئة الحروف.",
            [("Sight", "/saɪt/", "كلمات بصرية شائعة: the, and, they, have, you, what, where")],
            [("Look", "L-OO-K", "ينظر"), ("Play", "P-L-AY", "يلعب"), ("Come", "C-O-M-E", "يأتي"), ("Like", "L-I-K-E", "يحب"), ("Good", "G-OO-D", "جيد"), ("Help", "H-E-L-P", "يساعد")],
            [("Look at me, please.", "انظر إليّ من فضلك."), ("I like to play sports.", "أحب ممارسة الرياضة."), ("They have a cute puppy.", "لديهم جرو لطيف."), ("Can you help me carry this?", "هل يمكنك مساعدتي في حمل هذا؟"), ("We play happily together.", "نلعب معاً بسعادة.")],
            {"title": "Playing with Friends", "text": "They have a lovely park near home. 'Come and play with us,' they say. I like my kind friends because we help each other every day.", "translation_ar": "لديهم حديقة جميلة قرب المنزل. يقولون: 'تعال والعب معنا'. أنا أحب أصدقائي الطيبين لأننا نساعد بعضنا كل يوم."},
            "اكتب 3 جمل كاملة تحتوي على الكلمات البصرية: I like, We play, You help me."
        ),
        (
            10, "Paragraph Reading & Comprehensive Review", "قراءة أول فقرة متكاملة ومترابطة",
            "الانتقال التاريخي من قراءة الكلمات المنفصلة إلى قراءة فقرة كاملة ذات معنى وسياق.",
            [("Read", "/riːd/", "مهارة القراءة السلسة والربط بين الأفكار")],
            [("Story", "S-T-O-R-Y", "قصة"), ("Book", "B-OO-K", "كتاب"), ("Read", "R-EA-D", "يقرأ"), ("Write", "W-R-I-T-E", "يكتب"), ("Learn", "L-EA-R-N", "يتعلم"), ("Start", "S-T-AR-T", "يبدأ")],
            [("I read my colorful storybook.", "أقرأ كتاب القصص الملون الخاص بي."), ("I can write clear English words.", "أستطيع كتابة كلمات إنجليزية واضحة."), ("Learning English is an exciting journey.", "تعلم الإنجليزية رحلة ممتعة."), ("Every day I practice and learn more.", "كل يوم أمارس وأتعلم المزيد."), ("Today I start reading full paragraphs.", "اليوم أبدأ بقراءة فقرات كاملة.")],
            {"title": "My First Reading Journey", "text": "Every morning, I open my colorful book. I read the sweet words out loud. My teacher listens and smiles with pride. Learning to read and write English makes me feel confident and strong. Now, I am ready to speak with the whole world!", "translation_ar": "كل صباح، أفتح كتابي الملون. أقرأ الكلمات الجميلة بصوت عالٍ. معلمي يستمع ويبتسم بفخر. تعلم القراءة والكتابة بالإنجليزية يجعلني أشعر بالثقة والقوة. والآن أنا جاهز للتحدث مع العالم كله!"},
            "انسخ الفقرة الكاملة 'My First Reading Journey' بخطك الجميل في كراسة الخط والتقط صورة واضحة."
        )
    ]

    for num, title, subtitle, desc, letters_raw, words_raw, sents_raw, passage, hw in stage1:
        levels.append({
            "level_number": num,
            "stage": 1,
            "stage_name": "المرحلة 1: التأسيس وأصوات الحروف (Phonics & Early Reading)",
            "level_type": "letters_and_words",
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": desc,
            "icon": "sparkles",
            "letters": [{"symbol": l[0], "sound": l[1], "name": l[0], "sound_name": f"{l[0]} sound", "arabic_desc": l[2]} for l in letters_raw],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_raw],
            "sentences": [{"text": s[0], "translation_ar": s[1]} for s in sents_raw],
            "passage": passage,
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"أهلاً بك في {title}. استمع بانتباه، كرر الكلمات، واقرأ الجمل والقصة بصوت واضح."
        })

    # =========================================================================
    # STAGE 2: LEVELS 11 - 20 (الكلمات والجمل الحياتية والمحادثة الاجتماعية)
    # =========================================================================
    stage2 = [
        (
            11, "Daily Greetings & Social Introductions", "التحيات اليومية والتعريف بالنفس",
            "بناء الثقة في إلقاء التحية ومقابلة الناس والتعريف بالاسم والبلد.",
            [("Hello", "H-E-LL-O", "مرحباً"), ("Name", "N-A-M-E", "اسم"), ("Nice", "N-I-C-E", "لطيف"), ("Meet", "M-EE-T", "يلتقي"), ("Morning", "M-OR-N-I-NG", "صباح"), ("Friend", "F-R-IE-N-D", "صديق")],
            [("Hello, my name is Ahmed.", "مرحباً، اسمي أحمد."), ("Nice to meet you!", "سعيد بلقائك!"), ("Good morning, how are you today?", "صباح الخير، كيف حالك اليوم؟"), ("I am doing great, thank you.", "أنا بخير حال، شكراً لك."), ("This is my kind friend, Omar.", "هذا صديقي اللطيف، عمر.")],
            {"title": "Meeting a New Classmate", "text": "It was a sunny morning at school. Ahmed walked up to the new student. 'Hello, my name is Ahmed,' he said with a warm smile. 'Nice to meet you! How are you today?' The new student smiled back and replied, 'I am great, thank you. I am glad we are friends!'", "translation_ar": "كان صباحاً مشمساً في المدرسة. تقدم أحمد نحو الطالب الجديد. قال بابتسامة دافئة: 'مرحباً، اسمي أحمد. سعيد بلقائك! كيف حالك اليوم؟'. ابتسم الطالب الجديد ورد: 'أنا بخير شكراً لك. يسعدني أننا أصدقاء!'."},
            "اكتب حوار تعارف كامل بين شخصين (التحية، السؤال عن الحال، والاسم) في كراستك."
        ),
        (
            12, "Family Members & Character Descriptions", "العائلة والأقارب وصفات الأشخاص",
            "استخدام الكلمات التعبيرية لوصف أفراد العائلة وشخصياتهم ومظهرهم.",
            [("Mother", "M-O-TH-ER", "أم"), ("Father", "F-A-TH-ER", "أب"), ("Brother", "B-R-O-TH-ER", "أخ"), ("Sister", "S-I-S-T-ER", "أخت"), ("Family", "F-A-M-I-L-Y", "عائلة"), ("Helpful", "H-E-L-P-F-U-L", "مساعد/متعاون")],
            [("This is my loving family.", "هذه عائلتي الحبيبة."), ("My mother is kind and patient.", "أمي طيبة وصبورة."), ("My father works hard every day.", "أبي يعمل بجد كل يوم."), ("My brother is tall and athletic.", "أخي طويل ورياضي."), ("My little sister is very smart and helpful.", "أختي الصغيرة ذكية جداً ومتعاونة.")],
            {"title": "My Wonderful Family", "text": "Family is the greatest treasure in life. In our cozy home, my mother cooks delicious meals with love, while my father teaches us valuable lessons about respect and honesty. My older brother always plays games with me, and my little sister makes us laugh with her joyful jokes. We always support each other through everything.", "translation_ar": "العائلة هي الكنز الأعظم في الحياة. في بيتنا الدافئ، تطهو أمي وجبات لذيذة بحب، بينما يعلمنا أبي دروساً قيّمة عن الاحترام والصدق. أخي الأكبر يلعب معي الألعاب دائماً، وأختي الصغيرة تضحكنا بنكاتها المرحة. نحن ندعم بعضنا دائماً في كل شيء."},
            "اكتب 4 جمل تصف فيها أفراد عائلتك وماذا تحب في كل فرد منهم."
        ),
        (
            13, "Time, Daily Schedules & Habits", "الوقت، الروتين اليومي وجدول المواعيد",
            "التعبير عن الوقت بالساعات والدقائق وسرد الأنشطة اليومية من الصباح للمساء.",
            [("Clock", "C-L-O-CK", "ساعة حائط"), ("Wake", "W-A-K-E", "يستيقظ"), ("School", "S-CH-OO-L", "مدرسة"), ("Night", "N-IGH-T", "ليل"), ("Early", "EA-R-L-Y", "مبكراً"), ("Routine", "R-OU-T-I-N-E", "روتين")],
            [("I wake up early at seven o'clock.", "أستيقظ مبكراً في السابعة تماماً."), ("It is time to eat a healthy breakfast.", "حان وقت تناول إفطار صحي."), ("I go to school at eight o'clock.", "أذهب للمدرسة في الثامنة تماماً."), ("In the afternoon, I finish my homework.", "بعد الظهر، أنتهي من واجباتي المدرسية."), ("I sleep early to stay energetic.", "أنام مبكراً لأبقى مفعماً بالطاقة.")],
            {"title": "A Day in My Productive Life", "text": "Every morning at seven o'clock, my alarm rings cheerfully. I jump out of bed, wash my face, and enjoy a nutritious breakfast of warm milk and fresh fruit. By eight o'clock, I am sitting eagerly in my classroom, discovering exciting ideas in science and language. In the evening, after completing my homework, I read a captivating story before turning off the lights.", "translation_ar": "كل صباح في السابعة تماماً، يرن منبهي ببهجة. أقفز من السرير، أغسل وجهي، وأتناول إفطاراً مغذياً من الحليب الدافئ والفاكهة الطازجة. وبحلول الثامنة، أكون جالساً بحماس في فصلي أكتشف أفكاراً مشوقة في العلوم واللغات. وفي المساء، بعد إنهاء واجباتي، أقرأ قصة آسرة قبل إطفاء الأنوار."},
            "اكتب جدول روتينك اليومي موضحاً 4 أوقات مختلفة باللغة الإنجليزية."
        ),
        (
            14, "Food, Dining & Courteous Ordering", "المطعم، الطعام والطلب بأدب",
            "المفردات الخاصة بالوجبات والأطعمة وكيفية الطلب بأدب في المطاعم والمقاهي.",
            [("Water", "W-A-T-ER", "ماء"), ("Bread", "B-R-EA-D", "خبز"), ("Apple", "A-PP-L-E", "تفاحة"), ("Order", "OR-D-ER", "يطلب"), ("Please", "P-L-EA-S-E", "من فضلك"), ("Delicious", "D-E-L-I-C-I-OU-S", "لذيذ")],
            [("Can I have a glass of water, please?", "هل يمكنني الحصول على كوب ماء من فضلك؟"), ("I would like to order a warm soup.", "أود طلب حساء دافئ."), ("This fresh salad is extremely delicious.", "هذه السلطة الطازجة لذيذة للغاية."), ("Thank you very much for your great service.", "شكراً جزيلاً لك على خدمتك الممتازة."), ("Could we please have the bill?", "هل يمكننا الحصول على الحساب من فضلك؟")],
            {"title": "Dining at the Garden Bistro", "text": "Yesterday, my friends and I visited a cozy bistro near the public park. The polite waiter handed us the menus and asked, 'What can I bring for you today?' I smiled and said, 'Could I please have a bowl of vegetable soup and fresh orange juice?' The meal was served hot and flavorful. We truly enjoyed the delightful flavors and polite atmosphere.", "translation_ar": "بالأمس، زرت أنا وأصدقائي مطعماً دافئاً قرب الحديقة العامة. سلمنا النادل المهذب قوائم الطعام وسأل: 'ماذا يمكنني أن أحضر لكم اليوم؟'. ابتسمت وقلت: 'هل يمكنني من فضلك الحصول على وعاء حساء خضار وعصير برتقال طازج؟'. قُدمت الوجبة ساخنة وغنية بالنكهة. استمتعنا حقاً بالنكهات الرائعة والأجواء الراقية."},
            "اكتب حوار طلب وجبة كاملة في مطعم باستخدام: Could I please have... و Thank you."
        ),
        (
            15, "Conversations with Real People (Fluency Milestone)", "التحدث مع الناس والتواصل الاجتماعي المباشر",
            "المحطة الفاصلة: القدرة على خوض محادثة حقيقية كاملة مع أي متحدث أجنبي بطلاقة وثقة.",
            [("Speak", "S-P-EA-K", "يتحدث"), ("Talk", "T-A-L-K", "يتكلم"), ("People", "P-EO-P-L-E", "الناس"), ("Question", "QU-E-S-T-I-ON", "سؤال"), ("Answer", "A-N-S-W-ER", "إجابة"), ("Listen", "L-I-S-T-EN", "يستمع")],
            [("Where are you from originally?", "من أي بلد أنت في الأصل؟"), ("I come from Egypt, a land of ancient civilization.", "أنا من مصر، بلد الحضارة العريقة."), ("What brings you to our city today?", "ما الذي أتى بك إلى مدينتنا اليوم؟"), ("I really enjoy exchanging ideas with friendly people.", "أستمتع حقاً بتبادل الأفكار مع الناس الطيبين."), ("It has been an absolute pleasure talking with you!", "كان من دواعي سروري البالغ التحدث معك!")],
            {"title": "An Inspiring Conversation in London", "text": "While sitting at a sunny park bench, I struck up a conversation with a traveler from Canada. 'Excuse me, where are you from?' I inquired politely. He smiled brightly, 'I am from Vancouver! How about you?' I replied confidently, 'I am from Egypt, learning English to connect with people across the globe.' We chatted effortlessly about our favorite books, traditional foods, and future dreams. It was the moment I realized: I can truly speak English!", "translation_ar": "أثناء جلوسي على مقعد في حديقة مشمسة، بدأت محادثة مع مسافر من كندا. سألت بلباقة: 'عفواً، من أين أنت؟'. ابتسم بحرارة: 'أنا من فانكوفر! وماذا عنك؟'. أجبت بكل ثقة: 'أنا من مصر، وأتعلم الإنجليزية لأتواصل مع الناس في كل العالم.' تحدثنا بسلاسة عن كتبنا المفضلة، أكلاتنا الشعبية، وأحلامنا المستقبلية. كانت تلك اللحظة التي أدركت فيها: أنا أستطيع حقاً التحدث بالإنجليزية!"},
            "اكتب محادثة واقعية من 6 أسطر يمكنك استخدامها في المطار أو الفندق للتعرف على شخص أجنبي."
        ),
        (
            16, "Directions, Landmarks & City Navigation", "السؤال عن الأماكن والاتجاهات ومعالم المدينة",
            "كيف تسأل وتصف الاتجاهات الجغرافية والأماكن الحيوية بدقة ولغة واضحة.",
            [("Where", "WH-E-R-E", "أين"), ("Right", "R-IGH-T", "يمين"), ("Left", "L-E-F-T", "يسار"), ("Straight", "S-T-R-AIGH-T", "مستقيم"), ("Corner", "C-OR-N-ER", "زاوية/منعطف"), ("Station", "S-T-A-T-I-ON", "محطة")],
            [("Excuse me, could you direct me to the nearest museum?", "عفواً، هل يمكنك إرشادي لأقرب متحف؟"), ("Turn right at the traffic lights.", "انعطف يميناً عند إشارة المرور."), ("Walk straight ahead for two blocks.", "سر للأمام مباشرة لمسافة مربعين سكنيين."), ("The train station is right across the street.", "محطة القطار تقع تماماً عبر الشارع."), ("You will see a large blue building on your left.", "سترى مبنى أزرق كبير على يسارك.")],
            {"title": "Finding the Historic Library", "text": "A foreign tourist looked puzzled on the bustling street corner. I approached him politely and asked, 'May I help you find your way?' He smiled with relief and said, 'Yes, please! I am searching for the historic public library.' I explained clearly: 'Walk straight along this avenue, turn left past the post office, and you will see the grand entrance right next to the park.' He thanked me warmly for the clear directions.", "translation_ar": "بدا سائح أجنبي حائراً على زاوية الشارع المزدحم. اقتربت منه بلباقة وسألته: 'هل يمكنني مساعدتك في العثور على طريقك؟'. ابتسم بارتياح وقال: 'نعم من فضلك! أنا أبحث عن المكتبة العامة التاريخية.' شرحت له بوضوح: 'سر للأمام مباشرة على هذا الشارع، انعطف يساراً بعد مكتب البريد، وسترى المدخل الرئيسي بجانب الحديقة مباشرة.' شكرني بحرارة على التوجيهات الدقيقة."},
            "ارسم مخطط اتجاهات بسيط واكتب 3 إرشادات باستخدام: Turn left, Go straight, On your right."
        ),
        (
            17, "Shopping, Prices & Product Specifications", "التسوق، الأسعار ومواصفات السلع",
            "إجراء حوارات الشراء والتفاوض واختيار المقاسات والألوان وطرق الدفع.",
            [("Price", "P-R-I-C-E", "سعر"), ("Shirt", "SH-IR-T", "قميص"), ("Size", "S-I-Z-E", "مقاس"), ("Color", "C-O-L-OR", "لون"), ("Discount", "D-I-S-C-OU-N-T", "خصم"), ("Cash", "C-A-SH", "نقد")],
            [("How much does this elegant jacket cost?", "كم ثمن هذه السترة الأنيقة؟"), ("Do you carry this shirt in size medium?", "هل يتوفر لديكم هذا القميص بمقاس متوسط؟"), ("Can I try this on in the fitting room?", "هل يمكنني قياس هذا في غرفة تبديل الملابس؟"), ("Is there any promotional discount today?", "هل يوجد أي خصم ترويجي اليوم؟"), ("I will pay using my credit card, please.", "سأدفع باستخدام بطاقتي الائتمانية من فضلك.")],
            {"title": "Shopping for Winter Clothes", "text": "With the cold winter breeze approaching, I visited the downtown department store to buy a durable wool jacket. The sales assistant was very attentive and showed me various shades of navy blue and dark gray. I asked, 'Could I try this jacket in medium size?' It fit comfortably and kept me remarkably warm. When she mentioned a twenty percent seasonal discount, I happily decided to purchase it.", "translation_ar": "مع اقتراب نسيم الشتاء البارد، زرت المتجر الكبير في وسط المدينة لشراء سترة صوفية متينة. كانت البائعة مهتمة للغاية وأرتني درجات مختلفة من الكحلي والرمادي الداكن. سألتها: 'هل يمكنني تجربة هذه السترة بمقاس وسط؟'. كانت مناسبة جداً ومريحة وأشعرتني بدفء ملحوظ. وعندما ذكرت وجود خصم موسمي بنسبة عشرين بالمائة، قررت شراءها بكل سعادة."},
            "اكتب حوار تسوق مع البائع تسأل فيه عن السعر والمقاس وإمكانية القياس."
        ),
        (
            18, "Weather, Climate Patterns & Seasons", "الطقس، تغيرات المناخ وفصول السنة",
            "وصف الأحوال الجوية ودرجات الحرارة والتخطيط للأنشطة بناءً على الطقس.",
            [("Sunny", "S-U-NN-Y", "مشمس"), ("Rainy", "R-AI-N-Y", "ممطر"), ("Windy", "W-I-N-D-Y", "عاصف"), ("Breeze", "B-R-EE-Z-E", "نسيم"), ("Season", "S-EA-S-ON", "فصل"), ("Forecast", "F-OR-E-C-A-S-T", "نشرة جوية")],
            [("The weather forecast predicts a pleasant sunny afternoon.", "تتوقع النشرة الجوية ظهيرة مشمسة ولطيفة."), ("Make sure to carry an umbrella because it might rain.", "احرص على حمل مظلة لاحتمال هطول المطر."), ("Autumn brings cool refreshing breezes and colorful falling leaves.", "الخريف يأتي بنسمات عليلة وأوراق شجر متساقطة ملونة."), ("Spring is my favorite season because blossoms fill the gardens.", "الربيع فصلي المفضل لأن الأزهار تملأ الحدائق."), ("The temperature dropped significantly overnight.", "انخفضت درجة الحرارة بشكل ملحوظ خلال الليل.")],
            {"title": "The Beauty of Changing Seasons", "text": "Every season of the year holds its own enchanting charm. Spring brings vibrant colors as blossoming flowers awaken our spirits. Summer offers bright sunshine, perfect for swimming and coastal journeys. Autumn paints the mountains with golden hues as cool breezes invite reflective evening walks. And winter, with its crisp chilly air, gathers families around warm fireplaces. Appreciating nature's diverse cycles enriches our daily gratitude.", "translation_ar": "كل فصل من فصول السنة يحمل سحره الخاص والآسر. الربيع يجلب ألواناً نابضة بالحياة حيث توقظ الأزهار المتفتحة أرواحنا. الصيف يوفر أشعة شمس ساطعة مثالية للسباحة ورحلات الشواطئ. الخريف يصبغ الجبال بألوان ذهبية بينما تدعو النسمات العليلة للمشي المسائي الهادئ. والشتاء، بهوائه البارد المنعش، يجمع العائلات حول المدافئ الدافئة. تقدير دورات الطبيعة المتنوعة يثري امتناننا اليومي."},
            "اكتب فقرة من 5 أسطر تصف فيها طقس اليوم وفصلك السنوي المفضل مع التعليل."
        ),
        (
            19, "Emotions, Mindset & Expressing Needs", "المشاعر، الحالة النفسية والتعبير عن الاحتياجات",
            "القدرة على وصف المشاعر بدقة (الحماس، التردد، الثقة، الامتنان) والتعبير عن الدعم.",
            [("Happy", "H-A-PP-Y", "سعيد"), ("Excited", "EX-C-I-T-ED", "متحمس"), ("Confident", "C-O-N-F-I-D-E-N-T", "واثق"), ("Grateful", "G-R-A-T-E-F-U-L", "ممتن"), ("Calm", "C-A-L-M", "هادئ"), ("Courage", "C-OU-R-A-G-E", "شجاعة")],
            [("I feel genuinely excited about mastering the English language.", "أشعر بحماس حقيقي لإتقان اللغة الإنجليزية."), ("Whenever I speak, I remind myself to remain calm and confident.", "كلما تحدثت، أذكر نفسي بأن أبقى هادئاً وواثقاً."), ("I am deeply grateful for the guidance and encouragement I receive.", "أنا ممتن للغاية للتوجيه والتشجيع الذي أتلقاه."), ("Do not hesitate to reach out if you feel overwhelmed.", "لا تتردد في طلب المساعدة إذا شعرت بالإرهاق."), ("Courage is not the absence of fear, but taking action regardless.", "الشجاعة ليست غياب الخوف، بل التقدم والعمل رغم وجوده.")],
            {"title": "Building Confidence Through Practice", "text": "When I first attempted to speak English, my hands trembled slightly and I felt hesitant. But my teacher offered reassuring advice: 'Mistakes are not failures; they are the stepping stones of mastery.' Hearing those words transformed my entire mindset. Instead of worrying about perfection, I focused on genuine connection. Day by day, my hesitation melted away, replaced by calm self-assurance. Today, every conversation is an inspiring opportunity to share my authentic voice.", "translation_ar": "عندما حاولت التحدث بالإنجليزية لأول مرة، كانت يداي ترتجفان قليلاً وشعرت بالتردد. لكن معلمي قدم نصيحة مطمئنة: 'الأخطاء ليست فشلاً؛ إنها درجات السلم نحو الإتقان.' سماع تلك الكلمات غيّر طريقة تفكيري بالكامل. وبدلاً من القلق بشأن الكمال، ركزت على التواصل الحقيقي. ويوماً بعد يوم، تلاشى ترددي وحل محله يقين هادئ بالنفس. واليوم، كل محادثة هي فرصة ملهمة لمشاركة صوتي الحقيقي."},
            "اكتب 4 جمل تعبر فيها عن مشاعرك تجاه رحلتك في تعلم اللغة الإنجليزية وكيف تتغلب على التردد."
        ),
        (
            20, "Passions, Hobbies & Personal Growth", "الهوايات، الشغف والتطور الشخصي",
            "التحدث عن الاهتمامات الشخصية وكيف تساهم الهوايات في بناء الشخصية وصقل المهارات.",
            [("Hobby", "H-O-BB-Y", "هواية"), ("Passion", "P-A-SS-I-ON", "شغف"), ("Creative", "C-R-EA-T-I-V-E", "مبدع"), ("Sport", "S-P-OR-T", "رياضة"), ("Music", "M-U-S-I-C", "موسيقى"), ("Skill", "S-K-I-LL", "مهارة")],
            [("Pursuing meaningful hobbies broadens our horizons and relieves stress.", "ممارسة الهوايات الهادفة توسع مداركنا وتخفف التوتر."), ("My favorite hobby is reading history books and creative writing.", "هوايتي المفضلة هي قراءة كتب التاريخ والكتابة الإبداعية."), ("Playing football every weekend teaches us the power of teamwork.", "لعب كرة القدم أسبوعياً يعلمنا قوة العمل الجماعي."), ("Music enables us to express profound feelings beyond mere words.", "الموسيقى تمكننا من التعبير عن مشاعر عميقة تفوق الكلمات المجردة."), ("Consistent dedication transforms a simple interest into true mastery.", "التفاني المستمر يحول الاهتمام البسيط إلى إتقان حقيقي.")],
            {"title": "The Power of Meaningful Hobbies", "text": "Engaging in rewarding hobbies is essential for a balanced and fulfilling life. For some people, painting vibrant canvases provides an outlet for boundless imagination. For others, playing an instrument like the violin cultivates deep patience and discipline. In my own life, reading literature in English has opened doors to diverse cultures and profound wisdom. Hobbies not only bring immense joy but also shape our character, fostering lifelong curiosity and intellectual growth.", "translation_ar": "ممارسة الهوايات المفيدة أمر أساسي لحياة متوازنة ومليئة بالإنجاز. بالنسبة لبعض الناس، يوفر رسم اللوحات النابضة بالحياة متنفساً للخيال اللامحدود. وبالنسبة لآخرين، فإن العزف على آلة مثل الكمان ينمي صبراً عميقاً وانضباطاً. وفي حياتي الخاصة، فتحت قراءة الأدب باللغة الإنجليزية أبواباً على ثقافات متنوعة وحكمة عميقة. الهوايات لا تجلب فرحاً هائلاً فحسب، بل تبني شخصيتنا وتغذي فضولنا الدائم ونمونا الفكري."},
            "اكتب مقالاً قصيراً من 5 أسطر في كراستك عن هوايتك وشغفك وكيف تطورها بانتظام."
        )
    ]

    for num, title, subtitle, desc, words_raw, sents_raw, passage, hw in stage2:
        levels.append({
            "level_number": num,
            "stage": 2,
            "stage_name": "المرحلة 2: المحادثة والتواصل مع الناس (Everyday Conversations)",
            "level_type": "words_to_sentences",
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": desc,
            "icon": "users",
            "letters": [{"symbol": w[0][:2].upper(), "sound": f"/{w[0][:2].lower()}/", "name": w[0], "sound_name": w[0], "arabic_desc": w[2]} for w in words_raw[:4]],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_raw],
            "sentences": [{"text": s[0], "translation_ar": s[1]} for s in sents_raw],
            "passage": passage,
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"مرحباً بك في المستوى {num}! هدفك اليوم هو التحدث والتواصل بطلاقة حول {subtitle}."
        })

    # =========================================================================
    # STAGE 3: LEVELS 21 - 30 (بناء الجمل المترابطة والفقرات السردية)
    # =========================================================================
    stage3 = [
        (
            21, "Present Continuous & Describing Ongoing Actions", "المضارع المستمر ووصف الأحداث الجارية",
            "صياغة الجمل في زمن المضارع المستمر بدقة لوصف ما يحدث في اللحظة الراهنة.",
            [("Active", "A-C-T-I-V-E", "نشط"), ("Develop", "D-E-V-E-L-O-P", "يطور"), ("Progress", "P-R-O-G-R-E-SS", "يتقدم"), ("Moment", "M-O-M-E-N-T", "لحظة"), ("Focus", "F-O-C-U-S", "يركز"), ("Achieve", "A-CH-IE-V-E", "يحقق")],
            [("I am currently studying advanced English vocabulary.", "أنا أدرس حالياً مفردات إنجليزية متقدمة."), ("The children are playing joyfully in the courtyard.", "الأطفال يلعبون ببهجة في الفناء."), ("Look, the technological world is changing rapidly right now.", "انظر، العالم التكنولوجي يتغير بسرعة فائقة الآن."), ("We are actively developing our public speaking abilities.", "نحن نعمل بنشاط على تطوير مهاراتنا في الإلقاء والتحدث."), ("The professor is explaining an intriguing scientific theory.", "الأستاذ يشرح نظرية علمية مشوقة ومثيرة.")],
            {"title": "Life in the City Square", "text": "Right now, the downtown city square is buzzing with lively energy. Street musicians are playing melodious tunes on their guitars, while curious spectators are gathering in cheerful circles. Nearby, artists are painting vivid portraits of smiling families. Young students are sitting at café tables, sipping iced drinks and discussing their academic projects. Everyone is embracing the present moment with genuine warmth.", "translation_ar": "الآن في هذه اللحظة، تعج ساحة المدينة المركزية بطاقة نابضة بالحياة. عازفو الشوارع يعزفون ألحاناً عذبة على غيتاراتهم، بينما يتجمع المشاهدون الفضوليون في حلقات مبهجة. وعلى مقربة منهم، يرسم فنانون لوحات حية لعائلات مبتسمة. يجلس طلاب صغار على طاولات المقاهي، يحتسون المشروبات المثلجة ويناقشون مشاريعهم الدراسية. الجميع يعيش اللحظة الحاضرة بدفء حقيقي."},
            "اكتب 5 جمل في زمن المضارع المستمر (am/is/are + verb-ing) تصف فيها ما يحدث حولك الآن في غرفتك أو منزلك."
        ),
        (
            22, "Past Simple Tense & Memorable Experiences", "الماضي البسيط ورواية الذكريات والمواقف السابقة",
            "سرد الأحداث التاريخية والذكريات الشخصية السابقة باستخدام الأفعال الماضية المنتظمة وغير المنتظمة.",
            [("Yesterday", "Y-E-S-T-ER-D-AY", "أمس"), ("Visited", "V-I-S-I-T-ED", "زار"), ("Discovered", "D-I-S-C-O-V-ER-ED", "اكتشف"), ("Learned", "L-EA-R-N-ED", "تعلم"), ("Inspired", "I-N-S-P-I-R-ED", "ألهم"), ("Memorable", "M-E-M-O-R-A-B-L-E", "لا يُنسى")],
            [("Last summer, our family traveled to an ancient coastal city.", "الصيف الماضي، سافرت عائلتنا لمدينة ساحلية أثرية."), ("I discovered a rare handwritten manuscript in the old archives.", "اكتشفت مخطوطة نادرة مكتوبة بخط اليد في الأرشيف القديم."), ("We celebrated our academic achievements with our devoted teachers.", "احتفلنا بإنجازاتنا الأكاديمية مع معلمينا المخلصين."), ("The historical museum inspired me to explore ancient cultures.", "ألهمني المتحف التاريخي لاستكشاف الثقافات القديمة."), ("Yesterday was truly one of the most memorable days of my life.", "كان يوم أمس بحق من أكثر الأيام التي لا تُنسى في حياتي.")],
            {"title": "An Unforgettable Journey to Alexandria", "text": "Last spring, my school organized an educational excursion to the historic city of Alexandria. Early in the morning, we boarded the comfortable train and watched the green delta landscape glide past our windows. When we arrived, the majestic Bibliotheca Alexandrina left us breathless with admiration. We walked through towering halls filled with millions of volumes and interacted with ancient historical exhibits. That journey ignited my lifelong love for knowledge.", "translation_ar": "في الربيع الماضي، نظمت مدرستي رحلة تعليمية لمدينة الإسكندرية التاريخية. في الصباح الباكر، ركبنا القطار المريح وشاهدنا مناظر الدلتا الخضراء تمر أمام نوافذنا. وعندما وصلنا، أبهرتنا مكتبة الإسكندرية المهيبة بعظمتها. مشينا عبر قاعات شاهقة تضم ملايين المجلدات وتفاعلنا مع معروضات تاريخية قديمة. تلك الرحلة أشعلت عشقي الدائم للمعرفة."},
            "اكتب فقرة من 6 أسطر في كراستك تحكي فيها عن موقف أو رحلة لا تنساها في الماضي باستخدام الأفعال الماضية."
        ),
        (
            23, "Future Projections, Goals & Intentions", "المستقبل، الأهداف والتخطيط للسنوات القادمة",
            "استخدام Will و Going to للتعبير عن الخطط المستقبلية والتنبؤات والطموحات المهنية.",
            [("Future", "F-U-T-U-R-E", "مستقبل"), ("Intend", "I-N-T-E-N-D", "ينوي"), ("Achieve", "A-CH-IE-V-E", "يحقق"), ("Ambition", "A-M-B-I-T-I-ON", "طموح"), ("Strategy", "S-T-R-A-T-E-G-Y", "خطة/استراتيجية"), ("Succeed", "S-U-CC-EE-D", "ينجح")],
            [("In the upcoming years, I will speak English with complete fluency.", "في السنوات القادمة، سأتحدث الإنجليزية بطلاقة تامة."), ("I am going to study computer science and artificial intelligence.", "أنا أنوي دراسة علوم الحاسب والذكاء الاصطناعي."), ("Dedication and discipline will undoubtedly lead to outstanding success.", "التفاني والانضباط سيقودان بلا شك لنجاح باهر."), ("We are going to launch an innovative community project next month.", "نحن نعتزم إطلاق مشروع مجتمعي مبتكر الشهر القادم."), ("Vision without execution remains a mere daydream.", "الرؤية بدون تطبيق تظل مجرد حلم يقظة عابر.")],
            {"title": "My Vision for the Next Decade", "text": "Looking ahead towards the coming decade, I envision a future defined by continuous learning and positive impact. First, I am going to master multilingual communication so that I can collaborate with visionary scientists worldwide. Furthermore, I will harness cutting-edge technologies to design solutions for environmental challenges. With persistent effort and unyielding passion, I am confident that these aspirations will become tangible realities.", "translation_ar": "بالنظر للأمام نحو العقد القادم، أتصور مستقبلاً يتسم بالتعلم المستمر والأثر الإيجابي. أولاً، سأتقن التواصل متعدد اللغات لأتمكن من التعاون مع علماء ملهمين حول العالم. علاوة على ذلك، سأوظف التكنولوجيات المتقدمة لتصميم حلول للتحديات البيئية. وبفضل الجهد المستمر والشغف الراسخ، أنا واثق أن هذه التطلعات ستتحول لحقائق ملموسة."},
            "اكتب 5 أهداف مستقبلية تنوي تحقيقها باستخدام الصيغتين: I will... و I am going to..."
        ),
        (
            24, "Health, Wellness & Navigating Medical Care", "الصحة، العافية والتعامل في العيادات والمستشفيات",
            "المصطلحات الطبية لوصف الأعراض الصحية، النصائح الغذائية، والتواصل مع الأطباء.",
            [("Health", "H-EA-L-TH", "صحة"), ("Doctor", "D-O-C-T-OR", "طبيب"), ("Medicine", "M-E-D-I-C-I-N-E", "دواء"), ("Symptom", "S-Y-M-P-T-O-M", "عَرَض مرضي"), ("Nutritious", "N-U-T-R-I-T-I-OU-S", "مغذٍ/صحي"), ("Exercise", "EX-ER-C-I-S-E", "تمرين")],
            [("Maintaining a nutritious diet is the cornerstone of vibrant health.", "الحفاظ على غذاء صحي متوازن هو حجر الأساس لصحة مفعمة بالحيوية."), ("I made an appointment to consult the specialist regarding my headache.", "حددت موعداً لاستشارة الطبيب الأخصائي بخصوص الصداع."), ("Regular cardiovascular exercise strengthens the heart and clears the mind.", "التمارين الهوائية المنتظمة تقوي عضلة القلب وتصفي الذهن."), ("The pharmacist provided detailed instructions about dosage and timing.", "قدم الصيدلي تعليمات مفصلة بشأن الجرعة وأوقات تناولها."), ("Getting sufficient restful sleep empowers your immune defense.", "الحصول على قدر كافٍ من النوم المريح يقوي جهازك المناعي.")],
            {"title": "The Path to Holistic Wellness", "text": "True wellness encompasses not merely the absence of physical illness, but the harmonious vitality of body, mind, and spirit. Nourishing our bodies with whole foods, drinking plentiful clean water, and engaging in invigorating physical activities lay a sturdy foundation. Equally vital is cultivating mental peace by managing daily stress through meditation and positive human bonds. Investing in your health today yields lifelong happiness.", "translation_ar": "العافية الحقيقية لا تعني مجرد غياب المرض الجسدي، بل الحيوية المتناغمة للجسد والعقل والروح. إن تغذية أجسادنا بالأطعمة الطبيعية، شرب وفرة من الماء النقي، وممارسة الأنشطة البدنية تضع أساساً متيناً. ومما لا يقل أهمية عن ذلك تنمية راحة البال من خلال إدارة الضغوط اليومية بالتأمل والروابط الإنسانية الإيجابية. الاستثمار في صحتك اليوم يثمر سعادة تدوم مدى الحياة."},
            "اكتب حواراً في عيادة طبية بين مريض وطبيب يصف فيه الأعراض ويطلب النصيحة الطبية."
        ),
        (
            25, "Education, Academic Discussions & University Life", "المحادثات الأكاديمية والتعليم والحياة الجامعية",
            "المصطلحات الجامعية والمناقشات العلمية داخل قاعات المحاضرات والمكتبات.",
            [("Academy", "A-C-A-D-E-M-Y", "أكاديمية"), ("Lecture", "L-E-C-T-U-R-E", "محاضرة"), ("Research", "R-E-S-EA-R-CH", "بحث علمي"), ("Scholar", "S-CH-O-L-AR", "باحث/عالم"), ("Degree", "D-E-G-R-EE", "درجة علمية"), ("Knowledge", "K-N-O-W-L-E-D-G-E", "معرفة")],
            [("The university library contains thousands of peer-reviewed journals.", "مكتبة الجامعة تحتوي على آلاف المجلات العلمية المحكمة."), ("We participated actively in the seminar discussion on renewable energy.", "شاركنا بفاعلية في نقاش الندوة حول الطاقة المتجددة."), ("Conducting meticulous empirical research requires patience and integrity.", "يتطلب إجراء بحث علمي تجريبي دقيق صبراً وأمانة علمية عالية."), ("Higher education equips students with sharp critical thinking skills.", "التعليم الجامعي يزود الطلاب بمهارات تفكير نقدي حادة."), ("Lifelong learning is the compass that guides human civilization.", "التعلم مدى الحياة هو البوصلة التي تقود الحضارة الإنسانية.")],
            {"title": "A Day Inside the University Hall", "text": "Entering the university auditorium early in the semester, a student feels the electric thrill of intellectual discovery. The professor ignited our curiosity with a provocative question regarding ethical considerations in technological development. Classmates from various cultural backgrounds eagerly contributed distinct viewpoints, turning the hall into a dynamic laboratory of ideas. University life teaches us not merely what to think, but how to analyze critically.", "translation_ar": "عند دخول قاعة المحاضرات الجامعية في بداية الفصل الدراسي، يشعر الطالب بإثارة الاكتشاف الفكري. أشعل الأستاذ فضولنا بسؤال عميق حول المعايير الأخلاقية في التطور التكنولوجي. وساهم زملاء من خلفيات ثقافية متنوعة بوجهات نظر مختلفة، محولين القاعة لمختبر أفكار نابض. الحياة الجامعية لا تعلمنا ماذا نفكر فقط، بل كيف نحلل بنقد وموضوعية."},
            "اكتب فقرة من 5 أسطر في كراستك عن تخصصك الدراسي المفضل ولماذا تود التعمق فيه بالإنجليزية."
        ),
        (
            26, "Telecommunications, Remote Collaboration & Calls", "المكالمات الهاتفية والتواصل الرقمي عن بُعد",
            "إجراء المكالمات الرسمية وغير الرسمية، إرسال الرسائل الصوتية، والاجتماعات الافتراضية.",
            [("Connect", "C-O-NN-E-C-T", "يتصل"), ("Message", "M-E-SS-A-G-E", "رسالة"), ("Virtual", "V-I-R-T-U-A-L", "افتراضي"), ("Signal", "S-I-G-N-A-L", "إشارة/شبكة"), ("Respond", "R-E-S-P-O-N-D", "يرد/يستجيب"), ("Network", "N-E-T-W-OR-K", "شبكة")],
            [("Good afternoon, could you please connect me with customer support?", "مساء الخير، هل يمكنك من فضلك تحويلي لقسم الدعم الفني؟"), ("I am leaving a concise voice note to update you on our progress.", "أترك رسالة صوتية موجزة لإحاطتك بآخر المستجدات."), ("Our team is holding a virtual conference call tomorrow at two.", "يعقد فريقنا مكالمة مؤتمرية افتراضية غداً في الثانية ظهرًا."), ("Pardon me, your audio signal cut out for a brief second.", "عذراً، انقطع صوتك لثانية وجيزة."), ("Thank you for following up so promptly by email.", "شكراً لك على المتابعة السريعة عبر البريد الإلكتروني.")],
            {"title": "The Evolution of Global Connection", "text": "Modern telecommunications have fundamentally collapsed physical distances, allowing instantaneous collaboration across continents. A software developer in Cairo can coordinate in real time with design teams in Tokyo and New York through seamless video conferences. However, mastering digital etiquette—such as speaking with deliberate clarity and active listening—remains paramount for effective international dialogue.", "translation_ar": "لقد ألغت الاتصالات الحديثة المسافات الجغرافية تماماً، متيحة تعاوناً فورياً عبر القارات. يستطيع مطور برمجيات في القاهرة أن ينسق في الوقت الحقيقي مع فرق تصميم في طوكيو ونيويورك عبر مكالمات فيديو سلسة. ومع ذلك، فإن إتقان آداب التواصل الرقمي—مثل التحدث بوضوح والاستماع النشط—يظل أمراً أساسياً للحوار الدولي الفعال."},
            "اكتب نص مكالمة هاتفية رسمية تطلب فيها تحديد موعد مقابلة عمل مع شركة دولية."
        ),
        (
            27, "Professions, Careers & the Modern Workplace", "المهن، بيئة العمل والمسارات المهنية",
            "المصطلحات المهنية، وصف الوظائف، ومسؤوليات فرق العمل في الشركات والمؤسسات.",
            [("Career", "C-A-R-EE-R", "مسار مهني"), ("Manager", "M-A-N-A-G-ER", "مدير"), ("Colleague", "C-O-LL-EA-G-UE", "زميل عمل"), ("Productive", "P-R-O-D-U-C-T-I-V-E", "مُنتج"), ("Challenge", "CH-A-LL-E-N-G-E", "تحدٍ"), ("Leadership", "L-EA-D-ER-SH-I-P", "قيادة")],
            [("She thrives in collaborative and creative workplace environments.", "هي تبدع وتزدهر في بيئات العمل التعاونية والمبتكرة."), ("Effective leaders inspire their colleagues rather than dictate orders.", "القادة الفعالون يلهمون زملاءهم بدلاً من مجرد إملاء الأوامر."), ("Balancing ambitious career milestones with personal well-being is vital.", "الموازنة بين أهداف العمل الطموحة والراحة الشخصية أمر حيوي."), ("Our department consistently delivers high-quality projects on schedule.", "يقدم قسمنا مشاريع عالية الجودة بانتظام وفي مواعيدها المحددة."), ("Continuous upskilling ensures long-term professional relevance.", "الارتقاء المستمر بالمهارات يضمن استمرارية النجاح المهني على المدى الطويل.")],
            {"title": "Thriving in the 21st Century Workplace", "text": "The contemporary workplace is evolving at unprecedented speed, placing a high premium on agility and emotional intelligence. Technical proficiency alone is no longer sufficient; professionals must communicate cross-culturally and resolve intricate disputes diplomatically. When organizations nurture an inclusive atmosphere where every team member feels valued, groundbreaking innovation inevitably blossoms.", "translation_ar": "بيئة العمل المعاصرة تتطور بسرعة غير مسبوقة، واضعة قيمة كبرى للمرونة والذكاء العاطفي. لم تعد الكفاءة التقنية وحدها كافية؛ بل يتعين على المهنيين التواصل عبر الثقافات وحل النزاعات المعقدة بدبلوماسية. وعندما ترعى المؤسسات أجواء يشعر فيها كل فرد بالتقدير، فإن الابتكار يزدهر حتماً."},
            "اكتب فقرة من 5 أسطر في كراستك عن مهنة أحلامك والمهارات التي تحتاج لتطويرها لتحقيقها."
        ),
        (
            28, "Diplomatic Disagreement & Persuasive Requests", "إبداء الرأي، الطلب بلباقة والاختلاف الراقي",
            "فنون الإقناع والتفاوض اللطيف والتعبير عن الاختلاف في وجهات النظر باحترافية.",
            [("Opinion", "O-P-I-N-I-ON", "رأي"), ("Respect", "R-E-S-P-E-C-T", "احترام"), ("Disagree", "D-I-S-A-G-R-EE", "يختلف بالرأي"), ("Persuade", "P-ER-S-UA-D-E", "يقنع"), ("Polite", "P-O-L-I-T-E", "مهذب"), ("Alternative", "A-L-T-ER-N-A-T-I-V-E", "بديل")],
            [("I appreciate your viewpoint, although I look at the issue somewhat differently.", "أقدر وجهة نظرك، رغم أنني أنظر للأمر من زاوية مختلفة قليلاً."), ("Would you consider exploring an alternative methodology that saves resources?", "هل تتكرم بدراسة منهجية بديلة توفر الموارد؟"), ("Healthy debate elevates mutual understanding and produces superior decisions.", "النقاش البناء يرتقي بالفهم المتبادل ويثمر قرارات أفضل."), ("I see your point clearly; however, we must also consider potential risks.", "أتفهم نقطتك بوضوح؛ غير أنه يتعين علينا أيضاً مراعاة المخاطر المحتملة."), ("Expressing courtesy under pressure reflects true emotional maturity.", "الحفاظ على اللباقة تحت الضغوط يعكس نضجاً عاطفياً حقيقياً.")],
            {"title": "The Gentle Art of Diplomatic Discourse", "text": "Disagreement is a natural facet of human interaction; the distinction lies in how we voice it. Blunt confrontation breeds defensiveness, whereas diplomatic discourse builds bridges of mutual respect. By prefacing critiques with empathetic acknowledgment—phrases such as 'I understand your perspective'—we invite open collaboration rather than conflict. True wisdom shines when we argue to discover truth rather than win applause.", "translation_ar": "الاختلاف في الرأي مظهر طبيعي للتفاعل البشري؛ والفارق يكمن في كيفية التعبير عنه. المواجهة الفجة تخلق دفاعية وتصلباً، بينما الحوار الدبلوماسي يبني جسوراً من الاحترام المتبادل. ومن خلال بدء الملاحظات بتقدير وجهة نظر الطرف الآخر، فإننا ندعو للتعاون المنفتح بدلاً من الصدام. تلمع الحكمة الحقيقية عندما نناقش لاكتشاف الحقيقة لا لكسب التصفيق."},
            "اكتب حواراً بين طرفين يختلفان في الرأي باحترام شديد حول طريقة تنفيذ مشروع مدرسي."
        ),
        (
            29, "International Travel, Airports & Border Crossing", "السفر والمطارات والإجراءات الجمركية والفنادق",
            "المحادثات في صالات السفر، ختم الجوازات، تفتيش الأمتعة، وحجز الفنادق العالمية.",
            [("Passport", "P-A-SS-P-OR-T", "جواز سفر"), ("Flight", "F-L-IGH-T", "رحلة طيران"), ("Luggage", "L-U-GG-A-G-E", "أمتعة"), ("Customs", "C-U-S-T-O-M-S", "جمارك"), ("Boarding", "B-O-AR-D-I-NG", "صعود الطائرة"), ("Destination", "D-E-S-T-I-N-A-T-I-ON", "وجهة السفر")],
            [("May I please see your passport and international boarding pass?", "هل يمكنني رؤية جواز سفرك وبطاقة صعود الطائرة من فضلك؟"), ("Our non-stop flight to London will commence boarding in twenty minutes.", "ستبدأ رحلتنا المباشرة للندن بصعود الركاب خلال عشرين دقيقة."), ("I have a reservation under the name Ahmed for three nights.", "لدي حجز فندقي باسم أحمد لمدة ثلاث ليالٍ."), ("Could you help me locate the luggage carousel for flight BA402?", "هل يمكنك مساعدتي في تحديد سير استلام الأمتعة للرحلة BA402؟"), ("Do you have any items to declare to the customs inspection authority?", "هل لديك أي مقتنيات تود الإفصاح عنها لجمارك التفتيش؟")],
            {"title": "An Arrival at Heathrow Airport", "text": "After a smooth six-hour flight, our aircraft touched down on the bustling runway of London Heathrow. I proceeded towards border control, holding my documents neatly prepared. The immigration officer smiled and inquired, 'What is the purpose of your visit to the United Kingdom?' I replied calmly, 'I am attending an international student leadership conference.' He stamped my passport and said warmly, 'Welcome to Britain!'", "translation_ar": "بعد رحلة طيران سلسة استغرقت ست ساعات، هبطت طائرتنا على مدرج مطار هيثرو المزدحم بلندن. توجهت نحو مراقبة الجوازات حاملاً وثائقي مجهزة بدقة. ابتسم ضابط الهجرة وسأل: 'ما هو الغرض من زيارتك للمملكة المتحدة؟'. أجبت بكل هدوء: 'أشارك في مؤتمر دولي لقيادات الطلاب.' ختم جواز سفري وقال بود: 'أهلاً بك في بريطانيا!'."},
            "اكتب حواراً كاملاً بين مسافر وموظف الجوازات في مطار دولي باللغة الإنجليزية."
        ),
        (
            30, "Expressive Storytelling & Narrative Sequences", "سرد القصص والتتابع الزمني المعبر",
            "إتقان أدوات الربط الزمني (First, Meanwhile, Suddenly, Eventually) لسرد حكايات شيقة.",
            [("Narrative", "N-A-RR-A-T-I-V-E", "سرد قصصي"), ("Suddenly", "S-U-DD-E-N-L-Y", "فجأة"), ("Meanwhile", "M-EA-N-WH-I-L-E", "في هذه الأثناء"), ("Eventually", "E-V-E-N-T-UA-LL-Y", "في نهاية المطاف"), ("Dramatic", "D-R-A-M-A-T-I-C", "درامي/مثير"), ("Resolution", "R-E-S-O-L-U-T-I-ON", "خاتمة/حل")],
            [("First, the morning sky turned a dramatic shade of amber.", "أولاً، تحولت سماء الصباح إلى درجة عنبرية مثيرة."), ("Suddenly, a gentle rustling sound emerged from the deep pine forest.", "وفجأة، صدر صوت حفيف لطيف من أعماق غابة الصنوبر."), ("Meanwhile, the adventurous villagers prepared their lanterns for the expedition.", "في هذه الأثناء، أعد القرويون المغامرون فوانيسهم للرحلة الاستكشافية."), ("Eventually, the lost traveler discovered a welcoming shelter atop the ridge.", "وفي نهاية المطاف، وجد المسافر التائه مأوى مرحباً فوق التل."), ("Every great story teaches us perseverance in the face of uncertainty.", "كل قصة عظيمة تعلمنا المثابرة في مواجهة المجهول.")],
            {"title": "The Lighthouse Keeper's Lantern", "text": "A fierce tempest was battering the rocky coastline as night descended. Inside the ancient stone lighthouse, old Thomas noticed that the primary beacon had abruptly extinguished. Knowing that fishing vessels were navigating through treacherous waters, he did not panic. First, he gathered his tools and ascended the steep spiral staircase. Meanwhile, torrential waves crashed against the foundation. With steady hands and unwavering resolve, he repaired the generator. Moments later, the brilliant beam pierced through the darkness, guiding every sailor safely home.", "translation_ar": "كانت عاصفة هوجاء تضرب الساحل الصخري مع حلول الليل. وداخل المنارة الحجرية العتيقة، لاحظ العجوز توماس أن الضوء الرئيسي قد انطفأ فجأة. ولعلمه بأن قوارب الصيد تبحر في مياه خطرة، لم يصب بالهلع. أولاً، جمع أدواته وصعد الدرج الحلزوني الحاد. وفي هذه الأثناء، كانت الأمواج العاتية تصطدم بالقواعد الحجرية. وبأيدٍ ثابتة وعزيمة راسخة، أصلح المولد. وبعد لحظات، اخترق الشعاع الوضّاء الظلام الدامس، مرشداً كل بحار بأمان نحو الوطن."},
            "اكتب قصة قصيرة في كراستك من 7 أسطر تحتوي على: Suddenly, Meanwhile, Eventually."
        )
    ]

    for num, title, subtitle, desc, words_raw, sents_raw, passage, hw in stage3:
        levels.append({
            "level_number": num,
            "stage": 3,
            "stage_name": "المرحلة 3: الطلاقة التعبيرية والأزمنة (Expressive Fluency & Grammar)",
            "level_type": "sentences_to_paragraphs",
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": desc,
            "icon": "book-open",
            "letters": [{"symbol": w[0][:3].upper(), "sound": f"/{w[0][:3].lower()}/", "name": w[0], "sound_name": w[0], "arabic_desc": w[2]} for w in words_raw[:4]],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_raw],
            "sentences": [{"text": s[0], "translation_ar": s[1]} for s in sents_raw],
            "passage": passage,
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"مرحباً بك في المستوى {num}! هدفك اليوم هو بناء فقرات وسرد أفكار متسلسلة حول {subtitle}."
        })

    # =========================================================================
    # STAGE 4: LEVELS 31 - 40 (المقالات التحليلية والمناقشات الفكرية)
    # =========================================================================
    stage4 = [
        (
            31, "Conditionals & Exploring Hypothetical Scenarios", "الجمل الشرطية واستكشاف الاحتمالات",
            "استخدام الأزمنة الشرطية (If clauses 1, 2, 3) لمناقشة البدائل والخيارات المستقبلية.",
            [("Condition", "C-O-N-D-I-T-I-ON", "شرط"), ("Imagine", "I-M-A-G-I-N-E", "يتخيل"), ("Consequence", "C-O-N-S-E-QU-E-N-C-E", "عاقبة/نتيجة"), ("Possibility", "P-O-SS-I-B-I-L-I-T-Y", "احتمال"), ("Reflect", "R-E-F-L-E-C-T", "يتأمل"), ("Hypothetical", "H-Y-P-O-TH-E-T-I-C-A-L", "افتراضي")],
            [("If you dedicate one hour daily, your fluency will soar tremendously.", "إذا خصصت ساعة يومياً، فستحلق طلاقتك اللغوية عالياً."), ("If I had the chance to travel back in time, I would study languages earlier.", "لو كانت لدي الفرصة للسفر بالزمن، لدرست اللغات في سن أصغر."), ("Unless we protect natural reserves, endangered species will disappear forever.", "ما لم نحمِ المحميات الطبيعية، فستنقرض الأنواع النادرة للأبد."), ("Were we to adopt solar energy fully, carbon emissions would plummet.", "لو أننا اعتمدنا الطاقة الشمسية بالكامل، لانخفضت الانبعاثات الكربونية بشدة."), ("Hypothetical inquiries illuminate hidden solutions to complex dilemmas.", "التساؤلات الافتراضية تكشف حلولاً خفية للمعضلات المعقدة.")],
            {"title": "The Power of the 'What If' Question", "text": "Throughout human history, breakthrough inventions have sprung from simple conditional inquiries: 'What if we could fly above the clouds?' or 'What if information could travel across oceans in fractions of a second?' By considering hypothetical alternatives, philosophers challenge obsolete dogmas and scientists formulate testable hypotheses. Exploring 'what if' expands the boundaries of human possibility.", "translation_ar": "على مدار التاريخ الإنساني، انبثقت الابتكارات الفارقة من تساؤلات شرطية بسيطة: 'ماذا لو استطعنا الطيران فوق السحاب؟' أو 'ماذا لو استطاعت المعلومات السفر عبر المحيطات في أجزاء من الثانية؟'. ومن خلال دراسة البدائل الافتراضية، يتحدى الفلاسفة الأفكار العقيمة ويصيغ العلماء فرضيات قابلة للاختبار. إن التساؤل بـ 'ماذا لو' يوسع حدود الإمكان البشري."},
            "اكتب 4 جمل شرطية باستخدام: If I study..., If I had known..., If we change..."
        ),
        (
            32, "Artificial Intelligence & the Digital Revolution", "الذكاء الاصطناعي والثورة الرقمية الحديثة",
            "قراءة ومناقشة مقالات التكنولوجيا المتقدمة وتأثير خوارزميات الذكاء الاصطناعي على مستقبل البشرية.",
            [("Intelligence", "I-N-T-E-LL-I-G-E-N-C-E", "ذكاء"), ("Algorithm", "A-L-G-O-R-I-TH-M", "خوارزمية"), ("Automation", "AU-T-O-M-A-T-I-ON", "أتمتة"), ("Ethics", "E-TH-I-C-S", "أخلاقيات"), ("Innovation", "I-NN-O-V-A-T-I-ON", "ابتكار"), ("Digital", "D-I-G-I-T-A-L", "رقمي")],
            [("Artificial intelligence is reshaping medicine, education, and global industries.", "الذكاء الاصطناعي يعيد تشكيل الطب والتعليم والصناعات العالمية."), ("Ethical guidelines are indispensable when deploying autonomous algorithms.", "المعايير الأخلاقية لا غنى عنها عند نشر الخوارزميات ذاتية التشغيل."), ("Machine learning models detect intricate patterns invisible to the naked human eye.", "نماذج التعلم الآلي تكتشف أنماطاً دقيقة خفية عن العين البشرية المجردة."), ("Automation should augment human creativity rather than displace compassion.", "ينبغي للأتمتة أن تعزز الإبداع البشري لا أن تحل محل التعاطف الإنساني."), ("The digital frontier invites responsible stewardship and lifelong curiosity.", "الآفاق الرقمية تدعو لرعاية مسؤولة وفضول معرفي مستمر.")],
            {"title": "The Symbiosis of Human Heart and Machine Mind", "text": "As computational power surges exponentially, society stands at an unprecedented crossroads. Artificial intelligence excels at processing colossal datasets and diagnosing anomalies with surgical precision. Yet, algorithms possess neither conscience nor empathy; they cannot weep with grief or beam with moral pride. The true frontier lies not in surrendering our humanity to silicon, but in harnessing intelligent tools to amplify education, alleviate human suffering, and democratize knowledge globally.", "translation_ar": "مع تسارع القوة الحاسوبية بشكل هائل، يقف المجتمع أمام مفترق طرق غير مسبوق. يتفوق الذكاء الاصطناعي في معالجة البيانات الضخمة وتشخيص الحالات بدقة جراحية. غير أن الخوارزميات لا تملك ضميراً ولا تعاطفاً؛ لا تستطيع البكاء حزناً أو الشعور بالفخر الأخلاقي. الأفق الحقيقي لا يكمن في التنازل عن إنسانيتنا للآلات، بل في توظيف الأدوات الذكية لتعزيز التعليم، وتخفيف المعاناة الإنسانية، وتعميم المعرفة على مستوى العالم."},
            "اكتب مقالاً تحليلياً من 8 أسطر في كراستك يناقش إيجابيات وسلبيات الذكاء الاصطناعي في التعليم."
        ),
        (
            33, "Environmental Stewardship & Climate Action", "حماية البيئة، الاستدامة والتحديات المناخية",
            "المفردات البيئية، الطاقة النظيفة، ومناقشة قضايا التغير المناخي والحلول البيئية العالمية.",
            [("Ecology", "E-C-O-L-O-G-Y", "علم البيئة"), ("Renewable", "R-E-N-EW-A-B-L-E", "متجدد"), ("Biodiversity", "B-I-O-D-I-V-ER-S-I-T-Y", "تنوع بيولوجي"), ("Preserve", "P-R-E-S-ER-V-E", "يحافظ على"), ("Sustainable", "S-U-S-T-AI-N-A-B-L-E", "مستدام"), ("Carbon", "C-AR-B-O-N", "كربون")],
            [("Transitioning to solar and wind energy is critical for ecological balance.", "التحول نحو الطاقة الشمسية وطاقة الرياح أمر حاسم للتوازن البيئي."), ("Preserving rainforests safeguards the planet's richest reservoir of biodiversity.", "حماية الغابات المطيرة يحفظ أغنى خزان للتنوع البيولوجي على الكوكب."), ("Sustainable agriculture minimizes water consumption and restores degraded soils.", "الزراعة المستدامة تقلل استهلاك المياه وتستصلح التربة المتدهورة."), ("Every single citizen can contribute by reducing unnecessary single-use plastics.", "يمكن لكل مواطن أن يساهم بالحد من استخدام البلاستيك أحادي الاستعمال."), ("We do not inherit the Earth from ancestors; we borrow it from our children.", "نحن لا نرث الأرض من أجدادنا؛ بل نستعيرها من أبنائنا.")],
            {"title": "Guardians of the Living Earth", "text": "Our fragile planet is a magnificent tapestry where every living organism plays an indispensable ecological role. From the microscopic phytoplankton generating oxygen in marine depths to ancient oak forests purifying atmospheric air, nature maintains an exquisite equilibrium. Yet, industrial emissions and environmental degradation threaten this delicate balance. Championing sustainable technologies and restoring green habitats are not optional luxuries; they are moral duties to safeguard our shared future.", "translation_ar": "كوكبنا الهش نسيج بديع يؤدي فيه كل كائن حي دوراً بيئياً لا غنى عنه. فمن العوالق النباتية المجهرية التي تولد الأكسجين في أعماق البحار إلى غابات البلوط العتيقة التي تنقي الهواء، تحافظ الطبيعة على توازن رائع. غير أن الانبعاثات الصناعية والتدهور البيئي يهددان هذا التوازن الدقيق. إن تبني التقنيات المستدامة واستعادة المساحات الخضراء ليست رفاهية اختيارية، بل واجب أخلاقي لحماية مستقبلنا المشترك."},
            "اكتب مقالاً من 8 أسطر عن 3 خطوات يمكن للفرد اتخاذها لتقليل التلوث البيئي في مدينته."
        ),
        (
            34, "Comparative Analysis & Philosophical Contrasts", "المقارنة النقدية والتحليل الفلسفي للأفكار",
            "المقارنة المتعمقة بين النظم والأفكار الفلسفية باستخدام أدوات المقارنة المتقدمة.",
            [("Contrast", "C-O-N-T-R-A-S-T", "تباين/مفارقة"), ("Analogy", "A-N-A-L-O-G-Y", "قياس/مماثلة"), ("Distinction", "D-I-S-T-I-N-C-T-I-ON", "فارق جوهري"), ("Criterion", "C-R-I-T-ER-I-ON", "معيار"), ("Evaluate", "E-V-A-L-UA-T-E", "يقيم"), ("Superior", "S-U-P-ER-I-OR", "أعلى/أسمى")],
            [("In contrast to transient wealth, profound knowledge endures through generations.", "على النقيض من الثروة الزائلة، فإن المعرفة العميقة تدوم عبر الأجيال."), ("Examining competing economic models reveals complementary strengths and liabilities.", "دراسة النماذج الاقتصادية المتنافسة يكشف عن نقاط قوة ونقاط ضعف متكاملة."), ("A crucial distinction exists between mere information and authentic wisdom.", "يوجد فارق جوهري حاسم بين مجرد المعلومات المجردة والحكمة الحقيقية."), ("We must evaluate policies based on long-term benefits rather than immediate popularity.", "يتعين علينا تقييم السياسات بناءً على فوائدها بعيدة المدى لا شعبيتها اللحظية."), ("Clear analogies bridge abstract concepts with tangible daily experiences.", "التشبيهات الدقيقة تربط بين المفاهيم المجردة والخبرات الحياتية الملموسة.")],
            {"title": "Information versus Wisdom", "text": "In the modern age of digital saturation, society is bombarded with unprecedented torrents of information. With a simple tap on our smartphones, we access billions of facts, charts, and news updates. However, information is merely the raw raw building material; wisdom is the architect that organizes it towards noble ends. While information answers 'What is it?', wisdom inquires 'Why does it matter?' and 'How does it benefit humanity?' Pursuing wisdom is the higher calling.", "translation_ar": "في العصر الحديث المشبع رقمياً، يتعرض المجتمع لطوفان غير مسبوق من المعلومات. وبلمسة بسيطة على هواتفنا، نصل لمليارات الحقائق والرسوم البيانية والأخبار. ومع ذلك، فإن المعلومات مجرد مادة خام؛ بينما الحكمة هي المهندس المعماري الذي يوجهها نحو الغايات النبيلة. ففي حين تسأل المعلومة 'ما هذا؟'، تسأل الحكمة 'لماذا يهم هذا؟' و'كيف يفيد الإنسانية؟'. السعي وراء الحكمة هو المطلب الأسمى."},
            "اكتب مقالاً مقارناً في كراستك يوضح الفرق بين 'المعلومات' و'الحكمة' في 6 أسطر."
        ),
        (
            35, "Cultural Nuances, Traditions & Global Identity", "التنوع الثقافي، التراث والهوية الإنسانية المشتركة",
            "قراءة متقدمة حول العولمة، الحفاظ على الهوية الأصيلة، واحترام التنوع الحضاري.",
            [("Culture", "C-U-L-T-U-R-E", "ثقافة"), ("Heritage", "H-E-R-I-T-A-G-E", "تراث"), ("Identity", "I-D-E-N-T-I-T-Y", "هوية"), ("Diversity", "D-I-V-ER-S-I-T-Y", "تنوع"), ("Tradition", "T-R-A-D-I-T-I-ON", "تقليد/عرف"), ("Harmony", "H-AR-M-O-N-Y", "تناغم/انسجام")],
            [("Cultural heritage anchors human dignity amidst the tides of rapid globalization.", "التراث الثقافي يرسخ الكرامة الإنسانية وسط أمواج العولمة المتسارعة."), ("Appreciating diverse customs enriches our collective understanding of human nature.", "تقدير العادات المتنوعة يثري فهمنا الجماعي للطبيعة البشرية."), ("Language is the sacred vessel carrying the folklore, poetry, and soul of a nation.", "اللغة هي الوعاء المقدس الذي يحمل الفولكلور والشعر وروح الأمة."), ("True global citizenship celebrates unique roots while fostering international solidarity.", "المواطنة العالمية الحقيقية تحتفي بالجذور الفريدة مع تعزيز التضامن الدولي."), ("Harmonious societies view differences as vibrant colors on a single magnificent canvas.", "المجتمعات المتناغمة تنظر للاختلافات كألوان زاهية على لوحة واحدة بديعة.")],
            {"title": "The Mosaic of Human Heritage", "text": "Human civilization resembles an exquisite mosaic, where each distinct culture represents an irreplaceable colored tile. When we listen to Bedouin poetry beneath desert stars, or contemplate traditional East Asian tea rituals, we glimpse varied expressions of identical yearnings: love, honor, belonging, and awe. Learning another language does not erode your mother tongue; rather, it provides a second lens to appreciate the beauty of human heritage.", "translation_ar": "تشبه الحضارة الإنسانية فسيفساء بديعة، تمثل فيها كل ثقافة فريدة قطعة حجرية ملونة لا تعوض. عندما نستمع للشعر البدوي تحت نجوم الصحراء، أو نتأمل طقوس الشاي التقليدية في شرق آسيا، نلمح تعبيرات متنوعة لنفس الأشواق الإنسانية: الحب، الشرف، الانتماء، والدهشة. إن تعلم لغة ثانية لا يطمس لغتك الأم؛ بل يمنحك عدسة ثانية لتقدير جمال التراث الإنساني."},
            "اكتب مقالاً بالإنجليزية من 8 أسطر تشرح فيه لزميل أجنبي ملمحاً أصيلاً ومميزاً من ثقافتك العربية."
        ),
        (
            36, "Mastery of Figurative Language & Idiomatic Nuance", "التعبيرات الاصطلاحية والمجازية في الإنجليزية",
            "فك شفرات الأمثال والمصطلحات الدارجة (Idioms & Metaphors) التي يستخدمها المتحدث الأصلي يومياً.",
            [("Idiom", "I-D-I-O-M", "تعبير اصطلاحي"), ("Metaphor", "M-E-T-A-P-H-OR", "استعارة مجازية"), ("Nuance", "N-U-A-N-C-E", "فارق دقيق"), ("Figurative", "F-I-G-U-R-A-T-I-V-E", "مجازي"), ("Context", "C-O-N-T-EX-T", "سياق الكلام"), ("Eloquence", "E-L-O-QU-E-N-C-E", "بلاغة وفصاحة")],
            [("To cut corners in architecture invariably leads to disastrous structural failures.", "اتباع الطرق المختصرة والتهاون في المعمار يؤدي حتماً لانهيارات كارثية."), ("When negotiations reached an impasse, his diplomatic humor broke the ice.", "عندما وصلت المفاوضات لطريق مسدود، نجحت دعابته الدبلوماسية في إذابة الجليد."), ("Reading literature enables us to read between the lines with sharp intuition.", "قراءة الأدب تمكننا من قراءة ما بين السطور بحدس وبديهة حادة."), ("Let us not beat around the bush; we must address the root cause directly.", "دعونا لا نلف وندور حول الموضوع؛ بل نواجه السبب الجذري مباشرة."), ("Idioms are cultural footprints embedded within everyday vernacular speech.", "التعبيرات الاصطلاحية هي بصمات ثقافية مغروسة في صلب الكلام الدارج.")],
            {"title": "Behind the Literal Words", "text": "To a novice language learner, idioms can present baffling riddles. Hearing someone remark that an examination was 'a piece of cake' or that they are 'feeling under the weather' might provoke comical confusion if translated word-for-word. Yet, these colorful metaphors are the living marrow of everyday English. They convey shared cultural humor, historical memories, and vivid imagery that sterile literal phrasing could never capture.", "translation_ar": "بالنسبة للمتعلم المبتدئ، قد تبدو التعبيرات الاصطلاحية ألغازاً محيرة. فسماع شخص يقول إن الاختبار كان 'قطعة كعك' (سهلاً جداً) أو أنه 'يشعر تحت الطقس' (متوعك صحياً) قد يثير حيرة مضحكة لو تُرجمت حرفياً. ومع ذلك، فإن هذه الاستعارات الملونة هي النخاع الحي للغة الإنجليزية اليومية؛ فهي تنقل دعابة ثقافية وذكريات وصوراً لا يمكن للترجمة الحرفية الجافة أن تنقلها."},
            "اكتب 4 جمل موظفاً فيها 4 تعبيرات اصطلاحية: Break the ice, Piece of cake, Under the weather, Beat around the bush."
        ),
        (
            37, "Phrasal Verbs Mastery in Spoken & Written Context", "الأفعال المركبة المتقدمة وسياقات استخدامها",
            "التمكن من الأفعال المركبة الشائعة (Look forward to, Bring about, Turn down, Figure out).",
            [("Phrasal", "P-H-R-A-S-A-L", "مركب/شبه جملي"), ("Combine", "C-O-M-B-I-N-E", "يدمج"), ("Meaning", "M-EA-N-I-NG", "معنى"), ("Interact", "I-N-T-ER-A-C-T", "يتفاعل"), ("Resolve", "R-E-S-O-L-V-E", "يحل/يحسم"), ("Structure", "S-T-R-U-C-T-U-R-E", "بنية/تركيب")],
            [("Scientists are working tirelessly to figure out the mysteries of deep ocean trenches.", "يعمل العلماء بلا كلل لفك ألغاز خنادق المحيطات العميقة."), ("I genuinely look forward to attending the international innovation symposium.", "أتطلع بشغف حقيقي لحضور مؤتمر الابتكار الدولي."), ("The diplomatic committee helped bring about historic accords between neighbors.", "ساعدت اللجنة الدبلوماسية في إحداث اتفاقيات تاريخية بين الجيران."), ("Never turn down an opportunity that challenges your intellectual growth.", "إياك أن ترفض فرصة تتحدى نموك الفكري وتصقل عقلك."), ("Phrasal verbs grant your speech the natural musicality of native speakers.", "الأفعال المركبة تمنح كلامك تلك النغمة الطبيعية التي يتحدث بها أهل اللغة.")],
            {"title": "The Dynamic Elasticity of English Verbs", "text": "One of the most distinctive features of the English language is its capacity to transform a simple verb by pairing it with prepositions. Consider the verb 'take': combined with 'off', it describes an aircraft ascending; with 'up', it signifies adopting a hobby; with 'over', it denotes assuming leadership. Mastering these combinations is the definitive bridge from academic rigidity to natural, intuitive speech.", "translation_ar": "إحدى أبرز سمات اللغة الإنجليزية هي قدرتها على تحويل معنى الفعل البسيط بمجرد دمجه مع حروف الجر. تأمل الفعل 'take': فبإضافة 'off' يصف إقلاع الطائرة؛ ومع 'up' يعني البدء بهواية؛ ومع 'over' يعني تولي القيادة. إن إتقان هذه التراكيب هو الجسر الحقيقي للعبور من الجفاف الأكاديمي إلى الكلام الطبيعي والعفوي."},
            "اكتب فقرة من 5 أسطر في كراستك تحتوي على 3 أفعال مركبة مع وضع خط تحتها."
        ),
        (
            38, "Professional Interviewing, Pitching & Executive Presentations", "المقابلات الشخصية، التقديم الاحترافي والخطاب التنفيذي",
            "إتقان المقابلات الوظيفية بالإنجليزية، تقديم عروض تقديمية مقنعة، ومهارات إلقاء المصاعد (Elevator Pitch).",
            [("Executive", "EX-E-C-U-T-I-V-E", "تنفيذي"), ("Candidate", "C-A-N-D-I-D-A-T-E", "مرشح لوظيفة"), ("Strengths", "S-T-R-E-N-G-TH-S", "نقاط القوة"), ("Competence", "C-O-M-P-E-T-E-N-C-E", "كفاءة/جدارة"), ("Presentation", "P-R-E-S-E-N-T-A-T-I-ON", "عرض تقديمي"), ("Impact", "I-M-P-A-C-T", "أثر/تأثير")],
            [("My core strength lies in translating complex analytical data into actionable strategies.", "تكمن نقطة قوتي المحورية في تحويل البيانات التحليلية المعقدة لخطط عمل ملموسة."), ("During my previous tenure, I spearheaded a team that increased productivity by forty percent.", "خلال عملي السابق، قدت فريقاً نجح في رفع الإنتاجية بنسبة أربعين بالمائة."), ("Could you describe the organizational culture and the key milestones for this role?", "هل يمكنك وصف ثقافة المؤسسة وأهم الأهداف المرحلية المطلوبة لهذا المنصب؟"), ("Confidence paired with humble competence creates an irresistible executive presence.", "الثقة المقترنة بالكفاءة المتواضعة تخلق حضوراً قيادياً لا يقاوم."), ("Deliver your core value proposition with crystal precision in the opening minute.", "اطرح مقترح قيمتك الأساسي بدقة فائقة في الدقيقة الأولى من العرض.")],
            {"title": "Commanding the Interview Room", "text": "A high-stakes interview is not an interrogation; it is a collaborative exploration of mutual value. Exemplary candidates do not recite rehearsed memorizations; they narrate compelling stories of challenges overcome, lessons learned, and innovations implemented. By articulating your career trajectory with poise, active listening, and thoughtful counter-questions, you transform an interview into a partnership conversation.", "translation_ar": "المقابلة الوظيفية المهمة ليست استجواباً، بل استكشاف مشترك للقيمة المتبادلة. فالمرشحون المتميزون لا يرددون إجابات محفوظة عن ظهر قلب؛ بل يسردون قصصاً مشوقة عن تحديات تم تجاوزها، ودروس تم تعلمها، وابتكارات تم تطبيقها. ومن خلال التعبير عن مسارك المهني باتزان واستماع نشط وأسئلة ذكية، تحول المقابلة إلى حوار شراكة راقٍ."},
            "اكتب ردك بالإنجليزية على أشهر سؤال في المقابلات: 'Tell me about yourself and your greatest strength.'"
        ),
        (
            39, "Critical Thinking, Fallacy Detection & Logical Rigor", "التفكير النقدي، تفنيد المغالطات وبناء الحجج المنطقية",
            "قراءة المقالات الفلسفية، اكتشاف المغالطات المنطقية، وبناء الحجج السليمة معرفياً.",
            [("Logical", "L-O-G-I-C-A-L", "منطقي"), ("Premise", "P-R-E-M-I-S-E", "مقدمة منطقية"), ("Fallacy", "F-A-LL-A-C-Y", "مغالطة منطقية"), ("Valid", "V-A-L-I-D", "صحيح منطقياً"), ("Rational", "R-A-T-I-O-N-A-L", "عقلاني"), ("Evidence", "E-V-I-D-E-N-C-E", "دليل/برهان")],
            [("A robust argument relies on verified empirical premises and sound logical deductions.", "تعتمد الحجة القوية على مقدمات تجريبية موثقة واستنتاجات منطقية سليمة."), ("Beware of emotional appeals disguised as factual evidence during public debates.", "احذر من الخطابات العاطفية المتنكرة في ثوب الأدلة الواقعية أثناء المناظرات."), ("Correlation does not necessarily imply direct causation between observed phenomena.", "الترابط الإحصائي لا يعني بالضرورة وجود علاقة سببية مباشرة بين الظواهر الملاحظة."), ("Intellectual honesty compels us to follow evidence wherever it logically leads.", "الأمانة الفكرية تجبرنا على اتباع الدليل أينما قادنا المنطق بكل شجاعة."), ("Challenging your own assumptions is the hallmark of genuine intellectual maturity.", "تحدي افتراضاتك الخاصة هو السمة المميزة للنضج الفكري الحقيقي.")],
            {"title": "The Shield of Rational Inquiry", "text": "In an era of hyper-information and sensationalized headlines, critical thinking serves as the cognitive armor of free citizens. Without logical scrutiny, we fall prey to circular reasoning, false dilemmas, and confirmation bias. Developing the disciplined habit of questioning assertions, verifying sources, and disentangling rhetoric from reality safeguards our intellectual freedom and fosters democratic integrity.", "translation_ar": "في عصر فيض المعلومات والعناوين المثيرة، يعمل التفكير النقدي كدرع معرفي للمواطنين الأحرار. وبدون الفحص المنطقي، نقع فريسة للاستدلال الدائري، والمفارقات الكاذبة، والانحياز التأكيدي. إن تنمية عادة التساؤل المنهجي، والتحقق من المصادر، وفصل البلاغة الخطابية عن الحقيقة الواقعية يحمي حريتنا الفكرية ويصون نزاهة المجتمع."},
            "اكتب مقالاً تحليلياً من 8 أسطر يشرح لماذا 'الارتباط لا يعني السببية' مع إعطاء مثال واقعي."
        ),
        (
            40, "Debating, Rhetoric & the Power of Persuasion", "المناظرات، البلاغة الكلاسيكية وفن الإقناع",
            "أدوات الإقناع الأرسطية الثلاث (Ethos, Pathos, Logos) وكيفية الفوز بالمناظرات بالإنجليزية.",
            [("Rhetoric", "R-H-E-T-O-R-I-C", "علم البلاغة"), ("Debate", "D-E-B-A-T-E", "مناظرة"), ("Ethos", "E-TH-O-S", "المصداقية الأخلاقية"), ("Logos", "L-O-G-O-S", "البرهان العقلي"), ("Pathos", "P-A-TH-O-S", "التأثير العاطفي"), ("Persuasive", "P-ER-S-UA-S-I-V-E", "مقنع")],
            [("Classical rhetoric harmonizes moral credibility, rational logic, and heartfelt empathy.", "البلاغة الكلاسيكية توفق بين المصداقية الأخلاقية، والبرهان العقلي، والتعاطف الصادق."), ("The winning debater disarms opposing counter-arguments before presenting their thesis.", "المناظر الفائز يفند حجج الخصم مسبقاً قبل طرح فرضيته الأساسية."), ("A resonant speech inspires listeners to transform conviction into concrete action.", "الخطاب المؤثر يلهم المستمعين لتحويل قناعاتهم إلى أفعال ملموسة على أرض الواقع."), ("Precision in language choices magnifies the persuasive gravity of your arguments.", "الدقة في انتقاء المفردات تعظم الثقل الإقناعي لحججك وبراهينك."), ("Truth delivered with gracious eloquence triumphs over aggressive dogmatism.", "الحقيقة التي تُقدم ببلاغة راقية تنتصر دائماً على التزمت العدواني.")],
            {"title": "The Triad of Persuasive Discourse", "text": "Over two millennia ago in Athens, Aristotle articulated the foundational pillars of persuasion. 'Ethos' establishes the speaker's moral authority and trustworthy character. 'Logos' furnishes rigorous logical reasoning supported by verifiable facts. 'Pathos' awakens noble passions in the hearts of listeners, forging an emotional bridge. When a communicator masterfully weaves these three elements, their words possess the power to shape history.", "translation_ar": "منذ أكثر من ألفي عام في أثينا، صاغ أرسطو الأركان الأساسية للإقناع. فالمصداقية 'Ethos' ترسي السلطة الأخلاقية والنزاهة للمتحدث. والبرهان 'Logos' يقدم استدلالاً منطقياً مدعوماً بالحقائق المثبتة. والعاطفة 'Pathos' توقظ المشاعر النبيلة في قلوب السامعين لتبني جسراً وجدانياً. وعندما ينسج المتحدث هذه العناصر الثلاثة باقتدار، تصبح لكلماته القدرة على صياغة مسار التاريخ."},
            "اكتب خطبة إقناعية قصيرة من 8 أسطر في كراستك تحث فيها الشباب على القراءة اليومية."
        )
    ]

    for num, title, subtitle, desc, words_raw, sents_raw, passage, hw in stage4:
        levels.append({
            "level_number": num,
            "stage": 4,
            "stage_name": "المرحلة 4: الاحتراف المتقدم والمقالات التحليلية (Analytical Essays & Rhetoric)",
            "level_type": "paragraphs_to_articles",
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": desc,
            "icon": "award",
            "letters": [{"symbol": w[0][:3].upper(), "sound": f"/{w[0][:3].lower()}/", "name": w[0], "sound_name": w[0], "arabic_desc": w[2]} for w in words_raw[:4]],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_raw],
            "sentences": [{"text": s[0], "translation_ar": s[1]} for s in sents_raw],
            "passage": passage,
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"مرحباً بك في المستوى المتقدم {num}! اليوم ستتعلم صياغة مقالات وتحليلات معمقة حول {subtitle}."
        })

    # =========================================================================
    # STAGE 5: LEVELS 41 - 50 (الطلاقة التامة والمقالات الفكرية العليا كالناطق الأصلي)
    # =========================================================================
    stage5 = [
        (
            41, "Advanced Cohesion, Transitional Flow & Discourse Connectors", "الربط البلاغي والاتساق النصي المعقد",
            "استخدام أدوات الربط المعقدة (Furthermore, On the contrary, Inadvertently, Inevitably) في كتابة المقالات الطويلة.",
            [("Cohesion", "C-O-H-E-S-I-ON", "اتساق/ترابط"), ("Transition", "T-R-A-N-S-I-T-I-ON", "انتقال سلس"), ("Furthermore", "F-U-R-TH-ER-M-OR-E", "علاوة على ذلك"), ("Inevitably", "I-N-E-V-I-T-A-B-L-Y", "حتماً ولابد"), ("Seamless", "S-EA-M-L-E-SS", "سلس بلا فجوات"), ("Discourse", "D-I-S-C-OU-R-S-E", "خطاب فكري")],
            [("Furthermore, recent empirical findings reinforce the foundational premise.", "علاوة على ذلك، تعزز النتائج التجريبية الحديثة الفرضية الأساسية."), ("Inadvertently overlooked variables can skew the validity of an entire study.", "المتغيرات التي يتم إغفالها دون قصد قد تخل بصحة دراسة بأكملها."), ("Inevitably, society must reckon with the moral ramifications of unchecked tech.", "حتماً، سيتعين على المجتمع مواجهة التبعات الأخلاقية للتكنولوجيا المتفلتة."), ("Seamless transitions weave disparate paragraphs into an unbroken intellectual tapestry.", "أدوات الربط السلسة تنسج الفقرات المنفصلة في نسيج فكري متصل بديع."), ("Notwithstanding intense headwinds, the diplomatic mission achieved its objective.", "على الرغم من الصعوبات العاتية، حققت البعثة الدبلوماسية هدفها المنشود.")],
            {"title": "The Architecture of Sophisticated Prose", "text": "Mastery of written expression is not measured by convoluted vocabulary, but by architectural coherence. Seamless transitional phrases serve as the invisible steel girders holding an essay together. When ideas flow logically—progressing effortlessly from premise to elaboration, antithesis, and synthesis—the reader is carried along an irresistible current of persuasion. Elevating prose requires meticulous sculpting of cadence, rhythm, and connective tissue.", "translation_ar": "إن إتقان التعبير الكتابي لا يقاس بالمفردات المعقدة المتكلفة، بل بالاتساق المعماري للأفكار. وتعمل أدوات الربط السلسة كالدعامات الفولاذية الخفية التي تشد المقال بمتانة. وعندما تتدفق الأفكار منطقياً—متدرجة من المقدمة إلى التوسيع، والاعتراض، والتوليف النهائي—يُحمل القارئ في تيار إقناع لا يقاوم. إن الارتقاء بالأسلوب يتطلب نحتاً دقيقاً للإيقاع والترابط اللفظي."},
            "اكتب مقالاً متماسكاً من 10 أسطر يستخدم 4 أدوات ربط متقدمة: Furthermore, Notwithstanding, Inevitably, On the contrary."
        ),
        (
            42, "Public Speaking, Oratory & Commanding the Stage", "الخطابة الجماهيرية والإلقاء الصوتي المؤثر",
            "التحكم في طبقات الصوت، الوقفات الدرامية، ومخاطبة الجماهير بالإنجليزية كقائد متحدث.",
            [("Oratory", "OR-A-T-OR-Y", "فن الخطابة"), ("Audience", "AU-D-I-E-N-C-E", "الجمهور"), ("Cadence", "C-A-D-E-N-C-E", "إيقاع صوتي"), ("Resonate", "R-E-S-O-N-A-T-E", "يتردد صداه"), ("Inspire", "I-N-S-P-I-R-E", "يلهم"), ("Presence", "P-R-E-S-E-N-C-E", "حضور/كاريزما")],
            [("A masterful orator wields deliberate silences as powerfully as spoken words.", "الخطيب المفوه يوظف الوقفات الصامتة بنفس قوة الكلمات المنطوقة."), ("Modulating your vocal cadence keeps listeners leaning in with rapt attention.", "تنويع النبرات الصوتية يبقي المستمعين مشدودين بانتباه كامل."), ("Speak from the crucible of conviction, and your message will resonate deeply.", "تحدث من أعماق قناعتك الحقيقية، وسيصل صوتك مدوياً لقلوب الجميع."), ("Authentic stage presence flows from serving the audience rather than seeking praise.", "الحضور المسرحي الحقيقي ينبع من الرغبة في خدمة الجمهور لا التماس المديح."), ("The human voice remains humanity's most potent instrument for global transformation.", "يظل الصوت البشري هو الأداة الأكثر تأثيراً على الإطلاق للتغيير في العالم.")],
            {"title": "The Resonant Platform", "text": "Stepping before an expectant assembly, an orator commands immense creative power. The auditorium falls hushed; hundreds of minds synchronize with the cadence of a single voice. Great speeches do not merely transmit data; they awaken latent courage, dissolve societal apathy, and mobilize communities toward collective transcendence. By harmonizing eye contact, deliberate pacing, and unshakeable sincerity, a speaker transforms an ordinary room into a sanctuary of shared purpose.", "translation_ar": "عندما يخطو الخطيب أمام حشد مترقب، فإنه يمتلك قوة إبداعية هائلة. يسود الصمت في القاعة؛ وتتناغم مئات العقول مع إيقاع صوت واحد. إن الخطب العظيمة لا تنقل معلومات مجردة فحسب؛ بل توقظ الشجاعة الكامنة، وتذيب اللامبالاة، وتستنفر المجتمعات نحو السمو الجماعي. ومن خلال التناغم بين التواصل البصري، والهدوء الواثق، والصدق المطلق، يحول المتحدث القاعة إلى صرح لهدف مشترك."},
            "اكتب نص خطبة افتتاحية من 10 أسطر تلقيها أمام مؤتمر عالمي للشباب في كراستك."
        ),
        (
            43, "Fast Connected Speech, Reductions & Native Listening", "النطق المتصل السريع وتفهم اللهجات الأصلية",
            "إتقان الإدغام والحذف الصوتي (Connected Speech, Elision, Assimilation) لفهم الأفلام والمحادثات السريعة دون ترجمة.",
            [("Connected", "C-O-NN-E-C-T-ED", "متصل"), ("Assimilation", "A-SS-I-M-I-L-A-T-I-ON", "إدغام صوتي"), ("Elision", "E-L-I-S-I-ON", "حذف صوتي"), ("Rhythm", "R-H-Y-TH-M", "إيقاع"), ("Natural", "N-A-T-U-R-A-L", "طبيعي"), ("Intuition", "I-N-T-U-I-T-I-ON", "حدس لغوي")],
            [("Native English rhythm is stress-timed rather than syllable-timed.", "إيقاع الإنجليزية الأصلي يعتمد على توقيت النبر لا توقيت المقاطع المنفصلة."), ("Phonetic reductions such as 'gonna' and 'wanna' reflect natural linguistic efficiency.", "الحذف الصوتي مثل gonna و wanna يعكس كفاءة لسانية طبيعية في الكلام العفوي."), ("Weak forms of function words allow content words to stand out prominently.", "الصيغ الضعيفة لأدوات الربط تسمح للكلمات المحورية بالبروز بوضوح."), ("Training your ear to recognize connected speech demystifies native dialogue.", "تدريب أذنك على تمييز الكلام المتصل يفك طلاسم الحوارات السريعة تماماً."), ("Speak fluidly by linking the final consonant of one word to the next vowel.", "تحدث بسلاسة عبر وصل الحرف الساكن الأخير بالصوت المتحرك في الكلمة التالية.")],
            {"title": "The Flowing River of Spoken English", "text": "Written English presents words as neat, isolated units divided by white spaces. Spoken English, however, behaves like a continuous flowing stream. Words meld together through assimilation, weak vowels dissolve, and consonants leap across boundaries. Understanding that native speakers naturally economize vocal energy unlocks the secret to listening comprehension. Once you stop listening for isolated words and begin tuning into rhythmic beats, clarity emerges effortlessly.", "translation_ar": "تقدم الإنجليزية المكتوبة كلماتها كوحدات مرتبة ومنفصلة بمساحات بيضاء. أما الإنجليزية المنطوقة، فتعمل كنهر جارٍ مستمر. تندمج الكلمات بالإدغام، وتذوب الحركات الضعيفة، وتقفز الحروف الساكنة عبر الحدود اللفظية. إن إدراك أن المتحدث الأصلي يقتصد في طاقته الصوتية بصورة طبيعية يفتح لك سر الاستيعاب السمعي الخارق. وبمجرد أن تتوقف عن الاستماع للكلمات المنفردة وتبدأ بالاستماع للنبرات الإيقاعية، يظهر الوضوح بلا عناء."},
            "اكتب فقرة توضح فيها كيف يتحول 'What do you want to do?' في النطق المتصل إلى 'Whaddya wanna do?' مع تحليل النبر."
        ),
        (
            44, "Literary Analysis, Poetry & Metaphorical Subtlety", "التحليل الأدبي، قراءة الشعر وتذوق الجماليات",
            "قراءة نصوص من الأدب الإنجليزي الكلاسيكي والحديث، واستيعاب الرمزية والجماليات البلاغية.",
            [("Literary", "L-I-T-ER-A-R-Y", "أدبي"), ("Symbolism", "S-Y-M-B-O-L-I-S-M", "رمزية"), ("Allegory", "A-LL-E-G-O-R-Y", "رمزية مجازية"), ("Resonance", "R-E-S-O-N-A-N-C-E", "صدى شعوري"), ("Aesthetic", "A-E-S-TH-E-T-I-C", "جمالي"), ("Profound", "P-R-O-F-OU-N-D", "عميق")],
            [("Great literature holds a mirror up to the profound complexities of human existence.", "الأدب الرفيع يرفع مرآة كاشفة أمام التعقيدات العميقة للوجود الإنساني."), ("The poet's evocative symbolism portrays the relentless passage of transient time.", "رمزية الشاعر المعبرة تصور التدفق الذي لا يهدأ للوقت والزمن الزائل."), ("Subtle allegories communicate timeless moral truths across centuries of history.", "الرموز الأدبية الدقيقة تنقل حقائق أخلاقية خالدة عبر قرون التاريخ."), ("Analyzing poetic meters unveils the heartbeat hidden within human language.", "تحليل البحور الشعرية يكشف عن نبض القلب الخبيء داخل اللغة البشرية."), ("To read deeply is to dwell in the minds of the world's greatest thinkers.", "أن تقرأ بعمق يعني أن تسكن عقول أعظم مفكري العالم عبر العصور.")],
            {"title": "The Eternal Echoes of Literature", "text": "In the immortal plays of Shakespeare and the stirring verses of the romantic poets, language reaches the zenith of its expressive majesty. Literature is not an academic diversion; it is the collective diary of the human species. When we analyze how a solitary metaphor can illuminate sorrow, redemption, or transcendent love, we expand our own emotional and linguistic frontiers. Great writing does not expire with the author; it reverberates eternally across human hearts.", "translation_ar": "في مسرحيات شكسبير الخالدة وأبيات شعراء الرومانسية المؤثرة، تبلغ اللغة ذروة مجدها التعبيري. الأدب ليس مجرد ترف أكاديمي، بل هو المذكرات الجماعية للنوع البشري. وعندما نحلل كيف يمكن لاستعارة واحدة أن تسلط الضوء على الحزن أو الخلاص أو الحب السامي، فإننا نوسع آفاقنا الشعورية واللغوية. الكتابة العظيمة لا تموت بموت صاحبها؛ بل تتردد أصداؤها للأبد في قلوب البشر."},
            "اكتب مقالاً تحليلياً من 8 أسطر يحلل بيتاً شعرياً أو حكمة أدبية إنجليزية باللغة الإنجليزية."
        ),
        (
            45, "High-Stakes Negotiation, Diplomacy & Conflict Resolution", "التفاوض الدولي، الدبلوماسية وحل النزاعات",
            "إدارة المفاوضات المعقدة باللغة الإنجليزية، صياغة الاتفاقيات، ونزع فتيل التوتر الدولي والتجاري.",
            [("Negotiate", "N-E-G-O-T-I-A-T-E", "يفاوض"), ("Diplomacy", "D-I-P-L-O-M-A-C-Y", "دبلوماسية"), ("Resolution", "R-E-S-O-L-U-T-I-ON", "حل/تسوية"), ("Compromise", "C-O-M-P-R-O-M-I-S-E", "حل وسط"), ("Consensus", "C-O-N-S-E-N-S-U-S", "إجماع/توافق"), ("Mediate", "M-E-D-I-A-T-E", "يتوسط")],
            [("Principled negotiation seeks mutual value rather than adversarial domination.", "التفاوض المبني على المبادئ يسعى للقيمة المشتركة لا الهيمنة الإقصائية."), ("A skilled mediator listens to underlying interests rather than stubborn positional claims.", "الوسيط الماهر ينصت للمصالح الجوهرية لا للمواقف الشكلية المتصلبة."), ("Drafting unambiguous contractual terms prevents future jurisdictional disputes.", "صياغة بنود تعاقدية واضحة ومحددة يمنع النزاعات القانونية المستقبلية."), ("Diplomatic finesse turns volatile impasses into cooperative breakthroughs.", "الكياسة الدبلوماسية تحول المآزق المتفجرة إلى انفراجات تعاونية كبرى."), ("Sustainable agreements endure because every stakeholder feels respected and heard.", "الاتفاقيات المستدامة تدوم لأن كل طرف يشعر بأنه محترم ومسموع الصوت.")],
            {"title": "The Craft of Principled Consensus", "text": "True negotiation is neither a duel of attrition nor a surrender of core values. The Harvard negotiation methodology revolutionized international relations by distinguishing between rigid positions and underlying human interests. In high-stakes dialogues, seasoned diplomats invent creative options for mutual gain and apply objective criteria. By reframing adversaries as problem-solving partners, they forge durable accords that outlive transient political tempests.", "translation_ar": "التفاوض الحقيقي ليس معركة استنزاف ولا تنازلاً عن المبادئ الجوهرية. لقد أحدثت منهجية هارفارد للتفاوض ثورة في العلاقات الدولية بالتمييز بين المواقف المتصلبة والمصالح الإنسانية العميقة. وفي الحوارات المصيرية، يبتكر الدبلوماسيون المحنكون خيارات إبداعية للمكسب المشترك ويطبقون معايير موضوعية. ومن خلال إعادة تصنيف الخصوم كشركاء في حل المشكلة، يصيغون اتفاقات متينة تعيش أطول من العواصف السياسية العابرة."},
            "اكتب سيناريو تفاوض بين شركتين عالميتين للوصول لحل وسط يرضي الطرفين في كراستك."
        ),
        (
            46, "Philosophical Epistemology & the Nature of Truth", "نظرية المعرفة الفلسفية وطبيعة الحقيقة",
            "مناقشة النصوص الفلسفية العليا (كيف نعرف ما نعرفه؟)، العقلانية مقابل التجريبية.",
            [("Epistemic", "E-P-I-S-T-E-M-I-C", "معرفي"), ("Philosophy", "P-H-I-L-O-S-O-P-H-Y", "فلسفة"), ("Rationalism", "R-A-T-I-O-N-A-L-I-S-M", "عقلانية"), ("Empiricism", "E-M-P-I-R-I-C-I-S-M", "تجريبية"), ("Certainty", "C-E-R-T-AI-N-T-Y", "يقين"), ("Skepticism", "S-K-E-P-T-I-C-I-S-M", "شك منهجي")],
            [("Epistemology investigates the boundaries dividing justified true belief from mere conjecture.", "تبحث نظرية المعرفة في الحدود الفاصلة بين الإيمان المبرر والظنون العابرة."), ("Rationalism posits that fundamental knowledge originates in reason rather than sensory data.", "ترى العقلانية أن المعرفة الجوهرية تنبع من العقل لا من معطيات الحواس وحدها."), ("Empiricism rigorously requires experiential observation before validating any theory.", "تشترط التجريبية فحص الملاحظة الواقعية بصرامة قبل إقرار أي نظرية."), ("Methodological skepticism refines truth by subjecting every premise to intense scrutiny.", "الشك المنهجي يصفي الحقيقة بإخضاع كل مقدمة لتمحيص فكري شديد."), ("To know that you know what you know, and know that you do not know what you do not know, is true wisdom.", "أن تعرف ما تعرفه، وتدرك ما تجهله، هو جوهر الحكمة الإنسانية الأصيلة.")],
            {"title": "The Quest for Epistemic Grounding", "text": "From Socrates wandering the bustling agora of Athens to contemporary cognitive scientists mapping neural synapses, the quest to comprehend the architecture of knowledge has defined humanity. Are our perceptions faithful representations of external reality, or merely evolutionary illusions engineered for survival? Grappling with these profound inquiries strips away dogmatic arrogance, instilling intellectual humility and a profound reverence for the mysteries of consciousness.", "translation_ar": "من سقراط متجولاً في ساحات أثينا إلى علماء الأعصاب المعاصرين وهم يرسمون خرائط التشابكات العصبية، ظل السعي لفهم بنية المعرفة هو ما يميز الإنسانية. هل إدراكنا الحسي تمثيل أمين للواقع الخارجي، أم مجرد وهم تطوري صُمم للبقاء؟ إن مصارعة هذه التساؤلات العميقة تنزع عنا الغرور وتغرس تواضعاً فكرياً وتقديراً لأسرار الوعي البشري."},
            "اكتب مقالاً فلسفياً من 10 أسطر يناقش كيف نصل لليقين في عصر الذكاء الاصطناعي والمعلومات المزيفة."
        ),
        (
            47, "Geopolitics, Global Economics & Macro Systems", "الجيوسياسة، الاقتصاد الكلي والنظم العالمية",
            "تحليل التوازنات الجيوسياسية، سلاسل الإمداد العالمية، وأسواق المال الدولية.",
            [("Geopolitics", "G-E-O-P-O-L-I-T-I-C-S", "جيوسياسة"), ("Economy", "E-C-O-N-O-M-Y", "اقتصاد"), ("Inflation", "I-N-F-L-A-T-I-ON", "تضخم مالي"), ("Supply-chain", "S-U-PP-L-Y-CH-AI-N", "سلسلة إمداد"), ("Monetary", "M-O-N-E-T-A-R-Y", "نقدي/مالي"), ("Sovereignty", "S-O-V-E-R-EI-G-N-T-Y", "سيادة وطنية")],
            [("Macroeconomic stability requires balancing monetary policy with fiscal discipline.", "يتطلب الاستقرار الاقتصادي الكلي موازنة السياسة النقدية بالانضباط المالي."), ("Globalized supply chains optimize production costs but introduce systemic vulnerabilities.", "سلاسل الإمداد المعولمة تحسن تكاليف الإنتاج لكنها تخلق هشاشة في الأزمات."), ("Geopolitical realignments are redrawing international trade corridors across Eurasia.", "إعادة التموضع الجيوسياسي تعيد رسم ممرات التجارة الدولية عبر أوراسيا."), ("Central banks navigate delicate tightropes between combating inflation and stifling growth.", "تسير البنوك المركزية على حبال دقيقة للموازنة بين كبح التضخم ودعم النمو."), ("Economic resilience demands domestic industrial capability combined with open commerce.", "المرونة الاقتصادية تقتضي قدرة تصنيع محلية قوية مقترنة بتجارة دولية منفتحة.")],
            {"title": "The Interconnected Web of Global Trade", "text": "In our intricately woven global economy, an earthquake in the Pacific or a canal blockade instantly reverberates across supermarkets and stock exchanges thousands of miles away. Modern nations are bound in a mutual dance of trade, where raw materials, microprocessors, and financial liquidity flow continuously. Understanding these macro currents enables leaders to anticipate geopolitical friction and construct resilient systems for the common good.", "translation_ar": "في اقتصادنا العالمي المنسوج بدقة، فإن زلزالاً في المحيط أو انسداداً في قناة مائية يتردد صداه فوراً في متاجر وأسواق مال تبعد آلاف الأميال. ترتبط الأمم الحديثة في رقصة تجارية متبادلة تتدفق فيها المواد الخام والرقائق والسيولة. إن فهم هذه التيارات الكلية يمكن القادة من استشراف التوترات وبناء نظم صلبة تخدم الصالح العام."},
            "اكتب مقالاً بالإنجليزية من 10 أسطر يحلل أهمية الاستثمار في التصنيع المحلي لمواجهة أزمات سلاسل الإمداد."
        ),
        (
            48, "Existential Ethics, Morality & Human Destiny", "الأخلاق الوجودية، الضمير الإنساني والمسؤولية الأخلاقية",
            "مناقشة المعضلات الأخلاقية الكبرى في الطب والحروب والجينات والمستقبل الحضاري.",
            [("Ethics", "E-TH-I-C-S", "أخلاقيات"), ("Conscience", "C-O-N-S-C-I-E-N-C-E", "ضمير"), ("Moral", "M-O-R-A-L", "أخلاقي"), ("Dilemma", "D-I-L-E-MM-A", "معضلة أخلاقية"), ("Obligation", "O-B-L-I-G-A-T-I-ON", "واجب/التزام"), ("Humanity", "H-U-M-A-N-I-T-Y", "إنسانية")],
            [("Technological prowess devoid of ethical conscience becomes an instrument of catastrophe.", "إن البراعة التكنولوجية المجردة من الضمير الأخلاقي تتحول إلى أداة كارثة."), ("Moral obligations transcend legal boundaries and bind universal human conscience.", "الالتزامات الأخلاقية تتجاوز الحدود القانونية وتلزم الضمير الإنساني العالمي."), ("In navigating profound ethical dilemmas, human dignity must remain inviolable.", "عند مواجهة المعضلات الأخلاقية العميقة، يجب أن تظل الكرامة الإنسانية مصونة لا تمس."), ("Every generation stands accountable for the world it bequeaths to its successors.", "كل جيل يقف مسؤولاً وخاضعاً للحساب عن شكل العالم الذي يتركه لخلفائه."), ("The ultimate measure of a human being is their conduct toward the vulnerable.", "المقياس النهائي للإنسان الحقيقي هو سلوكه وتعامله مع الضعفاء في المجتمع.")],
            {"title": "The Moral Compass of Progress", "text": "As science unlocks the keys to genetic editing, quantum computing, and artificial sentience, the ancient question of Socrates returns with terrifying urgency: 'How ought we to live?' The acquisition of power must never outpace the cultivation of moral character. Progress is not counted in megatons or gigahertz; it is measured by our capacity to alleviate suffering, uphold justice, and cherish the sacred gift of life.", "translation_ar": "مع قيام العلم بفك شفرات التعديل الجيني، والحوسبة الكمية، والذكاء الاصطناعي، يعود سؤال سقراط الخالد بإلحاح مهيب: 'كيف ينبغي لنا أن نحيا؟'. إن اكتساب القوة يجب ألا يسبق بناء الشخصية الأخلاقية. فالتقدم لا يقاس بالجيغاهرتز أو أرقام الإنتاج؛ بل بقدرتنا على تخفيف المعاناة، وإعلاء العدالة، وصون قدسية الحياة."},
            "اكتب مقالاً في كراستك من صفحة يناقش المعايير الأخلاقية التي يجب فرضها على أبحاث الذكاء الاصطناعي."
        ),
        (
            49, "Spontaneous High-Level Debate & Unscripted Dialogue", "المناظرات الارتجالية والحديث التلقائي الفوري",
            "التحدث بالإنجليزية دون تحضير مسبق، التفكير بالإنجليزية فورياً، والرد على الأسئلة الصعبة في المؤتمرات الدولية.",
            [("Spontaneous", "S-P-O-N-T-A-N-E-OU-S", "تلقائي/ارتجالي"), ("Unscripted", "U-N-S-C-R-I-P-T-ED", "عفوي غير معد"), ("Articulate", "AR-T-I-C-U-L-A-T-E", "يعبر بفصاحة"), ("Presence", "P-R-E-S-E-N-C-E", "سرعة بديهة"), ("Fluency", "F-L-U-E-N-C-Y", "طلاقة متدفقة"), ("Intuitive", "I-N-T-U-I-T-I-V-E", "بديهي/تلقائي")],
            [("Spontaneous mastery means expressing complex arguments without translating internally.", "الطلاقة الارتجالية تعني صياغة حجج معقدة دون الحاجة للترجمة الذهنية المسبقة."), ("He handled the aggressive press conference with calm poise and razor-sharp intellect.", "تعامل مع المؤتمر الصحفي الهجومي بهدوء متزن وذكاء حاد كالشفرة."), ("Your ideas flow effortlessly when vocabulary becomes second nature to your thoughts.", "تتدفق أفكارك بسلاسة تامة عندما تصبح المفردات جزءاً من طبيعة تفكيرك التلقائي."), ("Unscripted authenticity resonates far more powerfully than sterile memorized notes.", "الأصالة العفوية غير المكتوبة تلامس القلوب بقوة تفوق المذكرات المحفوظة."), ("True bilingualism means living, dreaming, and creating fluently across two languages.", "ثنائية اللغة الحقيقية تعني أن تعيش وتحلم وتبدع بطلاقة بين لغتين.")],
            {"title": "Thinking Without Borders", "text": "There arrives a golden milestone in language acquisition where the invisible wall between mind and tongue evaporates completely. You no longer translate; you simply conceive the idea and it manifests instantaneously in expressive English. You debate spontaneously, crack spontaneous humor, grasp literary undertones, and navigate unexpected intellectual storms with effortless composure. You have crossed the threshold of native intuition.", "translation_ar": "تأتي لحظة فارقة ذهبية في تعلم اللغة يتبخر فيها الجدار غير المرئي بين العقل واللسان تماماً. لم تعد تترجم؛ بل تفكر في الفكرة فتخرج فوراً بإنجليزية فصيحة ومعبرة. تناظر بارتجال، تمزح بعفوية، تدرك التلميحات الأدبية، وتواجه العواصف الفكرية غير المتوقعة بثبات وسلاسة. لقد عبرت أخيراً عتبة الحدس اللغوي الأصيل."},
            "اكتب مقالاً ارتجالياً من صفحة كاملة تسجل فيه حواراً حراً يدور في عقلك الآن بالإنجليزية التامة."
        ),
        (
            50, "Bilingual Native Mastery & The Ultimate Graduation", "الطلاقة التامة والتحدث كمتحدث أصلي (Native Mastery)",
            "قمة الهرم اللغوي: إتقان اللغة الإنجليزية كلغة أم ثانية، الحصول على الشهادة النهائية وتتويج الرحلة.",
            [("Mastery", "M-A-S-T-ER-Y", "إتقان تام"), ("Native", "N-A-T-I-V-E", "أصلي"), ("Bilingual", "B-I-L-I-N-G-U-A-L", "ثنائي اللغة"), ("Eloquent", "E-L-O-QU-E-N-T", "بليغ"), ("Triumph", "T-R-I-U-M-P-H", "انتصار/تتويج"), ("Legacy", "L-E-G-A-C-Y", "إرث حضاري")],
            [("Language is no longer a subject of study; it is an inseparable extension of my being.", "لم تعد اللغة مجرد مادة دراسية؛ بل أصبحت امتداداً لا يتجزأ من كياني وروحي."), ("I converse with native speakers around the globe as a cultural equal and ambassador.", "أتحدث مع المتحدثين الأصليين في العالم كسفير ثقافي ونظير كامل الأهلية."), ("From tracing the letter 'S' to debating global philosophy, this has been a heroic journey.", "من رسم حرف S إلى مناظرة الفلسفة العالمية، كانت هذه رحلة بطولية بحق."), ("True fluency unlocks the doors of global libraries, scientific laboratories, and human empathy.", "الطلاقة الحقيقية تفتح أبواب المكتبات العالمية، والمعامل العلمية، والتضامن الإنساني."), ("Congratulations, graduate! You now speak the global language with authentic native mastery.", "مبارك لك يا خريج! أنت الآن تتحدث لغة العالم بطلاقة أهلها الأصليين وبلاغتهم.")],
            {"title": "The Odyssey of Fluency: From Phonics to the Stars", "text": "Fifty levels ago, you embarked on this pilgrimage with simple phonetic sounds: /s/, /a/, /t/. Day after day, you practiced faithfully, repeating words, memorizing patterns, handwriting pages, recording voice notes, and daring to speak without fear. Look back at the mountain you have scaled. Today, you read complex essays, articulate profound philosophies, and converse naturally as an empowered global citizen. You do not just speak English; you command it. Congratulations on achieving Native Bilingual Mastery on the ABC Platform!", "translation_ar": "منذ خمسين مستوى، بدأت هذه الرحلة بأصوات صوتية بسيطة: /s/ و /a/ و /t/. ويوماً بعد يوم، تدربت بإخلاص، مكرراً الكلمات، حافظاً الأنماط، كاتباً في الكراسة، مسجلاً بصوتك، وجريئاً على التحدث دون خوف. انظر خلفك إلى الجبل الشاهق الذي تسلقته. اليوم، تقرأ مقالات معقدة، تعبر عن فلسفات عميقة، وتتحدث بعفوية كمواطن عالمي حر. أنت لا تتحدث الإنجليزية فحسب؛ بل تتقنها وتتحكم فيها ببراعة. مبارك لك تحقيق الطلاقة المزدوجة التامة على منصة ABC!"},
            "اكتب خطاب التخرج النهائي الكامل لرحلتك التعليمية في كراسة الخط بالإنجليزية (صفحة كاملة)، والتقط صورة لدفترك للتتويج والحصول على الشهادة المعتمدة النهائية 🎓🌟."
        )
    ]

    for num, title, subtitle, desc, words_raw, sents_raw, passage, hw in stage5:
        levels.append({
            "level_number": num,
            "stage": 5,
            "stage_name": "المرحلة 5: التحدث بالإنجليزية كلغة أم (Bilingual Native Mastery)",
            "level_type": "advanced_articles_and_debates",
            "title": f"Level {num} – {title}",
            "subtitle": subtitle,
            "description": desc,
            "icon": "trophy",
            "letters": [{"symbol": w[0][:3].upper(), "sound": f"/{w[0][:3].lower()}/", "name": w[0], "sound_name": w[0], "arabic_desc": w[2]} for w in words_raw[:4]],
            "words": [{"word": w[0], "phonemes": w[1], "translation_ar": w[2], "image": f"/images/words/{w[0].lower()}.svg"} for w in words_raw],
            "sentences": [{"text": s[0], "translation_ar": s[1]} for s in sents_raw],
            "passage": passage,
            "homework_prompt": hw,
            "repetition_count": 3,
            "intro_ar": f"أهلاً بك في قمة المستويات (المستوى {num})! هدفك هو الطلاقة المطلقة وبلاغة المتحدث الأصلي حول {subtitle}."
        })

    return levels

def generate_50_levels():
    return get_50_levels_data()

CURRICULUM_50 = generate_50_levels()
