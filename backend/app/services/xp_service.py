# XP Progression and Level Thresholds Service
# Formula:
# Level 1: 0 XP
# Level 2: 50 XP
# Level 3: 200 XP (+150)
# Level 4: 450 XP (+250)
# Level 5: 800 XP (+350)
# ...
# Level 15: 11,250 XP (Conversational Fluency)
# Level 50: 125,000 XP (Native Bilingual Mastery)

def get_xp_required_for_level(level: int) -> int:
    """Calculate cumulative XP required to reach a specific level (1 to 50)."""
    if level <= 1:
        return 0
    # Base 50 for L2, then incrementing delta: 150, 250, 350, 450...
    # Delta for step (k -> k+1) is 50 + 100*(k-1)
    # Sum of deltas from 1 to level-1:
    # sum_{k=1}^{level-1} [50 + 100*(k-1)] = 50*(level-1) + 100 * (level-2)*(level-1)/2
    # = 50*(level-1) + 50*(level-2)*(level-1) = 50*(level-1)^2
    return 50 * ((level - 1) ** 2)

def get_level_stage_info(level: int) -> dict:
    """Return stage category and title for a given level (1 to 50)."""
    if level <= 10:
        return {
            "stage_id": 1,
            "stage_name": "التأسيس وأصوات الحروف (Phonics & Foundations)",
            "badge": "🔤 خبير الأصوات",
            "fluency_target": "قراءة ودمج الكلمات والحروف بدقة"
        }
    elif level <= 20:
        return {
            "stage_id": 2,
            "stage_name": "المحادثة والتواصل الاجتماعي (Everyday Conversations)",
            "badge": "🗣️ متحدث اجتماعي",
            "fluency_target": "التحدث مع الناس والتعامل في المطاعم والمتاجر والمواقف اليومية بثقة (مستوى 15 يتيح المحادثة التامة مع أشخاص)"
        }
    elif level <= 35:
        return {
            "stage_id": 3,
            "stage_name": "الطلاقة المتوسطة والتعبير الحر (Expressive Fluency)",
            "badge": "🌟 طلاقة تعبيرية",
            "fluency_target": "سرد القصص والتعبير عن المشاعر والتفاوض وإبداء الآراء بطلاقة"
        }
    elif level <= 45:
        return {
            "stage_id": 4,
            "stage_name": "الاحتراف المتقدم والمصطلحات الدارجة (Advanced Professional)",
            "badge": "💼 لغة احترافية",
            "fluency_target": "المقابلات الرسمية والتعبيرات الاصطلاحية ومتابعة اللهجات السريعة"
        }
    else:
        return {
            "stage_id": 5,
            "stage_name": "إتقان اللغة كلغة أم (Native Bilingual Mastery)",
            "badge": "👑 متحدث أصلي (Native)",
            "fluency_target": "التحدث باللغة الإنجليزية بعفوية وتلقائية تامة تضاهي اللغة الأم"
        }

def get_next_level_requirements(current_level: int, current_xp: int) -> dict:
    next_level = min(50, current_level + 1)
    xp_needed_total = get_xp_required_for_level(next_level)
    xp_remaining = max(0, xp_needed_total - current_xp)
    current_level_base = get_xp_required_for_level(current_level)
    
    range_for_this_level = max(1, xp_needed_total - current_level_base)
    progress_in_level = max(0, current_xp - current_level_base)
    percentage = min(100, int((progress_in_level / range_for_this_level) * 100))

    return {
        "current_level": current_level,
        "next_level": next_level,
        "current_xp": current_xp,
        "xp_required_for_next": xp_needed_total,
        "xp_remaining": xp_remaining,
        "percentage": percentage,
        "can_level_up": current_xp >= xp_needed_total,
        "stage": get_level_stage_info(current_level)
    }
