import React, { useEffect, useState } from 'react';
import { 
  Award, Volume2, CheckCircle2, XCircle, ArrowLeft, ArrowRight,
  Sparkles, RotateCcw, Trophy, Star, ShieldCheck, Flame, ChevronRight, ChevronLeft
} from 'lucide-react';
import { api, playAudio, speakText } from '../services/api';
import { useAuth } from '../context/AuthContext';
import confetti from 'canvas-confetti';

export const QuizzesPage: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [levelQuiz, setLevelQuiz] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>(null);
  const [submitting, setSubmitting] = useState(false);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);

  const currentLevelId = user?.current_level_id || 1;

  const loadQuiz = () => {
    setLoading(true);
    setResult(null);
    setAnswers({});
    setCurrentIndex(0);
    api.getLevelQuiz(currentLevelId)
      .then(data => {
        setLevelQuiz(data);
        if (data?.questions?.[0]) {
          // Play audio for first question if applicable
          const q0 = data.questions[0];
          if (q0.audio_text || q0.question_type === 'listen_select') {
            setTimeout(() => {
              if (q0.audio_text) speakText(q0.audio_text);
            }, 600);
          }
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadQuiz();
  }, [currentLevelId]);

  const questions = levelQuiz?.questions || [];
  const totalQuestions = questions.length;
  const currentQ = questions[currentIndex];

  const handlePlayQuestionAudio = (q: any) => {
    if (!q) return;
    setIsAudioPlaying(true);
    const textToSpeak = q.audio_text || (q.question_type === 'listen_select' ? q.options?.[0] : null);
    if (textToSpeak) {
      speakText(textToSpeak);
    } else if (q.audio_url) {
      playAudio(q.audio_url, textToSpeak);
    }
    setTimeout(() => setIsAudioPlaying(false), 1200);
  };

  // Play audio when advancing to a new question if listening
  const handleGoToQuestion = (newIdx: number) => {
    if (newIdx < 0 || newIdx >= totalQuestions) return;
    setCurrentIndex(newIdx);
    const targetQ = questions[newIdx];
    if (targetQ && (targetQ.audio_text || targetQ.question_type === 'listen_select')) {
      setTimeout(() => handlePlayQuestionAudio(targetQ), 300);
    }
  };

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
    return <div className="text-center py-16 font-bold text-slate-400">جاري تحميل اختبار المستوى... 🎒</div>;
  }

  const answeredCount = Object.keys(answers).length;
  const progressPercent = totalQuestions > 0 ? Math.round(((currentIndex + 1) / totalQuestions) * 100) : 0;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      {/* Quiz Top Header */}
      <div className="bg-gradient-to-r from-rose-500 via-pink-500 to-amber-500 rounded-3xl p-6 text-white shadow-xl text-center relative overflow-hidden">
        <span className="text-xs font-black bg-white/20 px-3.5 py-1 rounded-full mb-2 inline-block">
          Level {currentLevelId}/50 Mastery Assessment
        </span>
        <h2 className="text-2xl md:text-3xl font-black font-fredoka">
          {levelQuiz?.title || 'اختبار إتقان المستوى'}
        </h2>
        <p className="text-xs font-bold text-rose-100 mt-1">
          نسبة النجاح لاجتياز الاختبار: {levelQuiz?.passing_score || 80}% • أسئلة متدرجة خطوة بخطوة
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
              ⭐ <b>أحسنت!</b> لقد اجتزت الاختبار بنجاح، وتحتاج إلى نقاط خبرة (XP) إضافية للارتقاء للمستوى التالي. واصل إكمال الواجبات والدروس!
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
                  className={`p-3.5 rounded-2xl border-2 text-xs font-bold flex items-center justify-between ${
                    item.is_correct ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-rose-50 border-rose-200 text-rose-900'
                  }`}
                >
                  <div>
                    <span className="block font-black mb-1">{item.question}</span>
                    <span className="text-[11px] opacity-80">إجابتك: {item.student_answer || item.child_answer || 'لم تجب'}</span>
                  </div>
                  <span className="shrink-0 text-lg font-black">{item.is_correct ? '✓' : '✗'}</span>
                </div>
              );
            })}
          </div>

          <button
            type="button"
            onClick={loadQuiz}
            className="kid-button-primary px-8 py-3.5 mx-auto text-sm"
          >
            <RotateCcw className="w-4 h-4" />
            <span>إعادة الاختبار</span>
          </button>
        </div>
      ) : (
        /* Step-by-Step Single Question Card */
        <div className="space-y-6">
          {/* Progress Indicator */}
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
            <div className="flex items-center justify-between text-xs font-black text-slate-700">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-ping"></span>
                السؤال {currentIndex + 1} من {totalQuestions}
              </span>
              <span className="text-amber-600">{progressPercent}% مكتمل</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden border border-slate-200">
              <div 
                className="bg-gradient-to-r from-amber-400 via-orange-500 to-rose-500 h-full rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              ></div>
            </div>

            {/* Step Dots */}
            <div className="flex items-center justify-center gap-2 pt-1">
              {questions.map((q: any, idx: number) => {
                const isAnswered = !!answers[q.id.toString()];
                const isCurrent = idx === currentIndex;
                return (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => handleGoToQuestion(idx)}
                    className={`w-7 h-7 rounded-full text-xs font-black transition-all flex items-center justify-center ${
                      isCurrent
                        ? 'bg-amber-500 text-white ring-4 ring-amber-200 scale-110'
                        : isAnswered
                        ? 'bg-emerald-500 text-white'
                        : 'bg-slate-200 text-slate-600 hover:bg-slate-300'
                    }`}
                  >
                    {idx + 1}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active Question Box */}
          {currentQ && (
            <div className="kid-card p-6 md:p-8 border-2 border-amber-200 shadow-xl bg-white space-y-6">
              {/* Question Header & Audio Button */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <span className="w-10 h-10 rounded-2xl bg-amber-400 text-amber-950 font-black text-base flex items-center justify-center shadow-md">
                    #{currentIndex + 1}
                  </span>
                  <span className="text-xs font-black text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
                    {currentQ.question_type === 'listen_select' ? '🎧 سؤال استماع وتمييز' : '✍️ سؤال فهم واختيار'}
                  </span>
                </div>

                {/* Crystal-Clear Audio Playback Button */}
                {(currentQ.audio_text || currentQ.audio_url || currentQ.question_type === 'listen_select') && (
                  <button
                    type="button"
                    onClick={() => handlePlayQuestionAudio(currentQ)}
                    className={`px-5 py-3 rounded-2xl font-black text-sm flex items-center justify-center gap-2 transition-all shadow-md active:scale-95 ${
                      isAudioPlaying
                        ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white animate-pulse shadow-emerald-200'
                        : 'bg-gradient-to-r from-amber-400 via-orange-400 to-amber-500 text-white hover:opacity-95 shadow-amber-200'
                    }`}
                  >
                    <Volume2 className={`w-5 h-5 ${isAudioPlaying ? 'animate-bounce' : ''}`} />
                    <span>{isAudioPlaying ? 'جاري التشغيل الآن...' : 'استمع للمقطع الصوتي 🔊'}</span>
                  </button>
                )}
              </div>

              {/* Question Text */}
              <h4 className="text-lg md:text-xl font-black text-slate-900 whitespace-pre-line leading-relaxed">
                {currentQ.question_text}
              </h4>

              {/* 4 Options Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                {currentQ.options?.map((opt: string, optIdx: number) => {
                  const isSelected = answers[currentQ.id.toString()] === opt;
                  return (
                    <button
                      key={optIdx}
                      type="button"
                      onClick={() => selectAnswer(currentQ.id, opt)}
                      className={`p-5 rounded-2xl border-2 text-base md:text-lg font-black font-fredoka transition-all text-center flex items-center justify-center gap-3 ${
                        isSelected
                          ? 'bg-amber-400 text-amber-950 border-amber-500 shadow-lg scale-102 ring-4 ring-amber-200'
                          : 'bg-slate-50/80 text-slate-800 border-slate-200 hover:bg-white hover:border-amber-300 hover:shadow-sm'
                      }`}
                    >
                      <span className="w-7 h-7 rounded-xl bg-white/80 border border-slate-200 text-slate-700 text-xs font-black flex items-center justify-center shrink-0">
                        {String.fromCharCode(65 + optIdx)}
                      </span>
                      <span className="grow text-center">{opt}</span>
                    </button>
                  );
                })}
              </div>

              {/* Navigation Actions (Previous / Next / Submit) */}
              <div className="flex items-center justify-between pt-6 border-t border-slate-100 gap-3">
                <button
                  type="button"
                  onClick={() => handleGoToQuestion(currentIndex - 1)}
                  disabled={currentIndex === 0}
                  className="px-5 py-3 rounded-2xl border-2 border-slate-200 text-slate-700 hover:bg-slate-50 font-black text-xs md:text-sm flex items-center gap-1.5 transition-all disabled:opacity-30 disabled:pointer-events-none"
                >
                  <ChevronRight className="w-4 h-4" />
                  <span>السؤال السابق</span>
                </button>

                {currentIndex < totalQuestions - 1 ? (
                  <button
                    type="button"
                    onClick={() => handleGoToQuestion(currentIndex + 1)}
                    className="px-6 py-3 rounded-2xl bg-amber-500 hover:bg-amber-600 text-white font-black text-xs md:text-sm flex items-center gap-1.5 shadow-md shadow-amber-200 active:scale-95 transition-all"
                  >
                    <span>السؤال التالي</span>
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={handleSubmitQuiz}
                    disabled={submitting || answeredCount === 0}
                    className="px-7 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:opacity-95 text-white font-black text-sm flex items-center gap-2 shadow-lg shadow-emerald-200 active:scale-95 transition-all disabled:opacity-50"
                  >
                    <Award className="w-5 h-5" />
                    <span>{submitting ? 'جاري الرصد...' : 'تسليم الاختبار ورصد النتيجة ⭐'}</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
