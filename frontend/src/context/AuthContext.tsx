import React, { createContext, useContext, useState, useEffect } from 'react';
import { api, getAuthToken, removeAuthToken } from '../services/api';

export interface UserProfile {
  id: number;
  student_id: string;
  full_name: string;
  phone_number: string;
  role: string;
  is_active: boolean;
  avatar: string;
  xp: number;
  stars: number;
  streak_days: number;
  current_level_id: number;
}

interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  login: (data: { phone_number: string; password: string }) => Promise<void>;
  register: (data: { full_name: string; phone_number: string; password: string; avatar?: string }) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      if (getAuthToken()) {
        const data = await api.getMe();
        setUser(data);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
      removeAuthToken();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (credentials: { phone_number: string; password: string }) => {
    await api.login(credentials);
    await refreshUser();
  };

  const register = async (regData: { full_name: string; phone_number: string; password: string; avatar?: string }) => {
    await api.register(regData);
    await api.login({ phone_number: regData.phone_number, password: regData.password });
    await refreshUser();
  };

  const logout = () => {
    removeAuthToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
