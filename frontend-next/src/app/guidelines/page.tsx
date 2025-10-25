'use client';

import Link from 'next/link';
import { useGuidelines } from '@/lib/hooks/use-guidelines';
import { useLanguage } from '@/contexts/language-context';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { FilePlus, Search, Eye } from 'lucide-react';
import { format } from 'date-fns';
import { useState } from 'react';

export default function GuidelinesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const { language } = useLanguage();
  const { data, isLoading } = useGuidelines();

  const translations = {
    en: {
      title: 'Anesthesia Guidelines',
      subtitle: 'View and manage generated anesthesia guidelines',
      generateButton: 'Generate Guideline',
      searchPlaceholder: 'Search by surgery name or anesthesia type...',
      date: 'Date',
      surgeon: 'Surgeon',
      anesthesiologist: 'Anesthesiologist',
      view: 'View',
      noGuidelines: 'No guidelines found',
      generateFirst: 'Generate your first guideline',
    },
    zh: {
      title: '麻醉指南',
      subtitle: '查看和管理生成的麻醉指南',
      generateButton: '生成指南',
      searchPlaceholder: '按手術名稱或麻醉類型搜索...',
      date: '日期',
      surgeon: '外科醫生',
      anesthesiologist: '麻醉師',
      view: '查看',
      noGuidelines: '未找到指南',
      generateFirst: '生成您的第一個指南',
    },
    fr: {
      title: 'Directives d\'Anesthésie',
      subtitle: 'Voir et gérer les directives d\'anesthésie générées',
      generateButton: 'Générer une Directive',
      searchPlaceholder: 'Rechercher par nom de chirurgie ou type d\'anesthésie...',
      date: 'Date',
      surgeon: 'Chirurgien',
      anesthesiologist: 'Anesthésiste',
      view: 'Voir',
      noGuidelines: 'Aucune directive trouvée',
      generateFirst: 'Générer votre première directive',
    },
    es: {
      title: 'Guías de Anestesia',
      subtitle: 'Ver y administrar guías de anestesia generadas',
      generateButton: 'Generar guía',
      searchPlaceholder: 'Buscar por nombre de cirugía o tipo de anestesia...',
      date: 'Fecha',
      surgeon: 'Cirujano',
      anesthesiologist: 'Anestesiólogo',
      view: 'Ver',
      noGuidelines: 'No se encontraron guías',
      generateFirst: 'Genere su primera guía',
    },
    ja: {
      title: '麻酔ガイドライン',
      subtitle: '生成された麻酔ガイドラインの表示と管理',
      generateButton: 'ガイドラインを生成',
      searchPlaceholder: '手術名または麻酔の種類で検索...',
      date: '日付',
      surgeon: '外科医',
      anesthesiologist: '麻酔科医',
      view: '表示',
      noGuidelines: 'ガイドラインが見つかりません',
      generateFirst: '最初のガイドラインを生成する',
    },
    ko: {
      title: '마취 가이드라인',
      subtitle: '생성된 마취 가이드라인 보기 및 관리',
      generateButton: '가이드라인 생성',
      searchPlaceholder: '수술명 또는 마취 유형으로 검색...',
      date: '날짜',
      surgeon: '외과의',
      anesthesiologist: '마취과 의사',
      view: '보기',
      noGuidelines: '가이드라인을 찾을 수 없습니다',
      generateFirst: '첫 가이드라인 생성하기',
    },
  };

  const t = translations[language];

  const filteredGuidelines = data?.items?.filter(
    (guideline) =>
      guideline.surgery_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      guideline.anesthesia_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {t.title}
          </h1>
          <p className="text-muted-foreground">
            {t.subtitle}
          </p>
        </div>
        <Link href="/guidelines/generate">
          <Button>
            <FilePlus className="mr-2 h-4 w-4" />
            {t.generateButton}
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder={t.searchPlaceholder}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-24 w-full" />
              ))}
            </div>
          ) : filteredGuidelines && filteredGuidelines.length > 0 ? (
            <div className="space-y-4">
              {filteredGuidelines.map((guideline) => (
                <div
                  key={guideline.id}
                  className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-accent"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-semibold">{guideline.surgery_name}</h3>
                      <Badge variant={guideline.is_generated ? 'default' : 'secondary'}>
                        {guideline.anesthesia_type}
                      </Badge>
                      {guideline.is_generated && (
                        <Badge variant="outline">AI Generated</Badge>
                      )}
                    </div>
                    <div className="mt-2 flex gap-6 text-sm text-muted-foreground">
                      <div>
                        <span className="font-medium">{t.date}:</span>{' '}
                        {format(new Date(guideline.surgery_date), 'MMM dd, yyyy')}
                      </div>
                      <div>
                        <span className="font-medium">{t.surgeon}:</span>{' '}
                        {guideline.surgeon_name}
                      </div>
                      <div>
                        <span className="font-medium">{t.anesthesiologist}:</span>{' '}
                        {guideline.anesthesiologist_name}
                      </div>
                    </div>
                  </div>
                  <Link href={`/guidelines/${guideline.id}`}>
                    <Button variant="ghost" size="sm">
                      <Eye className="mr-2 h-4 w-4" />
                      {t.view}
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground">{t.noGuidelines}</p>
              <Link href="/guidelines/generate">
                <Button className="mt-4" variant="outline">
                  <FilePlus className="mr-2 h-4 w-4" />
                  {t.generateFirst}
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
