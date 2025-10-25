'use client';

import { use } from 'react';
import Link from 'next/link';
import { useGuideline } from '@/lib/hooks/use-guidelines';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ArrowLeft, User, Calendar, Sparkles } from 'lucide-react';
import { useState, useEffect } from 'react';
import { getTranslation } from '@/lib/languages';
import { format } from 'date-fns';
import { enUS, zhCN } from 'date-fns/locale';

export default function GuidelineDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const guidelineId = parseInt(resolvedParams.id);

  const { data: guideline, isLoading } = useGuideline(guidelineId);

  // -----------------------
  // 语言切换状态
  // -----------------------
  const [currentLang, setCurrentLang] = useState<'en' | 'zh'>(() => {
    if (typeof window !== 'undefined') {
      const savedLang = localStorage.getItem('language');
      return savedLang === 'zh' ? 'zh' : 'en';
    }
    return 'en';
  });

  useEffect(() => {
    const handleLanguageChange = (event: CustomEvent) => {
      setCurrentLang(event.detail.language);
    };
    window.addEventListener('languageChanged', handleLanguageChange as EventListener);
    return () => {
      window.removeEventListener('languageChanged', handleLanguageChange as EventListener);
    };
  }, []);

  // -----------------------
  // 格式化日期
  // -----------------------
  function formatDate(dateString: string, lang: 'en' | 'zh', dateFormat = 'PPP') {
    const date = new Date(dateString);
    const locale = lang === 'zh' ? zhCN : enUS;
    return format(date, dateFormat, { locale });
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (!guideline) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-muted-foreground">
          {getTranslation(currentLang, 'guideline.notFound')}
        </p>
        <Link href="/guidelines">
          <Button className="mt-4">
            {getTranslation(currentLang, 'guideline.backToGuidelines')}
          </Button>
        </Link>
      </div>
    );
  }

  // -----------------------
  // 内容区块
  // -----------------------
  const sections = [
    { title: getTranslation(currentLang, 'guideline.sections.anesthesiaTypeInfo'), content: guideline.anesthesia_type_info },
    { title: getTranslation(currentLang, 'guideline.sections.surgeryProcess'), content: guideline.surgery_process },
    { title: getTranslation(currentLang, 'guideline.sections.expectedSensations'), content: guideline.expected_sensations },
    { title: getTranslation(currentLang, 'guideline.sections.potentialRisks'), content: guideline.potential_risks },
    { title: getTranslation(currentLang, 'guideline.sections.preSurgeryInstructions'), content: guideline.pre_surgery_instructions },
    { title: getTranslation(currentLang, 'guideline.sections.fastingInstructions'), content: guideline.fasting_instructions },
    { title: getTranslation(currentLang, 'guideline.sections.medicationInstructions'), content: guideline.medication_instructions },
    { title: getTranslation(currentLang, 'guideline.sections.commonQuestions'), content: guideline.common_questions },
    { title: getTranslation(currentLang, 'guideline.sections.postSurgeryCare'), content: guideline.post_surgery_care },
  ];

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center gap-4">
        <Link href="/guidelines">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{guideline.surgery_name}</h1>
            {guideline.is_generated && (
              <Badge className="bg-gradient-to-r from-blue-600 to-purple-600">
                <Sparkles className="mr-1 h-3 w-3" />
                {getTranslation(currentLang, 'guideline.aiGenerated')}
              </Badge>
            )}
          </div>
          <p className="text-muted-foreground">{getTranslation(currentLang, 'guideline.subtitle')}</p>
        </div>
      </div>

      {/* 手术信息卡片 */}
      <Card>
        <CardHeader>
          <CardTitle>{getTranslation(currentLang, 'guideline.surgeryInformation')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <Calendar className="mt-1 h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {getTranslation(currentLang, 'guideline.surgeryDate')}
                  </p>
                  <p className="font-medium">{formatDate(guideline.surgery_date, currentLang)}</p>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {getTranslation(currentLang, 'guideline.anesthesiaType')}
                </p>
                <Badge className="mt-1">{guideline.anesthesia_type}</Badge>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {getTranslation(currentLang, 'guideline.surgeon')}
                </p>
                <p className="font-medium">{guideline.surgeon_name}</p>
              </div>
            </div>

            <div className="space-y-3">
              {guideline.patient && (
                <div className="flex items-start gap-3">
                  <User className="mt-1 h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{getTranslation(currentLang, 'guideline.patient')}</p>
                    <Link href={`/patients/${guideline.patient_id}`}>
                      <p className="font-medium hover:underline">{guideline.patient.full_name}</p>
                    </Link>
                  </div>
                </div>
              )}

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {getTranslation(currentLang, 'guideline.anesthesiologist')}
                </p>
                <p className="font-medium">{guideline.anesthesiologist_name}</p>
              </div>
            </div>
          </div>

          {guideline.additional_notes && (
            <>
              <Separator className="my-4" />
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {getTranslation(currentLang, 'guideline.additionalNotes')}
                </p>
                <p className="mt-1 text-sm">{guideline.additional_notes}</p>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* 指南内容区 */}
      <Card>
        <CardHeader>
          <CardTitle>{getTranslation(currentLang, 'guideline.details')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {sections.map(
            (section, index) =>
              section.content && (
                <div key={index}>
                  {index > 0 && <Separator className="my-6" />}
                  <div>
                    <h3 className="mb-3 text-lg font-semibold">{section.title}</h3>
                    <div className="whitespace-pre-wrap rounded-lg bg-muted/50 p-4 text-sm leading-relaxed">
                      {section.content} {/* 后端内容不翻译 */}
                    </div>
                  </div>
                </div>
              )
          )}

          {sections.every((s) => !s.content) && (
            <p className="text-center text-muted-foreground">
              {getTranslation(currentLang, 'guideline.noContent')}
            </p>
          )}
        </CardContent>
      </Card>

      {/* Footer */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <div>
              {getTranslation(currentLang, 'guideline.createdAt')}: {formatDate(guideline.created_at, currentLang, 'PPpp')}
            </div>
            {guideline.generation_notes && (
              <div>
                {getTranslation(currentLang, 'guideline.generationNotes')}: {guideline.generation_notes}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

