'use client';

import { use } from 'react';
import Link from 'next/link';
import { useGuideline } from '@/lib/hooks/use-guidelines';
import { useLanguage } from '@/contexts/language-context';
import { useTranslations } from '@/hooks/use-translations';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { ArrowLeft, User, Calendar, Sparkles } from 'lucide-react';
import { format } from 'date-fns';

export default function GuidelineDetailsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const guidelineId = parseInt(resolvedParams.id);
  const { language } = useLanguage();
  const t = useTranslations();

  const { data: guideline, isLoading } = useGuideline(guidelineId, language);

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
        <p className="text-muted-foreground">{t.guidelineNotFound}</p>
        <Link href="/guidelines">
          <Button className="mt-4">{t.backToGuidelines}</Button>
        </Link>
      </div>
    );
  }

  const sections = [
    {
      title: t.anesthesiaTypeInfo,
      content: guideline.anesthesia_type_info,
    },
    { title: t.surgeryProcess, content: guideline.surgery_process },
    { title: t.expectedSensations, content: guideline.expected_sensations },
    { title: t.potentialRisks, content: guideline.potential_risks },
    {
      title: t.preSurgeryInstructions,
      content: guideline.pre_surgery_instructions,
    },
    { title: t.fastingInstructions, content: guideline.fasting_instructions },
    {
      title: t.medicationInstructions,
      content: guideline.medication_instructions,
    },
    { title: t.commonQuestions, content: guideline.common_questions },
    { title: t.postSurgeryCare, content: guideline.post_surgery_care },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/guidelines">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">
              {guideline.surgery_name}
            </h1>
            {guideline.is_generated && (
              <Badge className="bg-gradient-to-r from-blue-600 to-purple-600">
                <Sparkles className="mr-1 h-3 w-3" />
                {t.aiGenerated}
              </Badge>
            )}
          </div>
          <p className="text-muted-foreground">{t.anesthesiaGuideline}</p>
        </div>
      </div>

      {/* Summary Card */}
      <Card>
        <CardHeader>
          <CardTitle>{t.surgeryInformation}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <Calendar className="mt-1 h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {t.surgeryDate}
                  </p>
                  <p className="font-medium">
                    {format(new Date(guideline.surgery_date), 'MMMM dd, yyyy')}
                  </p>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {t.anesthesiaType}
                </p>
                <Badge className="mt-1">{guideline.anesthesia_type}</Badge>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {t.surgeon}
                </p>
                <p className="font-medium">{guideline.surgeon_name}</p>
              </div>
            </div>

            <div className="space-y-3">
              {guideline.patient && (
                <div className="flex items-start gap-3">
                  <User className="mt-1 h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      Patient
                    </p>
                    <Link href={`/patients/${guideline.patient_id}`}>
                      <p className="font-medium hover:underline">
                        {guideline.patient.full_name}
                      </p>
                    </Link>
                  </div>
                </div>
              )}

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  {t.anesthesiologist}
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
                  Additional Notes
                </p>
                <p className="mt-1 text-sm">{guideline.additional_notes}</p>
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Guideline Content */}
      <Card>
        <CardHeader>
          <CardTitle>{t.guidelineDetails}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {sections.map(
            (section, index) =>
              section.content && (
                <div key={index}>
                  {index > 0 && <Separator className="my-6" />}
                  <div>
                    <h3 className="mb-3 text-lg font-semibold">
                      {section.title}
                    </h3>
                    <div className="whitespace-pre-wrap rounded-lg bg-muted/50 p-4 text-sm leading-relaxed">
                      {section.content}
                    </div>
                  </div>
                </div>
              )
          )}

          {sections.every((s) => !s.content) && (
            <p className="text-center text-muted-foreground">
              {t.noGuidelineContent}
            </p>
          )}
        </CardContent>
      </Card>

      {/* Footer */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <div>
              {t.created}: {format(new Date(guideline.created_at), 'PPpp')}
            </div>
            {guideline.generation_notes && (
              <div>Generation Notes: {guideline.generation_notes}</div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
