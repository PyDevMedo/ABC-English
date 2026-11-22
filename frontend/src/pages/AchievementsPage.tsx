import React, { useEffect, useState } from 'react';
import { 
  Trophy, Star, Flame, Award, CheckCircle2, 
  Printer, Download, Sparkles 
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const AchievementsPage: React.FC = () => {
  const { user } = useAuth();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCert, setSelectedCert] = useState<any>(null);

  useEffect(() => {
    api.getGamificationDashboard()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const defaultBadges = [
    { key: 'first_sound', title: 'مستكشف أصوات الحروف الأولى', icon: '🌟', desc: 'أتقنت أصوات الحروف S, A, T, P, I, N' },
    { key: 'cvc_master', title: 'صانع الكلمات الثلاثية', icon: '🧩', desc: 'تكوين الكلمات السحرية من 3 أحرف' },
    { key: 'digraph_hero', title: 'بطل الأصوات المركبة SH و CH', icon: '🛡️', desc: 'إتقان نطق الأصوات المركبة بدون أخطاء' },
    { key: 'streak_3', title: 'بطل الاستمرارية 3 أيام', icon: '🔥', desc: 'التعلم لـ 3 أيام متتالية دون انقطاع' },
    { key: 'perfect_score', title: 'علامة كاملة 100/100', icon: '⭐', desc: 'تحقيق الدرجة الكاملة في النطق أو الاختبار' }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-400 via-yellow-400 to-rose-400 rounded-3xl p-6 md:p-8 text-amber-950 text-center shadow-xl relative overflow-hidden">
        <span className="text-xs font-black bg-white/70 px-3.5 py-1 rounded-full mb-2 inline-block">
          Gamification & Certificates
        </span>
        <h2 className="text-3xl md:text-4xl font-black font-fredoka">
          إنجازاتي وأوسمتي الذهبية
        </h2>
        <p className="text-xs md:text-sm font-bold text-amber-900 mt-2 max-w-lg mx-auto">
          كل خطوة تخطوها في القراءة والنطق تكافئك بكؤوس ونجوم وشهادات إتقان معتمدة 🏆
        </p>
      </div>

      {/* Stats Counter Bar */}
      <div className="grid grid-cols-3 gap-4">
        <div className="kid-card p-4 text-center border-amber-300">
          <Star className="w-8 h-8 text-amber-500 fill-amber-400 mx-auto mb-1 animate-bounce" />
          <div className="text-2xl md:text-3xl font-black text-amber-900 font-fredoka">{user?.stars || 0}</div>
          <span className="text-xs font-bold text-slate-500">النجوم الذهبية</span>
        </div>

        <div className="kid-card p-4 text-center border-purple-300">
          <Trophy className="w-8 h-8 text-purple-500 mx-auto mb-1" />
          <div className="text-2xl md:text-3xl font-black text-purple-900 font-fredoka">{user?.xp || 0}</div>
          <span className="text-xs font-bold text-slate-500">نقاط الخبرة XP</span>
        </div>

        <div className="kid-card p-4 text-center border-rose-300">
          <Flame className="w-8 h-8 text-rose-500 fill-rose-500 mx-auto mb-1" />
          <div className="text-2xl md:text-3xl font-black text-rose-900 font-fredoka">{user?.streak_days || 1}</div>
          <span className="text-xs font-bold text-slate-500">أيام الاستمرارية</span>
        </div>
      </div>

      {/* Badges Section */}
      <div className="bg-white rounded-3xl p-6 md:p-8 border-4 border-amber-200 shadow-md">
        <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
          <Award className="w-6 h-6 text-amber-500" />
          شارات وأوسمة الإنجاز
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {defaultBadges.map((b, i) => (
            <div
              key={i}
              className="p-4 rounded-2xl border-2 border-amber-100 bg-amber-50/50 flex items-start gap-3 shadow-sm hover:scale-102 transition-transform"
            >
              <div className="text-3xl shrink-0 p-2 bg-white rounded-2xl shadow-sm border border-amber-200">
                {b.icon}
              </div>
              <div>
                <h4 className="text-sm font-black text-slate-900">{b.title}</h4>
                <p className="text-[11px] text-slate-500 font-bold mt-0.5 leading-snug">{b.desc}</p>
                <span className="inline-flex items-center gap-1 text-[10px] font-black text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-md mt-2">
                  <CheckCircle2 className="w-3 h-3" /> تم الحصول عليها
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Certificates Section */}
      <div className="bg-white rounded-3xl p-6 md:p-8 border-4 border-amber-200 shadow-md">
        <h3 className="text-xl font-black text-slate-800 mb-4 flex items-center gap-2">
          <Trophy className="w-6 h-6 text-purple-500" />
          شهادات إتمام المستويات
        </h3>

        <div className="p-6 rounded-3xl border-4 border-amber-300 bg-gradient-to-br from-amber-50 via-yellow-50 to-white text-center space-y-4 max-w-lg mx-auto shadow-lg relative overflow-hidden">
          <div className="border-4 border-double border-amber-400 p-6 rounded-2xl">
            <span className="text-xs font-black tracking-widest text-amber-800 uppercase block mb-1">
              Certificate of Achievement
            </span>
            <h4 className="text-2xl font-black font-fredoka text-slate-900">
              شهادة تفوق وإتقان Phonics
            </h4>
            <p className="text-xs font-bold text-slate-500 my-2">تُمنح هذه الشهادة المعتمدة للطفل العبقري:</p>
            <div className="text-2xl font-black text-purple-900 border-b-2 border-purple-300 pb-2 max-w-xs mx-auto">
              {user?.full_name}
            </div>
            <p className="text-xs text-slate-600 font-bold mt-3 leading-relaxed">
              لاجتيازه مهارات منهج Phonics التأسيسي والقراءة الذكية بنجاح وتفوق باهر.
            </p>
            <div className="flex justify-between items-center text-[10px] text-slate-400 font-bold mt-6 pt-3 border-t border-amber-200">
              <span>المعرف: {user?.student_id}</span>
              <span>التاريخ: {new Date().toLocaleDateString('ar-EG')}</span>
            </div>
          </div>

          <button
            onClick={() => window.print()}
            className="kid-button-primary px-6 py-2.5 mx-auto text-xs"
          >
            <Printer className="w-4 h-4" />
            <span>طباعة الشهادة الآن 🖨️</span>
          </button>
        </div>
      </div>
    </div>
  );
};
