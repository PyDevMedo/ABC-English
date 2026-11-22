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
      <div className="bg-gradient-to-r from-amber-400 via-rose-400 to-indigo-600 rounded-[2.5rem] p-6 md:p-10 shadow-xl shadow-rose-100 text-white relative overflow-hidden">
        {/* Subtle decorative circles */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-black/10 rounded-full blur-2xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-5 text-center md:text-right">
            <div className="w-20 h-20 md:w-24 md:h-24 rounded-3xl bg-white/95 shadow-xl flex items-center justify-center text-4xl md:text-5xl border-4 border-white/60">
              {getAvatarEmoji(user.avatar)}
            </div>
            <div>
              <div className="inline-flex items-center gap-1.5 bg-white/20 backdrop-blur-md px-3.5 py-1 rounded-full text-xs font-black text-white mb-2">
                <Sparkles className="w-3.5 h-3.5 text-yellow-300" />
                المستوى الحالي: Level {user.current_level_id}
              </div>
              <h2 className="text-2xl md:text-4xl font-black font-fredoka tracking-tight text-white drop-shadow">
                Hello, {user.full_name}! 👋
              </h2>
              <p className="text-xs md:text-sm font-bold text-white/90 mt-1 max-w-lg">
                أهلاً بك في منصة <b>ABC</b> لتعليم الإنجليزية، هل أنت مستعد لدمج الأصوات وحصد النجوم اليوم؟ 🌟
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => onNavigate('levels')}
              className="px-6 py-3.5 bg-white hover:bg-slate-50 text-slate-900 font-black rounded-2xl shadow-lg transform active:scale-95 transition-all flex items-center gap-2 text-sm"
            >
              <PlayCircle className="w-5 h-5 text-rose-500 fill-rose-500" />
              <span>ابدأ درس اليوم</span>
            </button>
            <button
              onClick={() => onNavigate('pronunciation')}
              className="px-5 py-3.5 bg-white/20 hover:bg-white/30 backdrop-blur-md text-white font-black rounded-2xl border border-white/40 shadow-lg transform active:scale-95 transition-all flex items-center gap-2 text-sm"
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
        <div className="kid-card p-6">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-sky-50 text-sky-600 rounded-2xl border border-sky-100">
              <Layers className="w-6 h-6" />
            </span>
            <span className="text-[11px] font-black text-sky-600 bg-sky-50 px-3 py-1 rounded-full">الدرس التالي</span>
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-1">
            Level {user.current_level_id}: Letter Sounds
          </h3>
          <p className="text-xs text-slate-500 mb-4 font-bold">
            أصوات الحروف، دمج الكلمات، وقراءة الجمل القصيرة.
          </p>
          <button
            onClick={() => onNavigate('levels')}
            className="w-full py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-black rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all shadow-md shadow-sky-100"
          >
            <span>متابعة الدرس</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>

        {/* AI Learning Path Alert Card */}
        <div className="kid-card p-6">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-purple-50 text-purple-600 rounded-2xl border border-purple-100">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </span>
            <span className="text-[11px] font-black text-purple-600 bg-purple-50 px-3 py-1 rounded-full">المدرس الذكي AI</span>
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
            className="w-full py-2.5 bg-purple-500 hover:bg-purple-600 text-white font-black rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all shadow-md shadow-purple-100"
          >
            <span>{learningPlan?.has_plan ? 'حل تدريبات الذكاء الاصطناعي' : 'عرض مسار التعلم'}</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>

        {/* Homework & Exam Status Card */}
        <div className="kid-card p-6">
          <div className="flex items-center justify-between mb-4">
            <span className="p-3 bg-emerald-50 text-emerald-600 rounded-2xl border border-emerald-100">
              <Award className="w-6 h-6" />
            </span>
            <span className="text-[11px] font-black text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">الواجبات والاختبارات</span>
          </div>
          <h3 className="text-lg font-black text-slate-800 mb-1">
            اختبار المستوى {user.current_level_id}
          </h3>
          <p className="text-xs text-slate-500 mb-4 font-bold">
            اجتز الاختبار بنسبة 80% لفتح المستوى التالي والحصول على كؤوس XP!
          </p>
          <button
            onClick={() => onNavigate('quizzes')}
            className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white font-black rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all shadow-md shadow-emerald-100"
          >
            <span>خوض الاختبار الآن</span>
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Skills Showcase Section */}
      <div className="kid-card p-6 md:p-8">
        <h3 className="text-lg font-black text-slate-800 mb-4 flex items-center gap-2">
          <Trophy className="w-5 h-5 text-amber-500" />
          المهارات التي أتقنتها في منصة ABC
        </h3>
        <div className="flex flex-wrap gap-2.5">
          {dashboard?.mastered_skills?.map((skill: string, idx: number) => (
            <span
              key={idx}
              className="inline-flex items-center gap-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200 px-3.5 py-1.5 rounded-2xl text-xs md:text-sm font-bold"
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
