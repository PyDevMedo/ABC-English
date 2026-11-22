import React, { useState } from 'react';
import { 
  Sparkles, Star, Flame, Trophy, Send, LogOut, BookOpen, 
  Layers, CheckSquare, Award, Mic, Home, User
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { TelegramModal } from './TelegramModal';

interface NavbarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, setCurrentTab }) => {
  const { user, logout } = useAuth();
  const [showTelegramModal, setShowTelegramModal] = useState(false);

  if (!user) return null;

  const navItems = [
    { id: 'home', label: 'الرئيسية', icon: Home, color: 'text-amber-500' },
    { id: 'levels', label: 'المستويات والدروس', icon: Layers, color: 'text-sky-500' },
    { id: 'adaptive', label: 'المسار الذكي AI', icon: Sparkles, color: 'text-purple-500' },
    { id: 'homework', label: 'الواجبات', icon: CheckSquare, color: 'text-emerald-500' },
    { id: 'quizzes', label: 'اختباراتي', icon: Award, color: 'text-rose-500' },
    { id: 'pronunciation', label: 'مدرس النطق', icon: Mic, color: 'text-indigo-500' },
    { id: 'achievements', label: 'إنجازاتي', icon: Trophy, color: 'text-yellow-500' },
  ];

  const getAvatarEmoji = (avatar: string) => {
    switch (avatar) {
      case 'panda': return '🐼';
      case 'bunny': return '🐰';
      case 'fox': return '🦊';
      case 'monkey': return '🐵';
      default: return '🦁';
    }
  };

  return (
    <>
      <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-xl border-b border-slate-100 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)]">
        {/* Top Header Row */}
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          {/* ABC Brand Logo */}
          <div 
            onClick={() => setCurrentTab('home')}
            className="flex items-center gap-3 cursor-pointer group select-none"
          >
            <div className="relative flex items-center justify-center">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-400 via-rose-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-rose-200 group-hover:scale-105 group-hover:rotate-1 transition-all">
                <span className="font-black font-fredoka text-xl tracking-tighter text-white drop-shadow">ABC</span>
              </div>
              <span className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-emerald-400 border-2 border-white rounded-full animate-ping"></span>
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <h1 className="text-2xl md:text-3xl font-black font-fredoka tracking-wide bg-gradient-to-r from-rose-500 via-amber-500 to-indigo-600 bg-clip-text text-transparent">
                  ABC English
                </h1>
                <span className="text-[10px] font-black bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full border border-amber-300">
                  AI KIDS
                </span>
              </div>
              <p className="text-[11px] font-bold text-slate-500 hidden sm:block">
                منصة تعليم الإنجليزية الذكية للأطفال 🌟
              </p>
            </div>
          </div>

          {/* Gamification Stats */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Stars */}
            <div className="flex items-center gap-1.5 bg-gradient-to-r from-amber-50 to-yellow-50 px-3.5 py-1.5 rounded-2xl border border-amber-200 shadow-sm">
              <Star className="w-4 h-4 text-amber-500 fill-amber-400 animate-bounce" />
              <span className="font-black text-amber-900 text-sm md:text-base font-fredoka">{user.stars}</span>
            </div>

            {/* XP */}
            <div className="flex items-center gap-1.5 bg-gradient-to-r from-purple-50 to-indigo-50 px-3.5 py-1.5 rounded-2xl border border-purple-200 shadow-sm">
              <Trophy className="w-4 h-4 text-purple-600" />
              <span className="font-black text-purple-900 text-sm md:text-base font-fredoka">
                {user.xp} <span className="text-[10px] text-purple-600 font-bold">XP</span>
              </span>
            </div>

            {/* Streak */}
            <div className="flex items-center gap-1.5 bg-gradient-to-r from-rose-50 to-orange-50 px-3 py-1.5 rounded-2xl border border-rose-200 shadow-sm hidden md:flex">
              <Flame className="w-4 h-4 text-rose-500 fill-rose-500" />
              <span className="font-black text-rose-900 text-xs font-fredoka">{user.streak_days} Days</span>
            </div>

            {/* Telegram Link Pill */}
            <button
              onClick={() => setShowTelegramModal(true)}
              className="flex items-center gap-1.5 bg-gradient-to-r from-sky-400 to-blue-500 hover:from-sky-500 hover:to-blue-600 text-white px-3.5 py-2 rounded-2xl shadow-md shadow-sky-200 text-xs md:text-sm font-black transition-all active:scale-95"
              title="ربط حساب Telegram لولي الأمر"
            >
              <Send className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">ربط Telegram</span>
            </button>

            {/* User Profile Pill */}
            <div className="flex items-center gap-2 bg-slate-50 p-1.5 pr-3 rounded-2xl border border-slate-200/80">
              <span className="text-xl" title={user.avatar}>{getAvatarEmoji(user.avatar)}</span>
              <div className="text-right hidden lg:block leading-tight">
                <span className="text-xs font-black text-slate-800 block truncate max-w-[100px]">{user.full_name}</span>
                <span className="text-[10px] text-purple-700 font-black">Level {user.current_level_id}</span>
              </div>
              <button 
                onClick={logout} 
                className="p-1.5 text-slate-400 hover:text-rose-500 hover:bg-white rounded-xl transition-all"
                title="تسجيل الخروج"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs Bar */}
        <div className="border-t border-slate-100 bg-slate-50/60 overflow-x-auto scrollbar-none">
          <div className="max-w-7xl mx-auto px-4 flex items-center gap-1.5 md:gap-2 py-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-xs md:text-sm whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-amber-400 to-orange-400 text-white shadow-md shadow-orange-200 scale-102'
                      : 'text-slate-600 hover:bg-white hover:text-slate-900'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : item.color}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </header>

      <TelegramModal
        isOpen={showTelegramModal}
        onClose={() => setShowTelegramModal(false)}
        studentName={user.full_name}
      />
    </>
  );
};
