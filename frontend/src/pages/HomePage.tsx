import React, { useEffect, useState } from 'react';
import { 
  Sparkles, Star, Trophy, Flame, PlayCircle, CheckCircle, 
  ArrowLeft, ArrowRight, BookOpen, Layers, Award, Mic, Send
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api, playAudio } from '../services/api';

interface HomePageProps {
  onNavigate: (tab: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState<any>(null);
  const [learningPlan, setLearningPlan] = useState<any>(null);

  useEffect(() => {
    api.getGamificationDashboard().then(setDashboard).catch(console.error);
    api.getLearningPlan().then(setLearningPlan).catch(console.error);
  }, []);

  if (!user) return null;

  const getAvatarEmoji = (avatar: string) => {
    switch (avatar) {
      case 'panda': return '🐼';
      case 'bunny': return '🐰';
      case 'fox': return '🦊';
      case 'monkey': return '🐵';
      default: return '🦁';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Hero Welcome Banner */}
      <div className="bg-gradient-to-r from-amber-400 via-rose-300 to-purple-400 rounded-3xl p-6 md:p-8 shadow-xl text-amber-950 relative overflow-hidden border-4 border-white">
        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4 text-center md:text-right">
            <div className="w-20 h-20 md:w-24 md:h-24 rounded-3xl bg-white/90 shadow-lg flex items-center justify-center text-4xl md:text-5xl border-4 border-amber-200">
              {getAvatarEmoji(user.avatar)}
            </div>
            <div>
              <div className="inline-flex items-center gap-1.5 bg-white/70 px-3 py-1 rounded-full text-xs font-black text-purple-900 mb-2">
                <Sparkles className="w-3.5 h-3.5" />
                المستوى الحالي: Level {user.current_level_id}
              </div>
              <h2 className="text-2xl md:text-4xl font-black text-slate-900 font-fredoka">
                Hello, {user.full_name}! 👋
              </h2>
              <p className="text-sm md:text-base font-bold text-slate-800 mt-1">
                مدرسك الذكي فخور بنشاطك اليوم، هل أنت مستعد لمغامرة لغوية جديدة؟ 🌟
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => onNavigate('levels')}
              className="px-6 py-3.5 bg-white hover:bg-amber-50 text-amber-950 font-black rounded-2xl shadow-lg transform active:scale-95 transition-all flex items-center gap-2 text-sm md:text-base"
            >
              <PlayCircle className="w-5 h-5 text-rose-500 fill-rose-500" />
              <span>ابدأ درس اليوم</span>
            </button>
            <button
              onClick={() => onNavigate('pronunciation')}
              className="px-5 py-3.5 bg-purple-600 hover:bg-purple-700 text-white font-black rounded-2xl shadow-lg transform active:scale-95 transition-all flex items-center gap-2 text-sm md:text-base"
            >
              <Mic className="w-5 h-5" />
              <span>مختبر النطق</span>
            </button>
          </div>
        </div>
      </div>

      {/* Quick Status Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Next Lesson Card */}
        <div className="kid-card p-6 border-sky-200 shadow-sky-200">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-sky-100 text-sky-600 rounded-2xl">
              <Layers className="w-6 h-6" />
            </span>
            <span className="text-xs font-bold text-sky-600 bg-sky-50 px-3 py-1 rounded-full">الدرس التالي</span>
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-1">
            Level {user.current_level_id}: Letter Sounds
          </h3>
          <p className="text-xs text-slate-500 mb-4 font-bold">
            أصوات الحروف، دمج الكلمات، وقراءة الجمل القصيرة.
          </p>
          <button
            onClick={() => onNavigate('levels')}
            className="w-full py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all"
          >
            <span>متابعة الدرس</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>

        {/* AI Learning Path Alert Card */}
        <div className="kid-card p-6 border-purple-200 shadow-purple-200">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-purple-100 text-purple-600 rounded-2xl">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </span>
            <span className="text-xs font-bold text-purple-600 bg-purple-50 px-3 py-1 rounded-full">المدرس الذكي AI</span>
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-1">
            {learningPlan?.has_plan ? 'خطة تدريب شخصية نشطة' : 'أداؤك الصوتي ممتاز!'}
          </h3>
          <p className="text-xs text-slate-500 mb-4 font-bold">
            {learningPlan?.has_plan
              ? learningPlan.current_focus
              : 'الذكاء الاصطناعي يراقب نطقك لتوجيهك عند الحاجة.'}
          </p>
          <button
            onClick={() => onNavigate('adaptive')}
            className="w-full py-2.5 bg-purple-500 hover:bg-purple-600 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all"
          >
            <span>{learningPlan?.has_plan ? 'حل تدريبات الذكاء الاصطناعي' : 'عرض مسار التعلم'}</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>

        {/* Homework & Exam Status Card */}
        <div className="kid-card p-6 border-emerald-200 shadow-emerald-200">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-emerald-100 text-emerald-600 rounded-2xl">
              <Award className="w-6 h-6" />
            </span>
            <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">الواجبات والاختبارات</span>
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-1">
            اختبار المستوى {user.current_level_id}
          </h3>
          <p className="text-xs text-slate-500 mb-4 font-bold">
            اجتز الاختبار بنسبة 80% لفتح المستوى التالي والحصول على كؤوس XP!
          </p>
          <button
            onClick={() => onNavigate('quizzes')}
            className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all"
          >
            <span>خوض الاختبار الآن</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Skills Showcase Section */}
      <div className="bg-white rounded-3xl p-6 md:p-8 border-4 border-amber-200 shadow-md">
        <h3 className="text-xl font-black text-slate-800 mb-4 flex items-center gap-2">
          <Trophy className="w-6 h-6 text-amber-500" />
          المهارات التي أتقنتها في رحلتك
        </h3>
        <div className="flex flex-wrap gap-2.5">
          {dashboard?.mastered_skills?.map((skill: string, idx: number) => (
            <span
              key={idx}
              className="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-800 border-2 border-emerald-200 px-3.5 py-1.5 rounded-2xl text-xs md:text-sm font-bold"
            >
              <CheckCircle className="w-4 h-4 text-emerald-500" />
              {skill}
            </span>
          ))}
          {(!dashboard?.mastered_skills || dashboard.mastered_skills.length === 0) && (
            <span className="text-sm font-bold text-slate-400">ابدأ أول درس لجمع المهارات الذهبية!</span>
          )}
        </div>
      </div>
    </div>
  );
};
