import React, { useEffect, useState } from 'react';
import { Layers, Lock, Play, Star, CheckCircle, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { LessonViewModal } from './LessonViewModal';
import { useAuth } from '../context/AuthContext';

export const LevelsPage: React.FC = () => {
  const { refreshUser } = useAuth();
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

  const getLevelColor = (levelNum: number) => {
    switch (levelNum) {
      case 1: return { bg: 'from-amber-400 to-amber-500', border: 'border-amber-300', text: 'text-amber-600', pill: 'bg-amber-100 text-amber-900' };
      case 2: return { bg: 'from-sky-400 to-sky-500', border: 'border-sky-300', text: 'text-sky-600', pill: 'bg-sky-100 text-sky-900' };
      case 3: return { bg: 'from-emerald-400 to-emerald-500', border: 'border-emerald-300', text: 'text-emerald-600', pill: 'bg-emerald-100 text-emerald-900' };
      case 4: return { bg: 'from-purple-400 to-purple-500', border: 'border-purple-300', text: 'text-purple-600', pill: 'bg-purple-100 text-purple-900' };
      case 5: return { bg: 'from-rose-400 to-rose-500', border: 'border-rose-300', text: 'text-rose-600', pill: 'bg-rose-100 text-rose-900' };
      case 6: return { bg: 'from-indigo-400 to-indigo-500', border: 'border-indigo-300', text: 'text-indigo-600', pill: 'bg-indigo-100 text-indigo-900' };
      case 7: return { bg: 'from-teal-400 to-teal-500', border: 'border-teal-300', text: 'text-teal-600', pill: 'bg-teal-100 text-teal-900' };
      default: return { bg: 'from-yellow-400 to-amber-500', border: 'border-yellow-300', text: 'text-yellow-600', pill: 'bg-yellow-100 text-yellow-900' };
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      <div className="text-center max-w-2xl mx-auto">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-200 text-amber-900 text-xs font-black mb-2">
          <Sparkles className="w-4 h-4" />
          منهج Phonics المتدرج للأطفال
        </span>
        <h2 className="text-3xl md:text-4xl font-black text-slate-800 font-fredoka">
          المستويات التعليمية الثمانية
        </h2>
        <p className="text-sm font-bold text-slate-600 mt-2">
          انتقل خطوة بخطوة من أصوات الحروف الأولى وحتى القراءة والكتابة الشاملة بثقة وإتقان.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 font-bold text-slate-400">جاري تحميل خريطة المستويات...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {levels.map((lvl) => {
            const colors = getLevelColor(lvl.level_number);
            const isUnlocked = lvl.is_unlocked;

            return (
              <div
                key={lvl.id}
                className={`kid-card p-6 flex flex-col justify-between relative overflow-hidden transition-all ${
                  isUnlocked ? 'border-amber-300 hover:scale-[1.02]' : 'opacity-70 bg-slate-100 border-slate-300'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className={`text-xs font-black px-2.5 py-1 rounded-xl ${colors.pill}`}>
                      Level {lvl.level_number}
                    </span>
                    {!isUnlocked ? (
                      <span className="p-1.5 bg-slate-200 text-slate-500 rounded-xl" title="مقفول">
                        <Lock className="w-4 h-4" />
                      </span>
                    ) : (
                      <span className="p-1.5 bg-emerald-100 text-emerald-600 rounded-xl" title="متاح للدراسة">
                        <CheckCircle className="w-4 h-4" />
                      </span>
                    )}
                  </div>

                  <h3 className="text-lg font-black text-slate-900 font-fredoka mb-1">
                    {lvl.title}
                  </h3>
                  <h4 className="text-xs font-bold text-slate-600 mb-3">{lvl.subtitle}</h4>
                  <p className="text-xs text-slate-500 leading-relaxed font-bold line-clamp-3 mb-4">
                    {lvl.description}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-100">
                  {isUnlocked ? (
                    <button
                      type="button"
                      onClick={() => setSelectedLevelId(lvl.id)}
                      className="w-full py-2.5 bg-gradient-to-r from-amber-400 to-rose-400 hover:from-amber-500 hover:to-rose-500 text-white font-black rounded-xl text-xs flex items-center justify-center gap-1.5 shadow-md shadow-amber-200 active:scale-95 transition-all"
                    >
                      <Play className="w-4 h-4 fill-white" />
                      <span>فتح الدرس التفاعلي</span>
                    </button>
                  ) : (
                    <div className="text-center py-2 text-xs font-bold text-slate-400 bg-slate-200/50 rounded-xl">
                      🔒 أكمل المستوى السابق لفتحه
                    </div>
                  )}
                </div>
              </div>
            );
          })}
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
