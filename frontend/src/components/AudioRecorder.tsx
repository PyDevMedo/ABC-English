import React, { useState, useRef } from 'react';
import { Mic, Square, Play, RotateCcw, Sparkles } from 'lucide-react';

interface AudioRecorderProps {
  onRecordingComplete: (blob: Blob) => void;
  onSimulatedSpeech?: (text: string) => void;
  targetWord?: string;
  isEvaluating?: boolean;
}

export const AudioRecorder: React.FC<AudioRecorderProps> = ({
  onRecordingComplete,
  onSimulatedSpeech,
  targetWord = '',
  isEvaluating = false
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      chunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setHasPermission(true);
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
        onRecordingComplete(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.warn("Microphone access not available or denied:", err);
      setHasPermission(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const playRecordedAudio = () => {
    if (audioUrl) {
      const a = new Audio(audioUrl);
      a.play();
    }
  };

  const resetRecording = () => {
    setAudioUrl(null);
    setIsRecording(false);
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-amber-50/80 rounded-3xl border-2 border-dashed border-amber-300 w-full max-w-md mx-auto my-4">
      <div className="text-center mb-4">
        <h4 className="text-lg font-bold text-amber-900 flex items-center justify-center gap-2">
          <Sparkles className="w-5 h-5 text-amber-500 animate-spin" />
          مختبر النطق الذكي
        </h4>
        <p className="text-sm text-amber-700">اضغط على الميكروفون وانطق الكلمة بصوتك الجميل</p>
      </div>

      <div className="relative mb-4">
        {isRecording && (
          <div className="absolute inset-0 rounded-full bg-rose-400 animate-ping opacity-75"></div>
        )}

        {!isRecording ? (
          <button
            type="button"
            onClick={startRecording}
            disabled={isEvaluating}
            className="relative w-24 h-24 rounded-full bg-gradient-to-tr from-amber-400 to-rose-400 hover:from-amber-500 hover:to-rose-500 text-white flex flex-col items-center justify-center shadow-lg transform active:scale-95 transition-all"
            title="ابدأ التسجيل"
          >
            <Mic className="w-10 h-10 mb-1" />
            <span className="text-xs font-bold">سجّل الآن</span>
          </button>
        ) : (
          <button
            type="button"
            onClick={stopRecording}
            className="relative w-24 h-24 rounded-full bg-rose-500 hover:bg-rose-600 text-white flex flex-col items-center justify-center shadow-lg transform active:scale-95 transition-all animate-pulse"
            title="إنهاء التسجيل"
          >
            <Square className="w-10 h-10 mb-1 fill-white" />
            <span className="text-xs font-bold">إيقاف</span>
          </button>
        )}
      </div>

      {isRecording && (
        <div className="text-rose-600 font-bold text-sm animate-bounce flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-rose-500 inline-block animate-ping"></span>
          الذكاء الاصطناعي يستمع إليك الآن... 👂
        </div>
      )}

      {audioUrl && !isRecording && (
        <div className="flex items-center gap-3 mt-2 bg-white px-4 py-2 rounded-2xl shadow-sm border border-amber-200">
          <button
            type="button"
            onClick={playRecordedAudio}
            className="flex items-center gap-1 text-sm font-bold text-emerald-600 hover:text-emerald-700"
          >
            <Play className="w-4 h-4 fill-emerald-600" />
            استمع لصوتك
          </button>
          <span className="text-slate-300">|</span>
          <button
            type="button"
            onClick={resetRecording}
            className="flex items-center gap-1 text-sm font-bold text-slate-500 hover:text-slate-700"
          >
            <RotateCcw className="w-4 h-4" />
            إعادة
          </button>
        </div>
      )}

      {/* Fallback for environments without mic or for quick browser test */}
      {hasPermission === false && onSimulatedSpeech && (
        <div className="mt-4 p-3 bg-amber-100 rounded-2xl text-center border border-amber-300 text-xs text-amber-900">
          <p className="mb-2 font-bold">لم نتمكن من الوصول للميكروفون، يمكنك تجربة التقييم الذكي بضغطة زر:</p>
          <div className="flex gap-2 justify-center">
            <button
              type="button"
              onClick={() => onSimulatedSpeech(targetWord)}
              className="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-xl shadow-sm"
            >
              نطق متقن ({targetWord}) 🌟
            </button>
            <button
              type="button"
              onClick={() => onSimulatedSpeech(targetWord.replace('sh', 's'))}
              className="px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white font-bold rounded-xl shadow-sm"
            >
              نطق فيه خطأ في الصوت ⚠️
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
