'use client';

import { useLanguage, languageNames, languageFlags } from '@/contexts/language-context';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Globe } from 'lucide-react';

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Globe className="h-4 w-4" />
          <span className="hidden sm:inline">
            {languageFlags[language]} {languageNames[language]}
          </span>
          <span className="sm:hidden">
            {languageFlags[language]}
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {Object.keys(languageNames).map((lang) => {
          // @ts-expect-error languageNames is a typed object, access by dynamic key
          const name = languageNames[lang];
          // @ts-expect-error languageFlags is a typed object, access by dynamic key
          const flag = languageFlags[lang];

          return (
            <DropdownMenuItem
              key={lang}
              onClick={() => setLanguage(lang as 'en' | 'zh' | 'fr' | 'es' | 'ja' | 'ko')}
              className={language === lang ? 'bg-accent' : ''}
            >
              <span className="mr-2">{flag}</span>
              {name}
            </DropdownMenuItem>
          );
        })}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
