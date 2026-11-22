import React, { useState } from 'react';
import { Mic, Volume2, Sparkles, Star, Award, RotateCcw } from 'lucide-react';
import { api, playAudio } from '../services/api';
import { AudioRecorder } from '../components/AudioRecorder';
import confetti from 'canvas-confetti';

export const PronunciationPage: React.FC = () => {
  const [targetText, setTargetText] = useState('Ship');
  const [evaluating, setEvaluating] = useState(false);
  const [evalResult, setEvalResult] = useState<any>(null);

  const popularWords = [
    { word: 'Ship', phonemes: 'SH-I-P', level: 'Level 5 (Digraphs)' },
    { word: 'Shop', phonemes: 'SH-O-P', level: 'Level 5 (Digraphs)' },
    { word: 'Cat', phonemes: 'C-A-T', level: 'Level 2 (CVC)' },
    { word: 'Dog', phonemes: 'D-O-G', level: 'Level 2 (CVC)' },
    { word: 'Sun', phonemes: 'S-U-N', level: 'Level 3 (Short Vowels)' },
    { word: 'Duck', phonemes: 'D-U-CK', level: 'Level 6 (Advanced)' },
    { word: 'Train', phonemes: 'T-R-AI-N', level: 'Level 7 (Vowel Teams)' },
    { word: 'Moon', phonemes: 'M-OO-N', level: 'Level 8 (Review)' }
  ];

  const handleRecording = async (blob: Blob) => {
    setEvaluating(true);
    setEvalResult(null);
    try {
      const res = await api.evaluatePronunciation(targetText, blob);
      setEvalResult(res);
      if (res.overall_score >= 80) {
        confetti({ particleCount: 60, spread: 60, origin: { y: 0.6 } });
      }
    } catch (err: any) {
      alert(err.message || 'فشل التقييم الصوتي');
    } finally {
      setEvaluating(false);
    }
  };

  const handleSimulated = async (text: string) => {
    setEvaluating(true);
    setEvalResult(null);
    try {
      const res = await api.evaluatePronunciation(targetText, undefined, text);
      setEvalResult(res);
      if (res.overall_score >= 80) {
        confetti({ particleCount: 60, spread: 60, origin: { y: 0.6 } });
      }
    } catch (err: any) {
      alert(err.message || 'فشل التقييم الصوتي');
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-rose-500 rounded-3xl p-6 md:p-8 text-white text-center shadow-xl relative overflow-hidden">
        <span className="text-xs font-black bg-white/20 px-3.5 py-1 rounded-full mb-2 inline-block">
          AI Pronunciation Assessment
        </span>
        <h2 className="text-3xl md:text-4xl font-black font-fredoka">
          مدرس النطق الذكي للأطفال
        </h2>
        <p className="text-xs md:text-sm font-bold text-purple-100 mt-2 max-w-lg mx-auto">
          تحليل صوتي دقيق لكل Phoneme مع مقارنة النطق النموذجي وتوجيهك خطوة بخطوة 🎤
        </p>
      </div>

      {/* Target Word Selector Box */}
      <div className="kid-card p-6 border-purple-200">
        <h3 className="text-base font-black text-slate-800 mb-3 text-center">
          اختر كلمة للتحدي أو اكتب الكلمة المطلوبة:
        </h3>

        <div className="flex flex-wrap justify-center gap-2 mb-6">
          {popularWords.map((item) => (
            <button
              key={item.word}
              type="button"
              onClick={() => {
                setTargetText(item.word);
                setEvalResult(null);
              }}
              className={`px-4 py-2 rounded-2xl font-black font-fredoka text-sm transition-all ${
                targetText.toLowerCase() === item.word.toLowerCase()
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-200 scale-105'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {item.word}
            </button>
          ))}
        </div>

        {/* Selected target showcase */}
        <div className="bg-purple-50 p-6 rounded-3xl border-2 border-purple-200 text-center max-w-sm mx-auto mb-6">
          <span className="text-xs font-bold text-purple-700">الكلمة المحددة:</span>
          <div className="text-5xl font-black font-fredoka text-purple-950 my-2 tracking-wide">
            {targetText}
          </div>
          <button
            type="button"
            onClick={() => playAudio(undefined, targetText)}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-purple-700 bg-white px-3.5 py-1.5 rounded-xl shadow-sm hover:bg-purple-100"
          >
            <Volume2 className="w-4 h-4" />
            استمع للنطق الصحيح
          </button>
        </div>

        {/* Mic Recorder */}
        <AudioRecorder
          onRecordingComplete={handleRecording}
          onSimulatedSpeech={handleSimulated}
          targetWord={targetText}
          isEvaluating={evaluating}
        />

        {evaluating && (
          <div className="text-center font-bold text-purple-800 animate-pulse text-sm my-4">
            الذكاء الاصطناعي يقوم بالمطابقة الصوتية Phoneme Alignment الآن... 🧠
          </div>
        )}

        {/* Result Card */}
        {evalResult && (
          <div className="bg-white rounded-3xl p-6 border-4 border-amber-300 shadow-xl space-y-4 max-w-md mx-auto mt-6 animate-in fade-in">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-slate-500">درجة النطق:</span>
                <div className="text-4xl font-black text-slate-800 font-fredoka">{evalResult.overall_score}/100</div>
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

            {/* Phonemes */}
            <div className="bg-slate-50 p-3 rounded-2xl border border-slate-200">
              <span className="text-xs font-bold text-slate-600 block mb-1">الأصوات المحللة (Phonemes):</span>
              <div className="flex flex-wrap gap-1.5">
                {evalResult.correct_phonemes?.map((p: string, i: number) => (
                  <span key={i} className="bg-emerald-100 text-emerald-800 text-xs font-black px-2.5 py-0.5 rounded-lg border border-emerald-300">
                    {p} ✓
                  </span>
                ))}
                {evalResult.error_phonemes?.map((p: string, i: number) => (
                  <span key={i} className="bg-rose-100 text-rose-800 text-xs font-black px-2.5 py-0.5 rounded-lg border border-rose-300">
                    {p} (يحتاج تدريب)
                  </span>
                ))}
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-950 font-bold text-sm">
              {evalResult.feedback_text}
            </div>

            {evalResult.adaptive_triggered && (
              <div className="p-3 bg-purple-100 rounded-2xl border border-purple-300 text-purple-900 text-xs font-bold flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-600 shrink-0" />
                <span>
                  اكتشف المدرس الذكي تكرار الصعوبة في {evalResult.weakness_detected}، وتم إعداد تدريبات خاصة لك في قسم "المسار الذكي"!
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
