'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Globe } from 'lucide-react';
import { languages, getTranslation } from '@/lib/languages';

type Language = 'en' | 'zh';

export function LanguageSwitcher() {
  const [currentLang, setCurrentLang] = useState<Language>('en');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // 从localStorage获取保存的语言设置
    const savedLang = localStorage.getItem('language') as Language;
    if (savedLang && (savedLang === 'en' || savedLang === 'zh')) {
      setCurrentLang(savedLang);
    }
  }, []);

  const handleLanguageChange = (lang: Language) => {
    setCurrentLang(lang);
    localStorage.setItem('language', lang);
    // 触发自定义事件来通知其他组件语言已更改
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
  };

  if (!mounted) {
    return (
      <Button variant="outline" size="sm" className="flex items-center gap-2">
        <Globe className="h-4 w-4" />
        <span>🇺🇸 EN</span>
      </Button>
    );
  }

  const currentLanguage = languages[currentLang];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="flex items-center gap-2"
          aria-label="Switch Language"
        >
          <Globe className="h-4 w-4" />
          <span>{currentLanguage.flag} {currentLanguage.name}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-40">
        {Object.entries(languages).map(([code, lang]) => (
          <DropdownMenuItem
            key={code}
            onClick={() => handleLanguageChange(code as Language)}
            className="flex items-center gap-2 cursor-pointer"
          >
            <span>{lang.flag}</span>
            <span>{lang.name}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
