import React, { useState } from 'react';
import { Sparkles, Phone, Lock, User, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AuthPage: React.FC = () => {
  const { login, register } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [avatar, setAvatar] = useState('lion');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const avatars = [
    { id: 'lion', emoji: '🦁', name: 'الأسد الشجاع' },
    { id: 'panda', emoji: '🐼', name: 'الباندا الذكي' },
    { id: 'bunny', emoji: '🐰', name: 'الأرنب السريع' },
    { id: 'fox', emoji: '🦊', name: 'الثعلب المبتكر' },
    { id: 'monkey', emoji: '🐵', name: 'القرد المرح' }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isRegister) {
        if (fullName.trim().split(/\s+/).length < 3) {
          throw new Error('يرجى إدخال الاسم الثلاثي كاملاً للطفل (مثال: محمد أحمد علي)');
        }
        await register({
          full_name: fullName.trim(),
          phone_number: phoneNumber.trim(),
          password,
          avatar
        });
      } else {
        await login({
          phone_number: phoneNumber.trim(),
          password
        });
      }
    } catch (err: any) {
      setError(err.message || 'حدث خطأ، يرجى المحاولة مرة أخرى');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-100 via-sky-100 to-rose-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl border-4 border-amber-300 p-8 relative overflow-hidden">
        {/* Playful Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-amber-400 to-rose-400 flex items-center justify-center text-white mx-auto mb-3 shadow-lg shadow-amber-200">
            <Sparkles className="w-10 h-10 animate-spin" />
          </div>
          <h2 className="text-3xl font-black font-fredoka text-slate-800 tracking-wide">
            My English Journey
          </h2>
          <p className="text-sm font-bold text-amber-800 mt-1">
            {isRegister ? 'تسجيل حساب طالب جديد بالمنصة 🌟' : 'أهلاً بك مجدداً يا بطل! سجل دخولك 🎒'}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border-2 border-rose-300 text-rose-700 text-sm font-bold text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">الاسم الثلاثي للطفل (مطلوب):</label>
              <div className="relative">
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="مثال: يوسف محمود إبراهيم"
                  className="w-full px-4 py-3 pr-10 rounded-2xl border-2 border-slate-200 focus:border-amber-400 focus:outline-none font-bold text-slate-800 transition-colors"
                />
                <User className="w-5 h-5 text-slate-400 absolute right-3 top-3.5" />
              </div>
              <p className="text-[11px] text-slate-500 mt-1">يجب أن يحتوي الاسم على 3 أجزاء على الأقل.</p>
            </div>
          )}

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">رقم الهاتف المحمول (للطالب أو ولي الأمر):</label>
            <div className="relative">
              <input
                type="tel"
                required
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="01012345678"
                dir="ltr"
                className="w-full px-4 py-3 pl-10 rounded-2xl border-2 border-slate-200 focus:border-amber-400 focus:outline-none font-bold text-slate-800 transition-colors text-right"
              />
              <Phone className="w-5 h-5 text-slate-400 absolute left-3 top-3.5" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">كلمة المرور:</label>
            <div className="relative">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 pr-10 rounded-2xl border-2 border-slate-200 focus:border-amber-400 focus:outline-none font-bold text-slate-800 transition-colors"
              />
              <Lock className="w-5 h-5 text-slate-400 absolute right-3 top-3.5" />
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-2">اختر شخصيتك التعليمية المفضلة:</label>
              <div className="flex justify-between gap-1">
                {avatars.map((a) => (
                  <button
                    key={a.id}
                    type="button"
                    onClick={() => setAvatar(a.id)}
                    className={`flex-1 p-2 rounded-2xl border-2 text-center transition-all ${
                      avatar === a.id
                        ? 'border-amber-500 bg-amber-50 scale-105 shadow-md shadow-amber-200'
                        : 'border-slate-200 bg-slate-50 opacity-70'
                    }`}
                  >
                    <span className="text-2xl block">{a.emoji}</span>
                    <span className="text-[10px] font-bold text-slate-600 truncate block mt-0.5">{a.name}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 mt-6 bg-gradient-to-r from-amber-400 to-rose-400 hover:from-amber-500 hover:to-rose-500 text-white font-black text-lg rounded-2xl shadow-lg shadow-amber-300 transform active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <span>جاري التحميل...</span>
            ) : (
              <>
                <span>{isRegister ? 'انطلق في رحلة التعلم 🚀' : 'دخول المنصة 🎒'}</span>
                <ArrowRight className="w-5 h-5 rotate-180" />
              </>
            )}
          </button>
        </form>

        <div className="mt-6 text-center border-t border-slate-100 pt-4">
          <button
            type="button"
            onClick={() => {
              setIsRegister(!isRegister);
              setError(null);
            }}
            className="text-sm font-bold text-amber-700 hover:text-amber-800 transition-colors"
          >
            {isRegister
              ? 'لديك حساب بالفعل؟ اضغط هنا لتسجيل الدخول'
              : 'ليس لديك حساب؟ أنشئ حساب طفلك الآن مجاناً!'}
          </button>
        </div>
      </div>
    </div>
  );
};
