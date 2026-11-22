import React, { useState, useEffect, useRef } from 'react';
import { 
  X, Volume2, Sparkles, BookOpen, Layers, CheckCircle2, 
  ArrowLeft, ArrowRight, Star, Trophy, Mic, Camera, Upload, 
  AlertCircle, PenTool, Check, RotateCcw
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
  const [activeTab, setActiveTab] = useState<'intro' | 'phonics' | 'words' | 'sentences' | 'lab' | 'handwriting'>('intro');
  const [evaluating, setEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState<any>(null);
  const [selectedWordForLab, setSelectedWordForLab] = useState<string>('Ship');
  const [completed, setCompleted] = useState(false);

  // Handwriting Homework State
  const [assignment, setAssignment] = useState<any>(null);
  const [hwImage, setHwImage] = useState<File | null>(null);
  const [hwImagePreview, setHwImagePreview] = useState<string | null>(null);
  const [hwSubmitting, setHwSubmitting] = useState(false);
  const [hwSubmitted, setHwSubmitted] = useState(false);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.getLevelDetail(levelId),
      api.getAssignmentByLevel(levelId)
    ])
      .then(([lvlData, asgData]) => {
        setLevelData(lvlData);
        setAssignment(asgData);
        if (asgData?.is_submitted) {
          setHwSubmitted(true);
          if (asgData.image_url) {
            setHwImagePreview(asgData.image_url);
          }
        }
        if (lvlData.lessons?.[0]?.sections) {
          const wordsSec = lvlData.lessons[0].sections.find((s: any) => s.section_type === 'words');
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

  const handleImageSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setHwImage(file);
      setHwImagePreview(URL.createObjectURL(file));
    }
  };

  const submitHandwritingHomework = async () => {
    if (!hwImage || !assignment?.id) return;
    setHwSubmitting(true);
    try {
      await api.submitHandwritingPhoto(assignment.id, hwImage);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      setHwSubmitted(true);
      if (onLessonCompleted) onLessonCompleted();
    } catch (err: any) {
      alert(err.message || 'فشل رفع صورة الواجب');
    } finally {
      setHwSubmitting(false);
    }
  };

  const finishLesson = async () => {
    if (!hwSubmitted) {
      setActiveTab('handwriting');
      return;
    }
    if (lesson?.id) {
      await api.completeLesson(lesson.id);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      setCompleted(true);
      if (onLessonCompleted) onLessonCompleted();
      setTimeout(() => {
        onClose();
      }, 1800);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl max-w-4xl w-full max-h-[92vh] flex flex-col shadow-2xl border-4 border-amber-300 relative overflow-hidden">
        {/* Modal Top Bar */}
        <div className="bg-gradient-to-r from-amber-400 via-rose-300 to-purple-400 p-4 sm:p-6 text-amber-950 flex items-center justify-between shrink-0">
          <div>
            <span className="text-xs font-black bg-white/70 px-3 py-1 rounded-full text-purple-900 inline-block mb-1">
              ABC Level {levelData.level_number}
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
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'intro' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            📖 مقدمة القصة
          </button>
          <button
            onClick={() => setActiveTab('phonics')}
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'phonics' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            🔤 أصوات الحروف
          </button>
          <button
            onClick={() => setActiveTab('words')}
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'words' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            🧩 تركيب الكلمات
          </button>
          <button
            onClick={() => setActiveTab('sentences')}
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'sentences' ? 'bg-amber-400 text-amber-950 shadow-sm' : 'text-slate-600 hover:bg-white'
            }`}
          >
            📝 الجمل والكلمات البصرية
          </button>
          <button
            onClick={() => setActiveTab('lab')}
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === 'lab' ? 'bg-purple-500 text-white shadow-sm' : 'text-purple-700 bg-purple-50 hover:bg-purple-100'
            }`}
          >
            🤖 مختبر النطق
          </button>
          <button
            onClick={() => setActiveTab('handwriting')}
            className={`px-3.5 py-2 rounded-2xl text-xs sm:text-sm font-black whitespace-nowrap transition-all flex items-center gap-1.5 ${
              activeTab === 'handwriting'
                ? 'bg-gradient-to-r from-rose-500 to-orange-500 text-white shadow-md shadow-rose-200'
                : hwSubmitted
                ? 'bg-emerald-100 text-emerald-800'
                : 'bg-rose-100 text-rose-800 hover:bg-rose-200 animate-pulse'
            }`}
          >
            <PenTool className="w-4 h-4" />
            <span>✍️ واجب الدفتر (إجباري)</span>
            {hwSubmitted && <Check className="w-3.5 h-3.5 text-emerald-600 stroke-[3]" />}
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

              {evalResult && (
                <div className="bg-white rounded-3xl p-6 border-4 border-amber-300 shadow-lg space-y-4">
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

                  <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-950 font-bold text-sm">
                    {evalResult.feedback_text}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 6: MANDATORY HANDWRITING HOMEWORK (واجب الكتابة الورقية وتصوير الدفتر) */}
          {activeTab === 'handwriting' && (
            <div className="space-y-6">
              {/* Mandatory Alert Banner */}
              <div className="bg-gradient-to-r from-rose-50 to-orange-50 p-6 rounded-3xl border-2 border-rose-200 text-center relative overflow-hidden">
                <span className="text-xs font-black bg-rose-500 text-white px-3 py-1 rounded-full mb-2 inline-block">
                  شرط إلزامي للانتقال للدرس التالي 🔒
                </span>
                <h4 className="text-xl sm:text-2xl font-black text-slate-900 mb-1">
                  واجب كتابة وتثبيت الكلمات في الدفتر ✍️
                </h4>
                <p className="text-xs sm:text-sm font-bold text-slate-600 max-w-xl mx-auto">
                  حتى تثبت الحروف والكلمات في ذاكرتك، أحضر كراسة اللغة الإنجليزية الخاصة بك واكتب الكلمات بخطك الجميل، ثم التقط صورة لدفترك وارفعها هنا!
                </p>
              </div>

              {/* 4-Lines Handwriting Guide Sheet Simulation */}
              <div className="bg-white rounded-3xl p-6 border-2 border-slate-200 shadow-sm space-y-4">
                <div className="flex items-center justify-between border-b pb-3">
                  <span className="text-xs font-black text-slate-700 flex items-center gap-1.5">
                    <PenTool className="w-4 h-4 text-rose-500" />
                    الكلمات والجمل المطلوب كتابتها في كراستك:
                  </span>
                  <span className="text-[11px] font-bold text-slate-400">كراسة تحسين الخط 4-Lines</span>
                </div>

                {/* 4-lines Ruled Notebook Preview */}
                <div className="bg-amber-50/40 rounded-2xl p-5 border border-amber-200 space-y-4 font-fredoka">
                  {assignment?.target_words?.map((w: string, i: number) => (
                    <div key={i} className="relative py-2 border-b-2 border-slate-200 select-none">
                      {/* 4 dashed guide lines */}
                      <div className="absolute inset-0 flex flex-col justify-between pointer-events-none opacity-20">
                        <div className="border-b border-rose-500 w-full"></div>
                        <div className="border-b border-dashed border-sky-500 w-full"></div>
                        <div className="border-b border-sky-500 w-full"></div>
                        <div className="border-b border-rose-500 w-full"></div>
                      </div>
                      <div className="flex items-center justify-between relative z-10 px-3">
                        <span className="text-2xl sm:text-3xl font-black text-slate-800 tracking-wider" dir="ltr">
                          {w}
                        </span>
                        <button
                          type="button"
                          onClick={() => playAudio(undefined, w)}
                          className="px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-bold border border-slate-200 flex items-center gap-1"
                        >
                          <Volume2 className="w-3.5 h-3.5" />
                          نطق
                        </button>
                      </div>
                    </div>
                  ))}

                  {assignment?.target_sentences?.map((s: string, i: number) => (
                    <div key={i} className="relative py-2 border-b-2 border-slate-200 select-none">
                      <div className="flex items-center justify-between relative z-10 px-3">
                        <span className="text-xl sm:text-2xl font-black text-indigo-900 tracking-wide" dir="ltr">
                          {s}
                        </span>
                        <button
                          type="button"
                          onClick={() => playAudio(undefined, s)}
                          className="px-2.5 py-1 bg-white hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-bold border border-slate-200 flex items-center gap-1"
                        >
                          <Volume2 className="w-3.5 h-3.5" />
                          نطق
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Photo Upload & Camera Action Box */}
              <div className="bg-slate-50 p-6 rounded-3xl border-2 border-dashed border-slate-300 text-center space-y-4">
                {/* Hidden Inputs for Camera and File Picker */}
                <input
                  type="file"
                  accept="image/*"
                  capture="environment"
                  ref={cameraInputRef}
                  onChange={handleImageSelected}
                  className="hidden"
                />
                <input
                  type="file"
                  accept="image/*"
                  ref={fileInputRef}
                  onChange={handleImageSelected}
                  className="hidden"
                />

                {hwImagePreview ? (
                  /* Image Preview */
                  <div className="space-y-4 max-w-sm mx-auto">
                    <div className="relative rounded-2xl overflow-hidden border-4 border-white shadow-xl max-h-72">
                      <img
                        src={hwImagePreview}
                        alt="Handwriting homework preview"
                        className="w-full h-auto object-cover"
                      />
                      {hwSubmitted && (
                        <div className="absolute inset-0 bg-emerald-950/60 backdrop-blur-xs flex flex-col items-center justify-center text-white p-4">
                          <CheckCircle2 className="w-12 h-12 text-emerald-400 mb-1" />
                          <span className="font-black text-base">تم اعتماد وتسليم الواجب!</span>
                          <span className="text-xs opacity-90">وصلت الصورة فوراً للمدرس عبر Telegram</span>
                        </div>
                      )}
                    </div>

                    {!hwSubmitted && (
                      <div className="flex gap-2 justify-center">
                        <button
                          type="button"
                          onClick={() => {
                            setHwImage(null);
                            setHwImagePreview(null);
                          }}
                          className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-xl text-xs flex items-center gap-1"
                        >
                          <RotateCcw className="w-3.5 h-3.5" />
                          إعادة التصوير
                        </button>
                        <button
                          type="button"
                          onClick={submitHandwritingHomework}
                          disabled={hwSubmitting}
                          className="kid-button-green px-6 py-2 text-xs font-black"
                        >
                          {hwSubmitting ? 'جاري الرفع...' : 'تسليم الصورة للمدرس 🚀'}
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  /* Action Buttons to Capture or Select */
                  <div className="space-y-3">
                    <p className="text-xs font-black text-slate-700">
                      اختر طريقة تصوير كراستك الآن:
                    </p>
                    <div className="flex flex-col sm:flex-row gap-3 justify-center max-w-md mx-auto">
                      <button
                        type="button"
                        onClick={() => cameraInputRef.current?.click()}
                        className="flex-1 py-3.5 px-4 bg-gradient-to-r from-rose-500 to-pink-600 hover:opacity-95 text-white font-black rounded-2xl shadow-md shadow-rose-200 flex items-center justify-center gap-2 text-sm active:scale-95 transition-all"
                      >
                        <Camera className="w-5 h-5" />
                        <span>تصوير مباشر بالكاميرا 📷</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="flex-1 py-3.5 px-4 bg-white hover:bg-slate-100 text-slate-800 font-black rounded-2xl border-2 border-slate-200 flex items-center justify-center gap-2 text-sm active:scale-95 transition-all shadow-sm"
                      >
                        <Upload className="w-5 h-5 text-slate-500" />
                        <span>اختيار صورة من المعرض 🖼️</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="bg-slate-50 border-t-2 border-slate-100 p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 text-slate-500 font-bold text-xs hover:text-slate-800"
          >
            إغلاق
          </button>

          <div className="flex items-center gap-3">
            {!hwSubmitted && (
              <span className="text-[11px] font-black text-rose-600 flex items-center gap-1">
                <AlertCircle className="w-4 h-4" />
                يجب تسليم واجب الدفتر لفتح المرحلة القادمة!
              </span>
            )}

            <button
              onClick={finishLesson}
              disabled={completed}
              className={`px-6 py-2.5 text-xs font-black rounded-2xl transition-all flex items-center gap-1.5 ${
                hwSubmitted
                  ? 'kid-button-green'
                  : 'bg-rose-500 hover:bg-rose-600 text-white shadow-md shadow-rose-200'
              }`}
            >
              {completed ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  <span>أحسنت! تم إكمال الدرس وفتح المستوى التالي</span>
                </>
              ) : hwSubmitted ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  <span>إتمام الدرس والتقدم للمرحلة التالية 🌟</span>
                </>
              ) : (
                <>
                  <PenTool className="w-4 h-4" />
                  <span>تصوير وتسليم واجب الدفتر أولاً ✍️</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
