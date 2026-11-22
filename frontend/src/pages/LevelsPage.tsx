import React, { useEffect, useState } from 'react';
import { 
  Layers, Lock, Play, Star, CheckCircle, Sparkles, BookOpen, 
  Award, ArrowLeft, CheckCircle2, ShieldCheck, PenTool, Mic
} from 'lucide-react';
import { api } from '../services/api';
import { LessonViewModal } from './LessonViewModal';
import { useAuth } from '../context/AuthContext';

export const LevelsPage: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [levels, setLevels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLevelId, setSelectedLevelId] = useState<number | null>(null);

  const loadLevels = () => {
    setLoading(true);
    api.getLevels()
      .then(setLevels)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadLevels();
  }, []);

  const currentLevelNum = user?.current_level_id || 1;
  const currentLevel = levels.find((l) => l.level_number === currentLevelNum) || levels[0];

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto">
        <span className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-black mb-3 border border-amber-300">
          <Sparkles className="w-4 h-4 text-amber-600" />
          منهج Phonics المتدرج للطلاب
        </span>
        <h2 className="text-3xl md:text-4xl font-black text-slate-800 font-fredoka">
          المستوى التعليمي الحالي
        </h2>
        <p className="text-sm font-bold text-slate-600 mt-2">
          يتم التركيز على مستواك الحالي خطوة بخطوة حتى تتقن أصوات الحروف والقراءة والكتابة بالكامل.
        </p>
      </div>

      {loading || !currentLevel ? (
        <div className="text-center py-16 font-bold text-slate-400">
          جاري تجهيز بيانات مستواك الحالي... ⏳
        </div>
      ) : (
        <div className="space-y-6">
          {/* Main Professional Level Focus Card */}
          <div className="bg-gradient-to-br from-white to-amber-50/60 rounded-[2.5rem] p-6 sm:p-10 border-2 border-amber-300 shadow-xl shadow-amber-100/50 relative overflow-hidden">
            {/* Top Level Status Pill */}
            <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
              <div className="flex items-center gap-2">
                <span className="px-4 py-1.5 bg-gradient-to-r from-amber-400 to-rose-400 text-white text-xs font-black rounded-2xl shadow-sm">
                  المستوى الحالي: Level {currentLevel.level_number}
                </span>
                <span className="px-3 py-1 bg-emerald-100 text-emerald-800 text-xs font-black rounded-2xl flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  متاح ومفعل
                </span>
              </div>
              <span className="text-xs font-black text-slate-500">
                منهج ABC المعتمد للغة الإنجليزية
              </span>
            </div>

            {/* Level Title & Subtitle */}
            <div className="mb-8">
              <h3 className="text-2xl sm:text-4xl font-black text-slate-900 font-fredoka mb-2">
                {currentLevel.title}
              </h3>
              <p className="text-base font-bold text-amber-800 mb-3">
                {currentLevel.subtitle}
              </p>
              <p className="text-sm text-slate-600 font-bold leading-relaxed max-w-3xl">
                {currentLevel.description}
              </p>
            </div>

            {/* Modules / Journey Path inside Current Level */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                <div className="w-10 h-10 rounded-xl bg-sky-100 text-sky-600 flex items-center justify-center font-black text-lg mb-2">
                  🔤
                </div>
                <h4 className="text-sm font-black text-slate-800 mb-1">أصوات الحروف</h4>
                <p className="text-[11px] text-slate-500 font-bold">الاستماع لأصوات الحروف بلهجة أمريكية نقية</p>
              </div>

              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center font-black text-lg mb-2">
                  🧩
                </div>
                <h4 className="text-sm font-black text-slate-800 mb-1">دمج الكلمات</h4>
                <p className="text-[11px] text-slate-500 font-bold">تركيب الحروف لقراءة الكلمات والجمل بثقة</p>
              </div>

              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center font-black text-lg mb-2">
                  🎙️
                </div>
                <h4 className="text-sm font-black text-slate-800 mb-1">التقييم الصوتي الذكي</h4>
                <p className="text-[11px] text-slate-500 font-bold">تحليل دقيق لنطقك وتصحيح مخارج الحروف</p>
              </div>

              <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center font-black text-lg mb-2">
                  ✍️
                </div>
                <h4 className="text-sm font-black text-slate-800 mb-1">واجب الخط بالدفتر</h4>
                <p className="text-[11px] text-slate-500 font-bold">كتابة الكلمات على الأسطر الأربعة وتصويرها</p>
              </div>
            </div>

            {/* Action Button */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-amber-200/60">
              <div className="text-xs font-black text-slate-600">
                ⭐ يجب إتمام خطوات الدرس ورفع صورة كراسة الواجب للانتقال للمستوى التالي.
              </div>

              <button
                type="button"
                onClick={() => setSelectedLevelId(currentLevel.id)}
                className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-amber-400 via-orange-500 to-rose-500 hover:opacity-95 text-white font-black rounded-2xl text-sm flex items-center justify-center gap-2 shadow-lg shadow-orange-200 active:scale-95 transition-all"
              >
                <Play className="w-5 h-5 fill-white" />
                <span>دخول الدرس التفاعلي (Level {currentLevel.level_number})</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {selectedLevelId && (
        <LessonViewModal
          levelId={selectedLevelId}
          onClose={() => setSelectedLevelId(null)}
          onLessonCompleted={() => {
            refreshUser();
            loadLevels();
          }}
        />
      )}
    </div>
  );
};
