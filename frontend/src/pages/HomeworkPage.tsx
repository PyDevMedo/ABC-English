import React, { useEffect, useState } from 'react';
import { 
  CheckSquare, Send, Volume2, Mic, Clock, CheckCircle2, 
  RotateCcw, Sparkles, FileText, AlertCircle 
} from 'lucide-react';
import { api, playAudio } from '../services/api';
import { AudioRecorder } from '../components/AudioRecorder';
import confetti from 'canvas-confetti';

export const HomeworkPage: React.FC = () => {
  const [assignments, setAssignments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedHw, setSelectedHw] = useState<any>(null);
  const [submissionText, setSubmissionText] = useState('');
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const loadAssignments = () => {
    setLoading(true);
    api.getAssignments()
      .then(setAssignments)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadAssignments();
  }, []);

  const handleSubmit = async () => {
    if (!selectedHw) return;
    setSubmitting(true);
    setSuccessMsg(null);
    try {
      await api.submitAssignment(
        selectedHw.id,
        audioBlob ? 'audio' : 'text',
        submissionText,
        audioBlob || undefined
      );
      confetti({ particleCount: 70, spread: 60, origin: { y: 0.6 } });
      setSuccessMsg('تم تسليم الواجب بنجاح وإشعار المعلم عبر Telegram! أحسنت يا بطل 🌟');
      setTimeout(() => {
        setSelectedHw(null);
        setSubmissionText('');
        setAudioBlob(null);
        loadAssignments();
      }, 2500);
    } catch (err: any) {
      alert(err.message || 'حدث خطأ أثناء تسليم الواجب');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="text-center max-w-xl mx-auto">
        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 text-xs font-black mb-2">
          <CheckSquare className="w-4 h-4" />
          واجباتي المدرسية
        </span>
        <h2 className="text-3xl font-black text-slate-800 font-fredoka">
          قائمة الواجبات والمهام
        </h2>
        <p className="text-xs font-bold text-slate-500 mt-1">
          حل واجباتك، سجل صوتك، وسيصل تنبيه فوري لمعلمك عبر Telegram لتصحيحه.
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 font-bold text-slate-400">جاري تحميل الواجبات...</div>
      ) : assignments.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border-4 border-amber-200 shadow-md">
          <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-3xl mx-auto flex items-center justify-center text-3xl mb-4">
            🎉
          </div>
          <h3 className="text-xl font-black text-slate-800 mb-1">لا توجد واجبات متأخرة!</h3>
          <p className="text-xs text-slate-500 font-bold">
            لقد أنجزت جميع الواجبات المطلوبة، انتظر مهام المعلم القادمة.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {assignments.map((hw) => {
            const isSubmitted = hw.status === 'submitted' || hw.status === 'graded';
            return (
              <div
                key={hw.id}
                className="kid-card p-6 border-emerald-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-black px-2.5 py-0.5 rounded-lg bg-emerald-100 text-emerald-900">
                      واجب قراءة ونطق
                    </span>
                    {hw.status === 'graded' ? (
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        تم التصحيح ({hw.score}/100)
                      </span>
                    ) : isSubmitted ? (
                      <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" />
                        تم التسليم (قيد المراجعة)
                      </span>
                    ) : (
                      <span className="text-xs font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded-md">
                        مطلوب الحل
                      </span>
                    )}
                  </div>
                  <h4 className="text-lg font-black text-slate-900">{hw.title}</h4>
                  <p className="text-xs text-slate-600 font-bold mt-1">{hw.instructions_ar}</p>

                  {hw.feedback && (
                    <div className="mt-2 p-2.5 bg-amber-50 rounded-xl border border-amber-200 text-xs font-bold text-amber-900">
                      💬 <b>ملاحظة المعلم:</b> {hw.feedback}
                    </div>
                  )}
                </div>

                <button
                  type="button"
                  onClick={() => setSelectedHw(hw)}
                  className={`px-5 py-2.5 rounded-2xl font-black text-xs shrink-0 transition-all ${
                    isSubmitted
                      ? 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                      : 'bg-emerald-500 hover:bg-emerald-600 text-white shadow-md shadow-emerald-200'
                  }`}
                >
                  {isSubmitted ? 'عرض التسليم' : 'حل الواجب الآن ✍️'}
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* Homework Solving Modal */}
      {selectedHw && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 shadow-2xl border-4 border-emerald-300 relative">
            <h3 className="text-xl font-black text-slate-900 mb-1">{selectedHw.title}</h3>
            <p className="text-xs text-slate-500 font-bold mb-4">{selectedHw.instructions_ar}</p>

            {successMsg && (
              <div className="p-4 bg-emerald-50 border-2 border-emerald-300 rounded-2xl text-emerald-800 font-bold text-sm text-center mb-4">
                {successMsg}
              </div>
            )}

            {/* Target Words preview */}
            {selectedHw.target_words?.length > 0 && (
              <div className="bg-emerald-50 p-3 rounded-2xl border border-emerald-200 mb-4">
                <span className="text-xs font-bold text-emerald-800 block mb-1">الكلمات المطلوبة:</span>
                <div className="flex flex-wrap gap-2">
                  {selectedHw.target_words.map((w: string, i: number) => (
                    <span key={i} className="bg-white px-3 py-1 rounded-xl text-xs font-black font-fredoka text-emerald-950 border border-emerald-200">
                      {w}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Voice Recorder for homework */}
            <AudioRecorder
              onRecordingComplete={(blob) => setAudioBlob(blob)}
              targetWord={selectedHw.target_words?.[0] || 'Homework'}
            />

            {/* Written text answer option */}
            <div className="mt-4">
              <label className="text-xs font-bold text-slate-700 block mb-1">أو اكتب إجابتك هنا (اختياري):</label>
              <textarea
                value={submissionText}
                onChange={(e) => setSubmissionText(e.target.value)}
                placeholder="اكتب الجملة أو الكلمات المطلوبة..."
                rows={2}
                className="w-full p-3 rounded-2xl border-2 border-slate-200 text-xs font-bold focus:border-emerald-400 focus:outline-none"
              />
            </div>

            <div className="flex gap-3 justify-end mt-6">
              <button
                type="button"
                onClick={() => setSelectedHw(null)}
                className="px-4 py-2 text-slate-500 font-bold text-xs"
              >
                إلغاء
              </button>
              <button
                type="button"
                onClick={handleSubmit}
                disabled={submitting}
                className="kid-button-green px-6 py-2.5 text-xs"
              >
                <Send className="w-4 h-4" />
                <span>{submitting ? 'جاري التسليم...' : 'تسليم الواجب للمعلم 🚀'}</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
