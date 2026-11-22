import React, { useState } from 'react';
import { Send, CheckCircle2, Copy, X, ShieldAlert, Sparkles } from 'lucide-react';
import { api } from '../services/api';

interface TelegramModalProps {
  isOpen: boolean;
  onClose: () => void;
  studentName: string;
}

export const TelegramModal: React.FC<TelegramModalProps> = ({ isOpen, onClose, studentName }) => {
  const [code, setCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const fetchCode = async () => {
    setLoading(true);
    try {
      const data = await api.generateTelegramLink();
      setCode(data.code);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    if (isOpen && !code) {
      fetchCode();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const copyToClipboard = () => {
    if (code) {
      navigator.clipboard.writeText(`/link ${code}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border-4 border-sky-300 relative animate-in fade-in zoom-in-95 duration-200">
        <button
          onClick={onClose}
          className="absolute top-4 left-4 p-2 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-100"
        >
          <X className="w-6 h-6" />
        </button>

        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-sky-100 text-sky-500 rounded-3xl mx-auto flex items-center justify-center mb-3 shadow-inner">
            <Send className="w-8 h-8" />
          </div>
          <h3 className="text-2xl font-black text-slate-800">ربط الحساب مع Telegram</h3>
          <p className="text-sm text-slate-500 mt-1">
            لمتابعة تقدم <b>{studentName}</b> وتلقي تقارير الذكاء الاصطناعي الأسبوعية
          </p>
        </div>

        {loading ? (
          <div className="py-8 text-center text-slate-500 font-bold">جاري استخراج رمز الربط الآمن...</div>
        ) : (
          <div>
            <div className="bg-sky-50 rounded-2xl p-4 border border-sky-200 text-center mb-5">
              <span className="text-xs font-bold text-sky-700 block mb-1">رمز الربط المؤقت (صالح لمدة 15 دقيقة):</span>
              <div className="text-4xl font-black tracking-widest text-sky-900 font-mono my-2 select-all">
                {code || '------'}
              </div>
              <button
                onClick={copyToClipboard}
                className="inline-flex items-center gap-1 text-xs font-bold text-sky-700 hover:text-sky-900 bg-sky-200/60 px-3 py-1.5 rounded-xl transition-all"
              >
                {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
                {copied ? 'تم نسخ الأمر بالرمز!' : 'نسخ أمر الربط'}
              </button>
            </div>

            <div className="space-y-3 text-sm text-slate-600 mb-6 bg-slate-50 p-4 rounded-2xl border border-slate-200">
              <div className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-sky-500 text-white text-xs flex items-center justify-center shrink-0 mt-0.5 font-bold">1</span>
                <span>افتح بوت المنصة على Telegram.</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-sky-500 text-white text-xs flex items-center justify-center shrink-0 mt-0.5 font-bold">2</span>
                <span>أرسل الأمر التالي في المحادثة:</span>
              </div>
              <div className="bg-white p-2 rounded-xl text-center font-mono text-sky-800 font-bold border border-slate-200">
                /link {code}
              </div>
              <div className="flex items-start gap-2">
                <span className="w-5 h-5 rounded-full bg-sky-500 text-white text-xs flex items-center justify-center shrink-0 mt-0.5 font-bold">3</span>
                <span>سيتم ربط حسابك فوراً وبدء استقبال إشعارات الدروس والواجبات!</span>
              </div>
            </div>

            <button
              onClick={onClose}
              className="w-full py-3 bg-sky-500 hover:bg-sky-600 text-white font-bold rounded-2xl shadow-lg shadow-sky-200 transition-all text-base"
            >
              تم، سأقوم بربط الحساب الآن ✨
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
