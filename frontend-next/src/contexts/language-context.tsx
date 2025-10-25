'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

export type Language = 'en' | 'zh' | 'fr' | 'es' | 'ja' | 'ko';

interface LanguageContextType {
  language: Language;
  setLanguage: (language: Language) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const languageNames = {
  en: 'English',
  zh: '中文',
  fr: 'Français',
  es: 'Español',
  ja: '日本語',
  ko: '한국어',
};

const languageFlags = {
  en: '🇺🇸',
  zh: '🇨🇳',
  fr: '🇫🇷',
  es: '🇪🇸',
  ja: '🇯🇵',
  ko: '🇰🇷',
};

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>('en');

  // Load language from localStorage on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('preferred-language') as Language | null;
    const allowed = ['en', 'zh', 'fr', 'es', 'ja', 'ko'];
    if (savedLanguage && allowed.includes(savedLanguage) && savedLanguage !== language) {
      setLanguageState(savedLanguage);
    }
  }, []);

  const setLanguage = (newLanguage: Language) => {
    setLanguageState(newLanguage);
    localStorage.setItem('preferred-language', newLanguage);
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

export { languageNames, languageFlags };
