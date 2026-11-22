import React, { useEffect, useState } from 'react';
import { 
  CheckSquare, Clock, CheckCircle2, AlertCircle, RotateCcw, 
  Sparkles, Camera, Image as ImageIcon, Star, Trophy, ExternalLink,
  ChevronLeft, Award, BookOpen
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

interface HomeworkSubmission {
  id: number;
  assignment_id: number;
  level_number: number;
  title: string;
  instructions_ar: string;
  submission_type: string;
  image_url?: string;
  audio_url?: string;
  status: 'submitted' | 'graded' | 'needs_retry';
  submitted_at: string;
  score?: number;
  comments?: string;
  retry_requested?: boolean;
  reviewed_at?: string;
}

export const HomeworkPage: React.FC = () => {
  const { user } = useAuth();
  const [submissions, setSubmissions] = useState<HomeworkSubmission[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);

  const loadSubmissions = () => {
    setLoading(true);
    api.getMySubmissions()
      .then(setSubmissions)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadSubmissions();
  }, []);

  const totalCount = submissions.length;
  const pendingCount = submissions.filter(s => s.status === 'submitted').length;
  const gradedCount = submissions.filter(s => s.status === 'graded').length;
  const retryCount = submissions.filter(s => s.status === 'needs_retry').length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header Section */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-emerald-100 text-emerald-900 text-xs font-black shadow-sm">
          <Camera className="w-4 h-4 text-emerald-700" />
          ركوستات وتسليمات الواجبات الورقية
        </span>
        <h2 className="text-2xl md:text-3xl font-black text-slate-800 font-fredoka">
          سجل طلبات الواجب وتصحيح المعلم 📝
        </h2>
        <p className="text-xs md:text-sm font-bold text-slate-500">
          هنا تتابع حالة دفاتر الخط التي صورتها ورفعتها بعد نهاية الحصص، ورؤية تقييمات ودرجات المعلم أولاً بأول.
        </p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Total Submissions */}
        <div className="kid-card p-4 text-center border-slate-200">
          <span className="text-xs font-black text-slate-500 block mb-1">إجمالي الركوستات</span>
          <span className="text-2xl md:text-3xl font-black font-fredoka text-slate-800">{totalCount}</span>
        </div>

        {/* Pending Review */}
        <div className="kid-card p-4 text-center border-amber-200 bg-amber-50/40">
          <span className="text-xs font-black text-amber-700 block mb-1">بانتظار المراجعة</span>
          <span className="text-2xl md:text-3xl font-black font-fredoka text-amber-600">{pendingCount}</span>
        </div>

        {/* Graded & Approved */}
        <div className="kid-card p-4 text-center border-emerald-200 bg-emerald-50/40">
          <span className="text-xs font-black text-emerald-700 block mb-1">واجبات معتمدة</span>
          <span className="text-2xl md:text-3xl font-black font-fredoka text-emerald-600">{gradedCount}</span>
        </div>

        {/* Needs Retry */}
        <div className="kid-card p-4 text-center border-rose-200 bg-rose-50/40">
          <span className="text-xs font-black text-rose-700 block mb-1">تحتاج إعادة خط</span>
          <span className="text-2xl md:text-3xl font-black font-fredoka text-rose-600">{retryCount}</span>
        </div>
      </div>

      {/* Main Content */}
      {loading ? (
        <div className="text-center py-16 font-bold text-slate-400">جاري تحميل سجل الواجبات... 🎒</div>
      ) : submissions.length === 0 ? (
        /* Empty State */
        <div className="bg-white rounded-3xl p-10 md:p-14 text-center border-4 border-dashed border-slate-200 shadow-sm space-y-4 max-w-lg mx-auto">
          <div className="w-20 h-20 bg-amber-100 text-amber-600 rounded-3xl mx-auto flex items-center justify-center text-4xl shadow-inner">
            📷
          </div>
          <h3 className="text-xl font-black text-slate-800">لا توجد ركوستات واجبات مرسلة بعد!</h3>
          <p className="text-xs md:text-sm text-slate-500 font-bold leading-relaxed">
            عند انتهائك من درسك في صفحة المستويات، قم بكتابة الكلمات في كراسة الأسطر الأربعة والتقط صورة لدفترك، وسيظهر طلب التسليم هنا فوراً لتصحيحه من قبل المعلم.
          </p>
        </div>
      ) : (
        /* Submissions Feed */
        <div className="space-y-4">
          {submissions.map((sub) => {
            const isGraded = sub.status === 'graded';
            const isRetry = sub.status === 'needs_retry';
            const isPending = sub.status === 'submitted';

            return (
              <div 
                key={sub.id}
                className={`kid-card p-6 border-2 transition-all ${
                  isGraded 
                    ? 'border-emerald-200 bg-emerald-50/20' 
                    : isRetry 
                    ? 'border-rose-300 bg-rose-50/20' 
                    : 'border-amber-200 bg-white'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div className="flex items-center gap-3">
                    <span className="w-10 h-10 rounded-2xl bg-slate-100 text-slate-800 font-black text-sm flex items-center justify-center font-fredoka shrink-0 shadow-sm">
                      L{sub.level_number}
                    </span>
                    <div>
                      <h4 className="text-base font-black text-slate-900">{sub.title}</h4>
                      <p className="text-xs font-bold text-slate-500 mt-0.5">
                        📅 أُرسل في: {sub.submitted_at}
                      </p>
                    </div>
                  </div>

                  {/* Status Badge */}
                  <div className="flex items-center gap-2">
                    {isGraded && (
                      <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-emerald-100 text-emerald-900 text-xs font-black shadow-sm">
                        <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                        تم التصحيح والاعتماد ({sub.score}%)
                      </span>
                    )}
                    {isPending && (
                      <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-amber-100 text-amber-900 text-xs font-black shadow-sm animate-pulse">
                        <Clock className="w-4 h-4 text-amber-700" />
                        قيد المراجعة لدى المعلم ⏳
                      </span>
                    )}
                    {isRetry && (
                      <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-rose-100 text-rose-900 text-xs font-black shadow-sm">
                        <AlertCircle className="w-4 h-4 text-rose-700" />
                        مطلوب إعادة كتابة الواجب
                      </span>
                    )}
                  </div>
                </div>

                {/* Body Details: Instructions & Notebook Photo */}
                <div className="pt-4 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
                  <div className="md:col-span-2 space-y-3">
                    {sub.instructions_ar && (
                      <p className="text-xs font-bold text-slate-600 bg-slate-50 p-3 rounded-2xl border border-slate-200">
                        ✍️ <b>مطلوب الواجب:</b> {sub.instructions_ar}
                      </p>
                    )}

                    {/* Feedback Note from Teacher */}
                    {isGraded && (
                      <div className="p-4 bg-emerald-50 rounded-2xl border border-emerald-200 space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-black text-emerald-900 flex items-center gap-1">
                            <Star className="w-4 h-4 text-amber-500 fill-amber-400" />
                            تقييم المعلم عبر البوت: <b>{sub.score}%</b>
                          </span>
                          <span className="text-[11px] font-bold text-emerald-700">
                            مكافأة: +50 XP و +3 ⭐
                          </span>
                        </div>
                        {sub.comments && (
                          <p className="text-xs font-bold text-emerald-800 italic mt-1">
                            "{sub.comments}"
                          </p>
                        )}
                      </div>
                    )}

                    {isRetry && (
                      <div className="p-4 bg-rose-50 rounded-2xl border border-rose-200 space-y-2">
                        <span className="text-xs font-black text-rose-900 block">
                          ⚠️ ملاحظة المعلم الإداري:
                        </span>
                        <p className="text-xs font-bold text-rose-800 italic">
                          "{sub.comments || 'يرجى إعادة كتابة الصفحة بخط أوضح وتصويرها مجدداً.'}"
                        </p>
                      </div>
                    )}

                    {isPending && (
                      <p className="text-xs font-bold text-slate-500">
                        🔔 وصل ركوست الواجب إلى بوت Telegram الخاص بالإدارة، وسيصلك إشعار فوري هنا عند رصد الدرجة.
                      </p>
                    )}
                  </div>

                  {/* Notebook Image Thumbnail */}
                  <div className="flex flex-col items-center justify-center">
                    {sub.image_url ? (
                      <div 
                        onClick={() => setSelectedPhoto(sub.image_url || null)}
                        className="group relative cursor-pointer rounded-2xl overflow-hidden border-2 border-slate-200 hover:border-amber-400 transition-all shadow-sm w-full max-w-[200px]"
                      >
                        <img 
                          src={sub.image_url} 
                          alt="صورة واجب الكراسة" 
                          className="w-full h-32 object-cover group-hover:scale-105 transition-all"
                        />
                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-all text-white text-xs font-black gap-1">
                          <ImageIcon className="w-4 h-4" />
                          <span>تكبير الصورة</span>
                        </div>
                      </div>
                    ) : (
                      <div className="w-full h-28 bg-slate-100 rounded-2xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-400 text-xs font-bold gap-1">
                        <ImageIcon className="w-6 h-6" />
                        <span>لم يتم إرفاق صورة</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Full Resolution Photo Lightbox Modal */}
      {selectedPhoto && (
        <div 
          onClick={() => setSelectedPhoto(null)}
          className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
        >
          <div 
            onClick={(e) => e.stopPropagation()}
            className="relative max-w-2xl w-full bg-white rounded-3xl p-4 shadow-2xl overflow-hidden space-y-4"
          >
            <div className="flex items-center justify-between px-2">
              <span className="font-black text-sm text-slate-800">معاينة صورة كراسة الواجب 📸</span>
              <button 
                onClick={() => setSelectedPhoto(null)}
                className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-black text-sm flex items-center justify-center transition-all"
              >
                ✕
              </button>
            </div>
            <div className="rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 max-h-[70vh] flex items-center justify-center">
              <img 
                src={selectedPhoto} 
                alt="كراسة الطالب" 
                className="max-h-[70vh] object-contain"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
