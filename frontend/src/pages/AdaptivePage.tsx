import React, { useEffect, useState } from 'react';
import { 
  Sparkles, CheckCircle2, Volume2, ArrowLeft, Star, 
  Trophy, ShieldAlert, Check, HelpCircle
} from 'lucide-react';
import { api, playAudio } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { AudioRecorder } from '../components/AudioRecorder';
import confetti from 'canvas-confetti';

export const AdaptivePage: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [planData, setPlanData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeStep, setActiveStep] = useState<number>(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());

  const loadPlan = () => {
    setLoading(true);
    api.getLearningPlan()
      .then(setPlanData)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadPlan();
  }, []);

  const handleStepComplete = async (exerciseId: number, index: number) => {
    try {
      await api.completeAdaptiveExercise(exerciseId, 100);
      confetti({ particleCount: 60, spread: 60, origin: { y: 0.7 } });
      setCompletedSteps(prev => new Set(prev).add(index));
      refreshUser();
      loadPlan();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <div className="text-center py-16 font-bold text-slate-400">جاري استعراض خطة المدرس الذكي...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-purple-500 via-indigo-500 to-sky-500 rounded-3xl p-6 md:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10">
          <div className="inline-flex items-center gap-1.5 bg-white/20 px-3 py-1 rounded-full text-xs font-bold mb-3">
            <Sparkles className="w-4 h-4 text-yellow-300" />
            نظام التعلم التكيفي المخصص
          </div>
          <h2 className="text-2xl md:text-3xl font-black font-fredoka">
            مدرسك الذكي: خطة التعلم الشخصية
          </h2>
          <p className="text-xs md:text-sm font-bold text-purple-100 mt-2 max-w-xl leading-relaxed">
            يقوم الذكاء الاصطناعي برصد الأصوات والحروف التي تحتاج لمزيد من الممارسة، ويصمم لك تدريبات سحرية ممتعة للتغلب عليها بسرعة.
          </p>
        </div>
      </div>

      {!planData?.has_plan ? (
        <div className="bg-white rounded-3xl p-8 md:p-12 text-center border-4 border-amber-200 shadow-md">
          <div className="w-24 h-24 bg-emerald-100 text-emerald-600 rounded-3xl mx-auto flex items-center justify-center text-4xl mb-4 shadow-inner">
            🌟
          </div>
          <h3 className="text-2xl font-black text-slate-800 mb-2">أنت عبقري يا بطل!</h3>
          <p className="text-slate-600 font-bold max-w-md mx-auto text-sm leading-relaxed mb-6">
            لا توجد نقاط ضعف أو أخطاء متكررة مسجلة في نطقك حالياً. جميع الأصوات اللغوية التي تدربت عليها ممتازة!
          </p>
          <div className="inline-flex items-center gap-2 bg-emerald-50 text-emerald-800 px-4 py-2 rounded-2xl font-bold text-xs border border-emerald-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>استمر في متابعة الدروس العادية وحصد النجوم!</span>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Active Plan Focus Card */}
          <div className="bg-white rounded-3xl p-6 border-4 border-purple-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <span className="text-xs font-black text-purple-600 bg-purple-50 px-3 py-1 rounded-full">
                الهدف الحالي:
              </span>
              <h3 className="text-xl font-black text-slate-900 mt-1 font-fredoka">
                {planData.current_focus}
              </h3>
              <p className="text-xs font-bold text-slate-500 mt-1">
                تم اكتشاف صعوبة في صوت {planData.weakness_summary?.skill}. صممنا لك {planData.exercises_count} تدريبات متدرجة.
              </p>
            </div>
            <div className="bg-purple-100 text-purple-900 px-4 py-2 rounded-2xl text-center shrink-0">
              <span className="text-2xl font-black block">{planData.exercises?.filter((e: any) => e.is_completed).length}/{planData.exercises_count}</span>
              <span className="text-[10px] font-bold">تم إنجازه</span>
            </div>
          </div>

          {/* Progressive Exercises List */}
          <div className="space-y-4">
            {planData.exercises?.map((ex: any, idx: number) => {
              const step = ex.data;
              const isDone = ex.is_completed || completedSteps.has(idx);

              return (
                <div
                  key={ex.id}
                  className={`kid-card p-6 border-2 transition-all ${
                    isDone
                      ? 'border-emerald-300 bg-emerald-50/40'
                      : 'border-purple-200 hover:border-purple-300'
                  }`}
                >
                  <div className="flex items-start justify-between gap-4 mb-4">
                    <div className="flex items-center gap-3">
                      <span className={`w-8 h-8 rounded-2xl flex items-center justify-center font-black text-sm shrink-0 ${
                        isDone ? 'bg-emerald-500 text-white' : 'bg-purple-500 text-white'
                      }`}>
                        {isDone ? '✓' : idx + 1}
                      </span>
                      <div>
                        <h4 className="text-base font-black text-slate-800">{step?.title_ar}</h4>
                        <span className="text-xs font-bold text-purple-700" dir="ltr">{step?.instruction_en}</span>
                      </div>
                    </div>

                    <span className="text-xs font-bold px-2.5 py-1 rounded-xl bg-purple-100 text-purple-800 shrink-0">
                      +{ex.difficulty === 'easy' ? '25' : '35'} XP
                    </span>
                  </div>

                  <p className="text-xs font-bold text-slate-600 bg-slate-50 p-3 rounded-2xl mb-4 border border-slate-200">
                    💡 {step?.instruction_ar}
                  </p>

                  {/* Target Words with Audio */}
                  {step?.target_words && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {step.target_words.map((w: string, wIdx: number) => (
                        <button
                          key={wIdx}
                          type="button"
                          onClick={() => playAudio(undefined, w)}
                          className="px-4 py-2 bg-white hover:bg-purple-50 text-purple-900 border-2 border-purple-200 rounded-2xl font-black font-fredoka text-sm flex items-center gap-2 shadow-sm transition-all"
                        >
                          <Volume2 className="w-4 h-4 text-purple-600" />
                          <span>{w}</span>
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Sample Sentence */}
                  {step?.sample_sentence && (
                    <div className="bg-purple-50/80 p-3 rounded-2xl mb-4 border border-purple-200 flex items-center justify-between">
                      <span className="font-black font-fredoka text-purple-950 text-sm" dir="ltr">
                        {step.sample_sentence}
                      </span>
                      <button
                        onClick={() => playAudio(undefined, step.sample_sentence)}
                        className="p-1.5 bg-white text-purple-700 rounded-xl shadow-sm"
                      >
                        <Volume2 className="w-4 h-4" />
                      </button>
                    </div>
                  )}

                  {/* Audio recorder if step has repeat/recording */}
                  {!isDone && (
                    <div className="flex justify-end mt-4">
                      <button
                        onClick={() => handleStepComplete(ex.id, idx)}
                        className="kid-button-green px-6 py-2.5 text-xs font-bold"
                      >
                        <Check className="w-4 h-4" />
                        <span>أتقنت هذا التدريب! (+25 XP)</span>
                      </button>
                    </div>
                  )}

                  {isDone && (
                    <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700 mt-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      <span>تم إتقان هذا التدريب بنجاح! 🌟</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
