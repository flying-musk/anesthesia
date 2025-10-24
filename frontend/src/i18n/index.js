import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// 導入語言資源
import zhTW from './locales/zh-TW.json';
import enUS from './locales/en-US.json';
import frFR from './locales/fr-FR.json';

const resources = {
  'zh-TW': {
    translation: zhTW
  },
  'en-US': {
    translation: enUS
  },
  'fr-FR': {
    translation: frFR
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'zh-TW',
    debug: false,
    interpolation: {
      escapeValue: false,
    },
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage'],
    },
  });

export default i18n;
