import { useLanguage } from '@/contexts/language-context';
import { getTranslations } from '@/lib/i18n';

export function useTranslations() {
  const { language } = useLanguage();
  return getTranslations(language);
}
