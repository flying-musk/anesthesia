'use client';

import { useLanguage, languageNames } from '@/contexts/language-context';
import { LanguageSwitcher } from '@/components/language-switcher';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function TestLanguagePage() {
  const { language } = useLanguage();

  const translations = {
    en: {
      title: 'Language Test Page',
      description: 'This page demonstrates the language switching functionality.',
      currentLanguage: 'Current Language',
      features: 'Features',
      feature1: 'Language switching with dropdown',
      feature2: 'Persistent language selection',
      feature3: 'API calls with language parameter',
    },
    zh: {
      title: '語言測試頁面',
      description: '此頁面演示語言切換功能。',
      currentLanguage: '當前語言',
      features: '功能',
      feature1: '下拉式語言切換',
      feature2: '持久化語言選擇',
      feature3: '帶語言參數的 API 調用',
    },
    fr: {
      title: 'Page de Test de Langue',
      description: 'Cette page démontre la fonctionnalité de changement de langue.',
      currentLanguage: 'Langue Actuelle',
      features: 'Fonctionnalités',
      feature1: 'Changement de langue avec menu déroulant',
      feature2: 'Sélection de langue persistante',
      feature3: 'Appels API avec paramètre de langue',
    },
    es: {
      title: 'Página de Prueba de Idioma',
      description: 'Esta página demuestra la funcionalidad de cambio de idioma.',
      currentLanguage: 'Idioma Actual',
      features: 'Características',
      feature1: 'Cambio de idioma con menú desplegable',
      feature2: 'Selección de idioma persistente',
      feature3: 'Llamadas API con parámetro de idioma',
    },
    ja: {
      title: '言語テストページ',
      description: 'このページは言語切り替え機能を示します。',
      currentLanguage: '現在の言語',
      features: '機能',
      feature1: 'ドロップダウンによる言語切替',
      feature2: '言語選択の永続化',
      feature3: '言語パラメータ付きのAPI呼び出し',
    },
    ko: {
      title: '언어 테스트 페이지',
      description: '이 페이지는 언어 전환 기능을 보여줍니다.',
      currentLanguage: '현재 언어',
      features: '기능',
      feature1: '드롭다운으로 언어 전환',
      feature2: '언어 선택 영구 저장',
      feature3: '언어 매개변수를 가진 API 호출',
    },
  };

  const t = translations[language];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t.title}</h1>
        <LanguageSwitcher />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{t.currentLanguage}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-medium">
            {language.toUpperCase()} - {language === 'en' ? 'English' : language === 'zh' ? '中文' : 'Français'}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{t.features}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p>{t.description}</p>
          <ul className="list-disc list-inside space-y-2">
            <li>{t.feature1}</li>
            <li>{t.feature2}</li>
            <li>{t.feature3}</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
