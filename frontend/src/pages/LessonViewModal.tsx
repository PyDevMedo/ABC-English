import React, { useState } from 'react';
import { 
  X, Volume2, Sparkles, BookOpen, Layers, CheckCircle2, 
  ArrowLeft, ArrowRight, Star, Trophy, Mic
} from 'lucide-react';
import { playAudio, api } from '../services/api';
import { AudioRecorder } from '../components/AudioRecorder';
import confetti from 'canvas-confetti';

interface LessonViewModalProps {
  levelId: number;
  onClose: () => void;
  onLessonCompleted?: () => void;
}

export const LessonViewModal: React.FC<LessonViewModalProps> = ({
  levelId,
  onClose,
  onLessonCompleted
}) => {
  const [levelData, setLevelData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'intro' | 'phonics' | 'words' | 'sentences' | 'lab'>('intro');
  const [evaluating, setEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState<any>(null);
  const [selectedWordForLab, setSelectedWordForLab] = useState<string>('Ship');
  const [completed, setCompleted] = useState(false);

  React.useEffect(() => {
    setLoading(true);
    api.getLevelDetail(levelId)
      .then((data) => {
        setLevelData(data);
        if (data.lessons?.[0]?.sections) {
          const wordsSec = data.lessons[0].sections.find((s: any) => s.section_type === 'words');
          if (wordsSec?.content_json?.words?.[0]?.word) {
            setSelectedWordForLab(wordsSec.content_json.words[0].word);
          }
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [levelId]);

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl p-8 text-center font-bold text-slate-700 animate-pulse">
          جاري تجهيز الدرس والمؤثرات الصوتية... 🎧
        </div>
      </div>
    );
  }

  if (!levelData) return null;

  const lesson = levelData.lessons?.[0];
  const sections = lesson?.sections || [];
  const introSec = sections.find((s: any) => s.section_type === 'intro');
  const phonicsSec = sections.find((s: any) => s.section_type === 'phonics');
  const wordsSec = sections.find((s: any) => s.section_type === 'words');
  const sentencesSec = sections.find((s: any) => s.section_type === 'sentences');

  const handlePronunciationRecord = async (blob: Blob) => {
    setEvaluating(true);
    setEvalResult(null);
    try {
      const res = await api.evaluatePronunciation(selectedWordForLab, blob);
      setEvalResult(res);
      if (res.overall_score >= 80) {
        confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  const handleSimulatedPronunciation = async (text: string) => {
    setEvaluating(true);
    setEvalResult(null);
    try {
      const res = await api.evaluatePronunciation(selectedWordForLab, undefined, text);
      setEvalResult(res);
      if (res.overall_score >= 80) {
        confetti({ particleCount: 50, spread: 60, origin: { y: 0.7 } });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  const finishLesson = async () => {
    if (lesson?.id) {
      await api.completeLesson(lesson.id);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      setCompleted(true);
      if (onLessonCompleted) onLessonCompleted();
      setTimeout(() => {
        onClose();
      }, 2000);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl max-w-4xl w-full max-h-[92vh] flex flex-col shadow-2xl border-4 border-amber-300 relative overflow-hidden">
        {/* Modal Top Bar */}
        <div className="bg-gradient-to-r from-amber-400 via-rose-300 to-purple-400 p-4 sm:p-6 text-amber-950 flex items-center justify-between shrink-0">
          <div>
            <span className="text-xs font-black bg-white/70 px-3 py-1 rounded-full text-purple-900 inline-block mb-1">
              Level {levelData.level_number}
            </span>
            <h3 className="text-xl sm:text-2xl font-black font-fredoka">{levelData.title}</h3>
            <p className="text-xs sm:text-sm font-bold text-slate-800">{levelData.subtitle}</p>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-2xl bg-white/80 hover:bg-white flex items-center justify-center text-slate-700 shadow-md transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Lesson Tabs Navigation */}
        <div className="flex border-b-2 border-amber-100 bg-amber-50/70 p-2 gap-1 overflow-x-auto shrink-0 scrollbar-none">
          <button
            onClick={() => setActiveTab('intro')}
            className={`px-4 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'intro' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            📖 مقدمة القصة
          </button>
          <button
            onClick={() => setActiveTab('phonics')}
            className={`px-4 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'phonics' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            🔤 أصوات الحروف
          </button>
          <button
            onClick={() => setActiveTab('words')}
            className={`px-4 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'words' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            🧩 تركيب الكلمات
          </button>
          <button
            onClick={() => setActiveTab('sentences')}
            className={`px-4 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'sentences' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            📝 الجمل والكلمات البصرية
          </button>
          <button
            onClick={() => setActiveTab('lab')}
            className={`px-4 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'lab' ? 'bg-purple-500 text-white shadow-sm' : 'text-purple-700 bg-purple-50 hover:bg-purple-100'
            }`}
          >
            🤖 مختبر النطق الذكي
          </button>
        </div>

        {/* Modal Body Content */}
        <div className="p-4 sm:p-6 overflow-y-auto grow space-y-6">
          {/* TAB 1: INTRO */}
          {activeTab === 'intro' && (
            <div className="space-y-4 text-center max-w-xl mx-auto py-6">
              <div className="w-20 h-20 bg-amber-100 rounded-3xl mx-auto flex items-center justify-center text-4xl shadow-inner border-2 border-amber-300">
                ✨
              </div>
              <h4 className="text-2xl font-black text-slate-800">مرحباً بك يا بطل في هذا المستوى!</h4>
              <p className="text-base text-slate-700 leading-relaxed font-bold bg-amber-50 p-6 rounded-3xl border-2 border-amber-200">
                {introSec?.content_json?.text_ar || levelData.description}
              </p>
              <button
                onClick={() => setActiveTab('phonics')}
                className="kid-button-primary px-8 py-3 text-base mx-auto mt-4"
              >
                <span>ابدأ استكشاف الأصوات</span>
                <ArrowLeft className="w-5 h-5" />
              </button>
            </div>
          )}

          {/* TAB 2: PHONICS LETTERS */}
          {activeTab === 'phonics' && (
            <div>
              <div className="text-center mb-6">
                <h4 className="text-xl font-black text-slate-800">استمع لأصوات الحروف السحرية 🎵</h4>
                <p className="text-xs text-slate-500 font-bold">اضغط على أي حرف لسماع صوته الواضح باللهجة الأمريكية</p>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                {phonicsSec?.content_json?.letters?.map((letter: any, idx: number) => (
                  <div
                    key={idx}
                    onClick={() => playAudio(undefined, `${letter.name}, sound: ${letter.symbol}`)}
                    className="kid-card p-4 text-center cursor-pointer border-sky-300 hover:border-amber-400 group"
                  >
                    <div className="text-4xl sm:text-5xl font-black font-fredoka text-sky-600 group-hover:scale-110 transition-transform mb-2">
                      {letter.symbol}
                    </div>
                    <div className="text-xs font-black text-slate-800 mb-1">{letter.name}</div>
                    <div className="text-[11px] text-amber-700 font-bold mb-3">{letter.arabic_desc}</div>
                    <button
                      type="button"
                      className="w-full py-1.5 bg-sky-100 hover:bg-sky-200 text-sky-700 rounded-xl text-xs font-bold flex items-center justify-center gap-1"
                    >
                      <Volume2 className="w-4 h-4" />
                      استمع
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: WORDS BLENDING */}
          {activeTab === 'words' && (
            <div>
              <div className="text-center mb-6">
                <h4 className="text-xl font-black text-slate-800">دمج وقراءة الكلمات 🧩</h4>
                <p className="text-xs text-slate-500 font-bold">استمع لتفكيك الأصوات وقراءة الكلمة كاملة</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {wordsSec?.content_json?.words?.map((w: any, idx: number) => (
                  <div
                    key={idx}
                    className="kid-card p-5 border-amber-200 text-center relative group"
                  >
                    <div className="text-3xl font-black font-fredoka text-slate-800 mb-1">
                      {w.word}
                    </div>
                    {/* Phoneme pills */}
                    <div className="flex justify-center gap-1.5 my-2">
                      {w.phonemes.split('-').map((p: string, pIdx: number) => (
                        <span key={pIdx} className="bg-amber-100 text-amber-900 font-fredoka text-xs font-bold px-2 py-0.5 rounded-lg border border-amber-300">
                          {p}
                        </span>
                      ))}
                    </div>
                    <div className="text-sm font-bold text-slate-600 mb-4">{w.translation_ar}</div>
                    
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => playAudio(w.audio_url, w.word)}
                        className="flex-1 py-2 bg-amber-400 hover:bg-amber-500 text-amber-950 font-bold rounded-xl text-xs flex items-center justify-center gap-1 shadow-sm"
                      >
                        <Volume2 className="w-4 h-4" />
                        استمع
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedWordForLab(w.word);
                          setActiveTab('lab');
                        }}
                        className="py-2 px-3 bg-purple-100 hover:bg-purple-200 text-purple-800 font-bold rounded-xl text-xs flex items-center justify-center"
                        title="تدرب على نطق هذه الكلمة"
                      >
                        <Mic className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 4: SENTENCES & SIGHT WORDS */}
          {activeTab === 'sentences' && (
            <div className="space-y-6">
              {/* Sight words */}
              <div>
                <h5 className="text-base font-black text-slate-800 mb-3 flex items-center gap-2">
                  <Star className="w-5 h-5 text-amber-500 fill-amber-400" />
                  الكلمات البصرية (Sight Words):
                </h5>
                <div className="flex flex-wrap gap-2">
                  {sentencesSec?.content_json?.sight_words?.map((sw: string, idx: number) => (
                    <button
                      key={idx}
                      onClick={() => playAudio(undefined, sw)}
                      className="px-4 py-2 bg-rose-100 hover:bg-rose-200 text-rose-800 rounded-2xl font-black font-fredoka text-base border-2 border-rose-300 flex items-center gap-1.5 transition-all"
                    >
                      <Volume2 className="w-4 h-4" />
                      {sw}
                    </button>
                  ))}
                </div>
              </div>

              {/* Sentences */}
              <div>
                <h5 className="text-base font-black text-slate-800 mb-3">الجمل القصيرة للقراءة:</h5>
                <div className="space-y-3">
                  {sentencesSec?.content_json?.sentences?.map((st: any, idx: number) => (
                    <div
                      key={idx}
                      className="bg-white p-4 rounded-2xl border-2 border-slate-200 flex items-center justify-between gap-4 shadow-sm"
                    >
                      <div>
                        <span className="text-lg font-black font-fredoka text-slate-800 block text-left" dir="ltr">
                          {st.text}
                        </span>
                        <span className="text-xs font-bold text-slate-500">{st.translation_ar}</span>
                      </div>
                      <button
                        type="button"
                        onClick={() => playAudio(undefined, st.text)}
                        className="w-10 h-10 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-800 flex items-center justify-center shrink-0"
                      >
                        <Volume2 className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: AI PRONUNCIATION LAB */}
          {activeTab === 'lab' && (
            <div className="space-y-6">
              <div className="bg-purple-50 p-6 rounded-3xl border-2 border-purple-200 text-center">
                <span className="text-xs font-black text-purple-700 bg-purple-200/60 px-3 py-1 rounded-full mb-2 inline-block">
                  الكلمة المختارة للتحدي:
                </span>
                <div className="text-4xl font-black font-fredoka text-purple-950 my-2 tracking-wide">
                  {selectedWordForLab}
                </div>
                <button
                  onClick={() => playAudio(undefined, selectedWordForLab)}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-purple-700 bg-white px-3 py-1.5 rounded-xl shadow-sm hover:bg-purple-100"
                >
                  <Volume2 className="w-4 h-4" />
                  استمع للنطق الصحيح
                </button>
              </div>

              {/* Mic recorder widget */}
              <AudioRecorder
                onRecordingComplete={handlePronunciationRecord}
                onSimulatedSpeech={handleSimulatedPronunciation}
                targetWord={selectedWordForLab}
                isEvaluating={evaluating}
              />

              {evaluating && (
                <div className="text-center font-bold text-purple-800 animate-pulse text-sm">
                  مدرس الذكاء الاصطناعي يحلل الأصوات الفردية الآن... 🧠
                </div>
              )}

              {/* Evaluation Result Card */}
              {evalResult && (
                <div className="bg-white rounded-3xl p-6 border-4 border-amber-300 shadow-lg space-y-4 animate-in fade-in">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-xs font-bold text-slate-500">تقييم النطق:</span>
                      <div className="text-3xl font-black text-slate-800">{evalResult.overall_score}/100</div>
                    </div>
                    <div className="flex gap-1">
                      {[1, 2, 3].map((s) => (
                        <Star
                          key={s}
                          className={`w-7 h-7 ${
                            evalResult.overall_score >= s * 30
                              ? 'text-amber-400 fill-amber-400'
                              : 'text-slate-200'
                          }`}
                        />
                      ))}
                    </div>
                  </div>

                  {/* Phoneme Breakdown */}
                  <div className="bg-slate-50 p-3 rounded-2xl border border-slate-200">
                    <span className="text-xs font-bold text-slate-600 block mb-1">الأصوات المحللة (Phonemes):</span>
                    <div className="flex gap-2">
                      {evalResult.correct_phonemes?.map((p: string, i: number) => (
                        <span key={i} className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-1 rounded-lg border border-emerald-300">
                          {p} ✓
                        </span>
                      ))}
                      {evalResult.error_phonemes?.map((p: string, i: number) => (
                        <span key={i} className="bg-rose-100 text-rose-800 text-xs font-bold px-2.5 py-1 rounded-lg border border-rose-300">
                          {p} (يحتاج تحسين)
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Feedback Message */}
                  <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-950 font-bold text-sm">
                    {evalResult.feedback_text}
                  </div>

                  {evalResult.adaptive_triggered && (
                    <div className="p-3 bg-purple-100 rounded-2xl border border-purple-300 text-purple-900 text-xs font-bold flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-purple-600 shrink-0" />
                      <span>
                        قام مدرس الذكاء الاصطناعي بتوليد تدريبات إضافية مخصصة لصوت {evalResult.weakness_detected} في قسم "المسار الذكي"!
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="bg-slate-50 border-t-2 border-slate-100 p-4 flex items-center justify-between shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-500 font-bold text-sm hover:text-slate-800"
          >
            إغلاق
          </button>

          <button
            onClick={finishLesson}
            disabled={completed}
            className="kid-button-green px-6 py-2.5 text-sm"
          >
            <CheckCircle2 className="w-5 h-5" />
            <span>{completed ? 'أحسنت! تم إكمال الدرس' : 'إتمام الدرس وحصد 30 XP 🌟'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
