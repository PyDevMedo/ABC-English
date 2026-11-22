import React, { useEffect, useState } from 'react';
import { 
  Award, Volume2, CheckCircle2, XCircle, ArrowLeft, 
  Sparkles, RotateCcw, Trophy, Star, ShieldCheck, Flame 
} from 'lucide-react';
import { api, playAudio } from '../services/api';
import { useAuth } from '../context/AuthContext';
import confetti from 'canvas-confetti';

export const QuizzesPage: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [levelQuiz, setLevelQuiz] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [submitting, setSubmitting] = useState(false);

  const currentLevelId = user?.current_level_id || 1;

  const loadQuiz = () => {
    setLoading(true);
    setResult(null);
    setAnswers({});
    api.getLevelQuiz(currentLevelId)
      .then(setLevelQuiz)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadQuiz();
  }, [currentLevelId]);

  const selectAnswer = (questionId: number, option: string) => {
    setAnswers(prev => ({
      ...prev,
      [questionId.toString()]: option
    }));
  };

  const handleSubmitQuiz = async () => {
    if (!levelQuiz) return;
    setSubmitting(true);
    try {
      const res = await api.submitQuiz(levelQuiz.id, answers);
      setResult(res);
      if (res.passed) {
        confetti({ particleCount: 120, spread: 80, origin: { y: 0.5 } });
        refreshUser();
      }
    } catch (err: any) {
      alert(err.message || 'فشل إرسال الإجابات');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="text-center py-16 font-bold text-slate-400">جاري تحميل اختبار المستوى...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-8">
      {/* Quiz Header */}
      <div className="bg-gradient-to-r from-rose-500 via-pink-500 to-amber-500 rounded-3xl p-6 text-white shadow-xl text-center relative overflow-hidden">
        <span className="text-xs font-black bg-white/20 px-3.5 py-1 rounded-full mb-2 inline-block">
          Level {currentLevelId}/50 Mastery Assessment
        </span>
        <h2 className="text-2xl md:text-3xl font-black font-fredoka">
          {levelQuiz?.title || 'اختبار إتقان المستوى'}
        </h2>
        <p className="text-xs font-bold text-rose-100 mt-1">
          نسبة النجاح لاجتياز الاختبار: {levelQuiz?.passing_score || 80}% • صعوبة تصاعدية مع كل مستوى
        </p>
      </div>

      {result ? (
        /* Quiz Result Card */
        <div className="bg-white rounded-3xl p-8 border-4 border-amber-300 shadow-xl text-center space-y-6">
          <div className="w-24 h-24 rounded-3xl mx-auto flex items-center justify-center text-5xl shadow-inner border-2 border-amber-200">
            {result.passed ? '🏆' : '💪'}
          </div>

          <div>
            <h3 className="text-3xl font-black text-slate-800">
              {result.passed ? 'مبارك! إنجاز واجتياز رائع 🌟' : 'محاولة جيدة، راجع وحاول مرة أخرى!'}
            </h3>
            <div className="text-4xl font-black text-amber-500 my-2 font-fredoka">
              {result.score}%
            </div>
            <p className="text-sm font-bold text-slate-600">
              أجبت إجابة صحيحة على {result.correct_count} من أصل {result.total_count} أسئلة.
            </p>
          </div>

          {result.level_unlocked ? (
            <div className="p-4 bg-emerald-50 rounded-2xl border-2 border-emerald-300 text-emerald-900 font-bold text-sm">
              🎉 <b>تهانينا!</b> لقد حققت شروط الإتقان ومعدل الـ XP المطلوب وتم فتح <b>Level {currentLevelId + 1}</b> لك رسمياً!
            </div>
          ) : result.passed ? (
            <div className="p-4 bg-purple-50 rounded-2xl border-2 border-purple-300 text-purple-900 font-bold text-sm">
              ⭐ <b>أحسنت!</b> لقد اجتزت الاختبار بنجاح، وتحتاج إلى نقاط خبرة (XP) إضافية للارتقاء للمستوى التالي. واصل التدرب في مختبر النطق وأكمل واجبات الدفتر!
            </div>
          ) : (
            <div className="p-4 bg-amber-50 rounded-2xl border-2 border-amber-300 text-amber-900 font-bold text-sm">
              تحتاج إلى 80% لاجتياز الاختبار، استمع للكلمات جيداً وحاول مرة أخرى بكل ثقة!
            </div>
          )}

          {/* Details breakdown */}
          <div className="space-y-3 text-right">
            <h4 className="text-sm font-black text-slate-800">مراجعة الإجابات:</h4>
            {Object.keys(result.details || {}).map((k) => {
              const item = result.details[k];
              return (
                <div
                  key={k}
                  className={`p-3 rounded-2xl border-2 text-xs font-bold flex items-center justify-between ${
                    item.is_correct ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-rose-50 border-rose-200 text-rose-900'
                  }`}
                >
                  <div>
                    <span className="block font-black mb-0.5">{item.question}</span>
                    <span className="text-[11px] opacity-80">إجابتك: {item.student_answer || item.child_answer || 'لم تجب'}</span>
                  </div>
                  <span className="shrink-0 text-base">{item.is_correct ? '✓' : '✗'}</span>
                </div>
              );
            })}
          </div>

          <button
            type="button"
            onClick={loadQuiz}
            className="kid-button-primary px-8 py-3 mx-auto text-sm"
          >
            <RotateCcw className="w-4 h-4" />
            <span>إعادة الاختبار</span>
          </button>
        </div>
      ) : (
        /* Questions List */
        <div className="space-y-6">
          {levelQuiz?.questions?.map((q: any, idx: number) => {
            const selectedOpt = answers[q.id.toString()];
            return (
              <div key={q.id} className="kid-card p-6 border-slate-200">
                <div className="flex items-center justify-between gap-4 mb-4">
                  <span className="w-8 h-8 rounded-xl bg-amber-400 text-amber-950 font-black text-sm flex items-center justify-center">
                    {idx + 1}
                  </span>
                  {q.audio_url && (
                    <button
                      type="button"
                      onClick={() => playAudio(q.audio_url, q.correct_answer)}
                      className="px-3.5 py-1.5 bg-amber-100 hover:bg-amber-200 text-amber-900 rounded-xl text-xs font-black flex items-center gap-1.5 shadow-sm active:scale-95 transition-all"
                    >
                      <Volume2 className="w-4 h-4 text-amber-700" />
                      <span>استمع للمقطع الصوتي 🔊</span>
                    </button>
                  )}
                </div>

                <h4 className="text-base font-black text-slate-900 mb-4 whitespace-pre-line">{q.question_text}</h4>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {q.options?.map((opt: string, optIdx: number) => {
                    const isSelected = selectedOpt === opt;
                    return (
                      <button
                        key={optIdx}
                        type="button"
                        onClick={() => selectAnswer(q.id, opt)}
                        className={`p-3.5 rounded-2xl border-2 text-sm font-black font-fredoka transition-all text-center ${
                          isSelected
                            ? 'bg-amber-400 text-amber-950 border-amber-500 shadow-md scale-102'
                            : 'bg-slate-50 text-slate-800 border-slate-200 hover:bg-white hover:border-slate-300'
                        }`}
                      >
                        {opt}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}

          <div className="text-center pt-4">
            <button
              type="button"
              onClick={handleSubmitQuiz}
              disabled={submitting || Object.keys(answers).length === 0}
              className="kid-button-primary px-10 py-4 text-base font-black mx-auto shadow-xl"
            >
              <Award className="w-6 h-6" />
              <span>{submitting ? 'جاري الرصد...' : 'تسليم الاختبار ورصد النتيجة ⭐'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
