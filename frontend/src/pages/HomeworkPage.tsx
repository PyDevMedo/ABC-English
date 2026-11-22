import React, { useEffect, useState, useRef } from 'react';
import { 
  CheckSquare, Clock, CheckCircle2, AlertCircle, RotateCcw, 
  Sparkles, Camera, Image as ImageIcon, Star, Trophy, ExternalLink,
  ChevronLeft, Award, BookOpen, Upload, PlusCircle, Check, RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import confetti from 'canvas-confetti';

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
  const { user, refreshUser } = useAuth();
  const [submissions, setSubmissions] = useState<HomeworkSubmission[]>([]);
  const [currentLevelAssignment, setCurrentLevelAssignment] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);

  // Quick Photo Upload State for Current Level
  const [quickImage, setQuickImage] = useState<File | null>(null);
  const [quickPreview, setQuickPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Specific Resubmission State for "needs_retry" cards
  const [retryTargetAssignmentId, setRetryTargetAssignmentId] = useState<number | null>(null);
  const [retryImage, setRetryImage] = useState<File | null>(null);
  const [retryPreview, setRetryPreview] = useState<string | null>(null);
  const [retryUploading, setRetryUploading] = useState(false);
  const retryCameraRef = useRef<HTMLInputElement>(null);
  const retryFileRef = useRef<HTMLInputElement>(null);

  const currentLevelId = user?.current_level_id || 1;

  const loadData = () => {
    setLoading(true);
    Promise.all([
      api.getMySubmissions(),
      api.getAssignmentByLevel(currentLevelId)
    ])
      .then(([subs, asg]) => {
        setSubmissions(subs);
        setCurrentLevelAssignment(asg);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [currentLevelId]);

  const handleImageSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setQuickImage(file);
      setQuickPreview(URL.createObjectURL(file));
    }
  };

  const handleUploadPhoto = async () => {
    if (!quickImage || !currentLevelAssignment?.id) return;
    setUploading(true);
    try {
      await api.submitHandwritingPhoto(currentLevelAssignment.id, quickImage);
      confetti({ particleCount: 90, spread: 60, origin: { y: 0.6 } });
      setQuickImage(null);
      setQuickPreview(null);
      refreshUser();
      loadData();
    } catch (err: any) {
      alert(err.message || 'حدث خطأ أثناء رفع صورة الواجب');
    } finally {
      setUploading(false);
    }
  };

  // Handlers for specific Retry submission
  const handleTriggerRetryUpload = (asgId: number, mode: 'camera' | 'file') => {
    setRetryTargetAssignmentId(asgId);
    if (mode === 'camera') {
      retryCameraRef.current?.click();
    } else {
      retryFileRef.current?.click();
    }
  };

  const handleRetryImageSelected = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setRetryImage(file);
      setRetryPreview(URL.createObjectURL(file));
    }
  };

  const handleSendRetrySubmission = async () => {
    if (!retryImage || !retryTargetAssignmentId) return;
    setRetryUploading(true);
    try {
      await api.submitHandwritingPhoto(retryTargetAssignmentId, retryImage);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
      setRetryImage(null);
      setRetryPreview(null);
      setRetryTargetAssignmentId(null);
      refreshUser();
      loadData();
    } catch (err: any) {
      alert(err.message || 'حدث خطأ أثناء إرسال الواجب الجديد');
    } finally {
      setRetryUploading(false);
    }
  };

  const totalCount = submissions.length;
  const pendingCount = submissions.filter(s => s.status === 'submitted').length;
  const gradedCount = submissions.filter(s => s.status === 'graded').length;
  const retryCount = submissions.filter(s => s.status === 'needs_retry').length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Hidden inputs for Retry Upload */}
      <input
        type="file"
        accept="image/*"
        capture="environment"
        ref={retryCameraRef}
        onChange={handleRetryImageSelected}
        className="hidden"
      />
      <input
        type="file"
        accept="image/*"
        ref={retryFileRef}
        onChange={handleRetryImageSelected}
        className="hidden"
      />

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
          هنا تتابع وتسلّم دفاتر الخط التي صورتها ورفعتها، ورؤية تقييمات ودرجات المعلم وإعادة الإرسال فوراً عند طلب المعلم.
        </p>
      </div>

      {/* Quick Upload Box for Current Level */}
      <div className="kid-card p-6 border-2 border-amber-300 bg-gradient-to-r from-amber-50/60 via-orange-50/30 to-amber-50/60 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-amber-200">
          <div className="flex items-center gap-3">
            <span className="w-12 h-12 rounded-2xl bg-amber-500 text-white font-black text-base flex items-center justify-center font-fredoka shadow-md shadow-amber-200">
              L{currentLevelId}
            </span>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base md:text-lg font-black text-slate-900">
                  {currentLevelAssignment?.title || `واجب المستوى ${currentLevelId}`}
                </h3>
                <span className="px-2.5 py-0.5 rounded-full bg-amber-200 text-amber-900 text-[10px] font-black">
                  المستوى الحالي
                </span>
              </div>
              <p className="text-xs font-bold text-slate-600 mt-0.5">
                {currentLevelAssignment?.instructions_ar || 'اكتب الكلمات في كراسة الأسطر الأربعة وصورها لفتح المستوى التالي 📸'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 self-end md:self-center">
            {currentLevelAssignment?.is_submitted ? (
              <span className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-emerald-100 text-emerald-900 text-xs font-black">
                <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                تم تسليم واجب هذا المستوى ✅
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-rose-100 text-rose-900 text-xs font-black animate-pulse">
                <AlertCircle className="w-4 h-4 text-rose-600" />
                بانتظار صورة الدفتر
              </span>
            )}
          </div>
        </div>

        {/* Hidden File Inputs */}
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

        {/* Action / Preview Area */}
        <div className="pt-4">
          {quickPreview ? (
            <div className="flex flex-col sm:flex-row items-center gap-4 bg-white p-4 rounded-2xl border border-amber-200">
              <div className="relative w-32 h-32 rounded-xl overflow-hidden border-2 border-amber-400 shrink-0">
                <img src={quickPreview} alt="Preview" className="w-full h-full object-cover" />
              </div>
              <div className="flex-1 space-y-2 text-center sm:text-right">
                <h4 className="text-sm font-black text-slate-800">جاهز للتسليم!</h4>
                <p className="text-xs font-bold text-slate-500">اضغط على زر التسليم أدناه لإرسال الصورة للمعلم عبر Telegram فوراً.</p>
                <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
                  <button
                    type="button"
                    onClick={handleUploadPhoto}
                    disabled={uploading}
                    className="px-6 py-2.5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:opacity-95 text-white font-black text-xs rounded-xl shadow-md active:scale-95 transition-all flex items-center gap-1.5 cursor-pointer"
                  >
                    <Check className="w-4 h-4" />
                    <span>{uploading ? 'جاري الإرسال...' : 'إرسال الصورة للمعلم الآن 🚀'}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setQuickImage(null);
                      setQuickPreview(null);
                    }}
                    className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-all"
                  >
                    إلغاء
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white/80 p-4 rounded-2xl border border-amber-200/80">
              <div className="text-xs font-bold text-slate-600">
                📸 يمكنك تصوير كراستك مباشرة من الكاميرا أو رفع صورة من المعرض:
              </div>
              <div className="flex gap-2 w-full sm:w-auto">
                <button
                  type="button"
                  onClick={() => cameraInputRef.current?.click()}
                  className="flex-1 sm:flex-none px-4 py-2.5 bg-gradient-to-r from-rose-500 to-pink-600 hover:opacity-95 text-white font-black text-xs rounded-xl shadow-sm flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer"
                >
                  <Camera className="w-4 h-4" />
                  <span>تصوير بالكاميرا</span>
                </button>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="flex-1 sm:flex-none px-4 py-2.5 bg-white hover:bg-slate-50 text-slate-800 font-black text-xs rounded-xl border border-slate-300 shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer"
                >
                  <Upload className="w-4 h-4 text-slate-500" />
                  <span>اختيار من المعرض</span>
                </button>
              </div>
            </div>
          )}
        </div>
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
          <h3 className="text-xl font-black text-slate-800">لا توجد ركوستات واجبات سابقة بعد!</h3>
          <p className="text-xs md:text-sm text-slate-500 font-bold leading-relaxed">
            التقط صورة لدفترك الآن عبر الصندوق بالأعلى، وسيتم إرسالها فوراً للمعلم عبر Telegram لتصحيحها ورصد درجتك.
          </p>
        </div>
      ) : (
        /* Submissions Feed */
        <div className="space-y-4">
          {submissions.map((sub) => {
            const isGraded = sub.status === 'graded';
            const isRetry = sub.status === 'needs_retry';
            const isPending = sub.status === 'submitted';
            const isThisTargetRetry = retryTargetAssignmentId === sub.assignment_id;

            return (
              <div 
                key={sub.id}
                className={`kid-card p-6 border-2 transition-all ${
                  isGraded 
                    ? 'border-emerald-200 bg-emerald-50/20' 
                    : isRetry 
                    ? 'border-rose-400 bg-rose-50/30 ring-2 ring-rose-200' 
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
                      <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-rose-500 text-white text-xs font-black shadow-sm shadow-rose-200 animate-bounce">
                        <AlertCircle className="w-4 h-4" />
                        مطلوب إعادة كتابة الواجب وتصويره ✍️
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

                    {/* Retry Message Box with Direct Action Button */}
                    {isRetry && (
                      <div className="p-5 bg-rose-50 rounded-3xl border-2 border-rose-300 space-y-3 shadow-xs">
                        <div className="flex items-start gap-2.5">
                          <span className="text-xl">⚠️</span>
                          <div className="space-y-1">
                            <span className="text-xs font-black text-rose-950 block">
                              ملاحظة المعلم عبر البوت:
                            </span>
                            <p className="text-xs font-bold text-rose-900 italic">
                              "{sub.comments || 'يرجى إعادة كتابة الصفحة بخط أوضح وتصويرها مجدداً.'}"
                            </p>
                          </div>
                        </div>

                        {/* Interactive Resubmission Area inside the Retry Card */}
                        <div className="pt-2 border-t border-rose-200">
                          {isThisTargetRetry && retryPreview ? (
                            <div className="flex flex-col sm:flex-row items-center gap-3 bg-white p-3 rounded-2xl border border-rose-300">
                              <img src={retryPreview} alt="Retry Preview" className="w-20 h-20 object-cover rounded-xl border border-rose-300" />
                              <div className="flex-1 space-y-1 text-center sm:text-right">
                                <span className="text-xs font-black text-slate-800 block">الصورة الجديدة جاهزة!</span>
                                <div className="flex gap-2 justify-center sm:justify-start">
                                  <button
                                    type="button"
                                    onClick={handleSendRetrySubmission}
                                    disabled={retryUploading}
                                    className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-black text-xs rounded-xl shadow-md flex items-center gap-1 cursor-pointer"
                                  >
                                    <Check className="w-3.5 h-3.5" />
                                    <span>{retryUploading ? 'جاري الإرسال...' : 'إرسال الواجب الجديد للمعلم 🚀'}</span>
                                  </button>
                                  <button
                                    type="button"
                                    onClick={() => {
                                      setRetryImage(null);
                                      setRetryPreview(null);
                                      setRetryTargetAssignmentId(null);
                                    }}
                                    className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl"
                                  >
                                    إلغاء
                                  </button>
                                </div>
                              </div>
                            </div>
                          ) : (
                            <div className="flex flex-col sm:flex-row items-center justify-between gap-2.5">
                              <span className="text-xs font-black text-rose-900">
                                أعدت كتابة الواجب في كراستك؟ أرسل النسخة الجديدة الآن:
                              </span>
                              <div className="flex gap-2 w-full sm:w-auto">
                                <button
                                  type="button"
                                  onClick={() => handleTriggerRetryUpload(sub.assignment_id, 'camera')}
                                  className="flex-1 sm:flex-none px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-black text-xs rounded-xl shadow-md flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer"
                                >
                                  <Camera className="w-3.5 h-3.5" />
                                  <span>تصوير بالكاميرا 📷</span>
                                </button>
                                <button
                                  type="button"
                                  onClick={() => handleTriggerRetryUpload(sub.assignment_id, 'file')}
                                  className="flex-1 sm:flex-none px-4 py-2 bg-white hover:bg-rose-50 text-rose-800 font-black text-xs rounded-xl border border-rose-300 shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer"
                                >
                                  <Upload className="w-3.5 h-3.5 text-rose-600" />
                                  <span>اختيار من المعرض 🖼️</span>
                                </button>
                              </div>
                            </div>
                          )}
                        </div>
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
            onClick={e => e.stopPropagation()} 
            className="bg-white rounded-3xl p-4 max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col space-y-3 shadow-2xl"
          >
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <span className="font-black text-sm text-slate-800">معاينة صورة كراسة الواجب 📸</span>
              <button
                type="button"
                onClick={() => setSelectedPhoto(null)}
                className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center font-black"
              >
                ✕
              </button>
            </div>
            <div className="flex-1 overflow-auto rounded-2xl bg-slate-950 flex items-center justify-center">
              <img 
                src={selectedPhoto} 
                alt="كراسة الطالب" 
                className="max-w-full max-h-[75vh] object-contain rounded-xl"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
