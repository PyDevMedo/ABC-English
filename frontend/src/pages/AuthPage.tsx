import React, { useState } from 'react';
import { Sparkles, Phone, Lock, User, ArrowRight, ShieldCheck, GraduationCap, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const AuthPage: React.FC = () => {
  const { login, register } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isRegister) {
        if (fullName.trim().split(/\s+/).length < 3) {
          throw new Error('يرجى إدخال الاسم الثلاثي كاملاً للطالب (مثال: أحمد أشرف الشوادفي)');
        }
        if (password.length < 6) {
          throw new Error('يجب ألا تقل كلمة المرور عن 6 أحرف أو أرقام');
        }
        if (password !== confirmPassword) {
          throw new Error('كلمتا المرور غير متطابقتين، يرجى كتابة نفس كلمة المرور في خانة التأكيد');
        }
        await register({
          full_name: fullName.trim(),
          phone_number: phoneNumber.trim(),
          password,
          avatar: 'student'
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
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-sky-50 to-indigo-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white/95 backdrop-blur-xl rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.06)] border border-slate-100 p-8 relative overflow-hidden">
        {/* Decorative Top Glow */}
        <div className="absolute -top-16 -right-16 w-36 h-36 bg-amber-300/30 rounded-full blur-2xl"></div>
        <div className="absolute -bottom-16 -left-16 w-36 h-36 bg-indigo-300/30 rounded-full blur-2xl"></div>

        {/* Brand Header */}
        <div className="text-center mb-6 relative z-10">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-amber-400 via-rose-500 to-indigo-600 flex items-center justify-center text-white mx-auto mb-3 shadow-xl shadow-rose-200">
            <span className="font-black font-fredoka text-3xl tracking-tighter drop-shadow-md">ABC</span>
          </div>
          <h2 className="text-3xl font-black font-fredoka text-slate-900 tracking-tight">
            ABC English
          </h2>
          <p className="text-xs font-bold text-slate-500 mt-1">
            {isRegister ? 'تسجيل حساب جديد في منصة ABC التعليمية 🌟' : 'أهلاً بك مجدداً في منصة ABC! سجل دخولك 🎒'}
          </p>
        </div>

        {/* Auth Mode Tabs Switcher */}
        <div className="grid grid-cols-2 p-1.5 bg-slate-100/90 rounded-2xl mb-6 relative z-10 border border-slate-200">
          <button
            type="button"
            onClick={() => {
              setIsRegister(false);
              setError(null);
            }}
            className={`py-3 rounded-xl font-black text-xs md:text-sm flex items-center justify-center gap-1.5 transition-all ${
              !isRegister
                ? 'bg-white text-slate-900 shadow-md shadow-slate-200 scale-102 font-bold'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <span>تسجيل الدخول</span>
          </button>
          <button
            type="button"
            onClick={() => {
              setIsRegister(true);
              setError(null);
              setConfirmPassword('');
            }}
            className={`py-3 rounded-xl font-black text-xs md:text-sm flex items-center justify-center gap-1.5 transition-all ${
              isRegister
                ? 'bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md shadow-orange-200 scale-102 font-bold'
                : 'text-slate-500 hover:text-slate-800'
            }`}
          >
            <span>إنشاء حساب جديد</span>
          </button>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-black text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 relative z-10">
          {isRegister && (
            <div>
              <label className="block text-xs font-black text-slate-700 mb-1">الاسم الثلاثي للطالب:</label>
              <div className="relative">
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="مثال: أحمد أشرف الشوادفي"
                  className="w-full px-4 py-3.5 pr-10 rounded-2xl border border-slate-200 bg-slate-50/50 focus:bg-white focus:border-amber-400 focus:outline-none font-bold text-slate-800 text-sm transition-all"
                />
                <User className="w-5 h-5 text-slate-400 absolute right-3.5 top-3.5" />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-black text-slate-700 mb-1">رقم الهاتف المحمول:</label>
            <div className="relative">
              <input
                type="tel"
                required
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                placeholder="01012345678"
                dir="ltr"
                className="w-full px-4 py-3.5 pl-10 rounded-2xl border border-slate-200 bg-slate-50/50 focus:bg-white focus:border-amber-400 focus:outline-none font-bold text-slate-800 text-sm transition-all text-right"
              />
              <Phone className="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-black text-slate-700 mb-1">كلمة المرور:</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3.5 pr-10 pl-11 rounded-2xl border border-slate-200 bg-slate-50/50 focus:bg-white focus:border-amber-400 focus:outline-none font-bold text-slate-800 text-sm transition-all"
              />
              <Lock className="w-5 h-5 text-slate-400 absolute right-3.5 top-3.5 pointer-events-none" />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-3 top-3 p-1 text-slate-400 hover:text-slate-600 focus:outline-none transition-colors"
                title={showPassword ? "إخفاء كلمة المرور" : "عرض كلمة المرور"}
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="block text-xs font-black text-slate-700 mb-1">تأكيد كلمة المرور:</label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full px-4 py-3.5 pr-10 pl-11 rounded-2xl border border-slate-200 bg-slate-50/50 focus:bg-white focus:border-amber-400 focus:outline-none font-bold text-slate-800 text-sm transition-all"
                />
                <Lock className="w-5 h-5 text-slate-400 absolute right-3.5 top-3.5 pointer-events-none" />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute left-3 top-3 p-1 text-slate-400 hover:text-slate-600 focus:outline-none transition-colors"
                  title={showConfirmPassword ? "إخفاء كلمة المرور" : "عرض كلمة المرور"}
                >
                  {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 mt-6 bg-gradient-to-r from-amber-400 via-orange-500 to-rose-500 hover:opacity-95 text-white font-black text-base rounded-2xl shadow-lg shadow-orange-200 transform active:scale-95 transition-all flex items-center justify-center gap-2"
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
              setConfirmPassword('');
            }}
            className="text-xs font-black text-slate-600 hover:text-amber-600 transition-colors"
          >
            {isRegister
              ? 'لديك حساب بالفعل؟ اضغط هنا لتسجيل الدخول'
              : 'ليس لديك حساب؟ أنشئ حساباً جديداً للبدء مجاناً!'}
          </button>
        </div>
      </div>
    </div>
  );
};
