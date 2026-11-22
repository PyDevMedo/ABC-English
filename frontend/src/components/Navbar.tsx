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
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b-4 border-amber-200 shadow-sm">
        {/* Top Header Row */}
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          {/* Logo */}
          <div 
            onClick={() => setCurrentTab('home')}
            className="flex items-center gap-2 cursor-pointer group select-none"
          >
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-amber-400 to-rose-400 flex items-center justify-center text-white shadow-md shadow-amber-300 group-hover:scale-105 transition-transform">
              <Sparkles className="w-7 h-7 animate-pulse" />
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-black font-fredoka tracking-wide bg-gradient-to-r from-amber-600 via-rose-500 to-purple-600 bg-clip-text text-transparent">
                My English Journey
              </h1>
              <p className="text-xs font-bold text-slate-500 hidden sm:block">منصة تعليم الإنجليزية للأطفال 🌟</p>
            </div>
          </div>

          {/* Gamification Stats */}
          <div className="flex items-center gap-2 sm:gap-4">
            {/* Stars */}
            <div className="flex items-center gap-1.5 bg-amber-50 px-3 py-1.5 rounded-2xl border-2 border-amber-300 shadow-sm">
              <Star className="w-5 h-5 text-amber-500 fill-amber-400 animate-bounce" />
              <span className="font-black text-amber-900 text-sm md:text-base">{user.stars}</span>
            </div>

            {/* XP */}
            <div className="flex items-center gap-1.5 bg-purple-50 px-3 py-1.5 rounded-2xl border-2 border-purple-300 shadow-sm">
              <Trophy className="w-5 h-5 text-purple-500" />
              <span className="font-black text-purple-900 text-sm md:text-base">{user.xp} <span className="text-xs font-normal text-purple-700">XP</span></span>
            </div>

            {/* Streak */}
            <div className="flex items-center gap-1.5 bg-rose-50 px-3 py-1.5 rounded-2xl border-2 border-rose-300 shadow-sm hidden md:flex">
              <Flame className="w-5 h-5 text-rose-500 fill-rose-500" />
              <span className="font-black text-rose-900 text-sm">{user.streak_days} أيام</span>
            </div>

            {/* Telegram Link Pill */}
            <button
              onClick={() => setShowTelegramModal(true)}
              className="flex items-center gap-1.5 bg-sky-500 hover:bg-sky-600 text-white px-3 py-1.5 rounded-2xl shadow-md shadow-sky-200 text-xs md:text-sm font-bold transition-transform active:scale-95"
              title="ربط حساب Telegram لولي الأمر"
            >
              <Send className="w-4 h-4" />
              <span className="hidden sm:inline">ربط Telegram</span>
            </button>

            {/* User Profile Pill */}
            <div className="flex items-center gap-2 bg-slate-100 p-1.5 pr-3 rounded-2xl border border-slate-200">
              <span className="text-xl" title={user.avatar}>{getAvatarEmoji(user.avatar)}</span>
              <div className="text-right hidden lg:block leading-tight">
                <span className="text-xs font-black text-slate-800 block truncate max-w-[100px]">{user.full_name}</span>
                <span className="text-[10px] text-amber-600 font-bold">Lvl {user.current_level_id}</span>
              </div>
              <button 
                onClick={logout} 
                className="p-1.5 text-slate-400 hover:text-rose-500 transition-colors"
                title="تسجيل الخروج"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs Bar */}
        <div className="border-t border-slate-100 bg-amber-50/50 overflow-x-auto scrollbar-none">
          <div className="max-w-7xl mx-auto px-4 flex items-center gap-1 md:gap-2 py-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentTab(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-2xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-amber-400 text-amber-950 shadow-md shadow-amber-200 scale-105'
                      : 'text-slate-600 hover:bg-white hover:text-slate-900'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-amber-950' : item.color}`} />
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
