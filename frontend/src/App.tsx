import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AuthPage } from './pages/AuthPage';
import { Navbar } from './components/Navbar';
import { HomePage } from './pages/HomePage';
import { LevelsPage } from './pages/LevelsPage';
import { AdaptivePage } from './pages/AdaptivePage';
import { HomeworkPage } from './pages/HomeworkPage';
import { QuizzesPage } from './pages/QuizzesPage';
import { PronunciationPage } from './pages/PronunciationPage';
import { AchievementsPage } from './pages/AchievementsPage';

const AppContent: React.FC = () => {
  const { user, loading } = useAuth();
  const [currentTab, setCurrentTab] = useState<string>('home');

  if (loading) {
    return (
      <div className="min-h-screen bg-amber-50 flex items-center justify-center font-bold text-amber-900 text-lg animate-pulse">
        جاري تحضير رحلتك التعليمية الممتعة... 🎒
      </div>
    );
  }

  if (!user) {
    return <AuthPage />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-amber-50/50">
      <Navbar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      <main className="grow">
        {currentTab === 'home' && <HomePage onNavigate={setCurrentTab} />}
        {currentTab === 'levels' && <LevelsPage />}
        {currentTab === 'adaptive' && <AdaptivePage />}
        {currentTab === 'homework' && <HomeworkPage />}
        {currentTab === 'quizzes' && <QuizzesPage />}
        {currentTab === 'pronunciation' && <PronunciationPage />}
        {currentTab === 'achievements' && <AchievementsPage />}
      </main>

      <footer className="bg-white border-t border-slate-100 py-6 text-center text-xs text-slate-500 font-bold">
        <p>منصة ABC لتعليم الإنجليزية للطلاب © {new Date().getFullYear()} — نظام إدارة متكامل عبر Telegram ومدعوم بالذكاء الاصطناعي</p>
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
