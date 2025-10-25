'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Link from 'next/link';
import { usePatients } from '@/lib/hooks/use-patients';
import { useGenerateGuideline } from '@/lib/hooks/use-guidelines';
import { useTranslations } from '@/hooks/use-translations';
import { useLanguage } from '@/contexts/language-context';
import {
  guidelineGenerateSchema,
  type GuidelineGenerateFormData,
} from '@/lib/validators/guideline';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ArrowLeft, ArrowRight, Loader2, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function GenerateGuidelinePage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const { data: patientsData } = usePatients();
  const generateGuideline = useGenerateGuideline();
  const t = useTranslations();
  const { language } = useLanguage();

  const STEPS = [t.selectPatient, t.surgeryDetails, t.review];

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
    trigger,
  } = useForm<GuidelineGenerateFormData>({
    resolver: zodResolver(guidelineGenerateSchema),
  });

  const formData = watch();
  const selectedPatient = patientsData?.items?.find(
    (p) => p.id === formData.patient_id
  );

  const handleNext = async () => {
    let isValid = false;
    if (currentStep === 0) {
      isValid = await trigger('patient_id');
    } else if (currentStep === 1) {
      isValid = await trigger([
        'surgery_name',
        'surgery_type',
        'surgery_date',
        'surgeon_name',
        'anesthesiologist_name',
      ]);
    }

    if (isValid || currentStep === 2) {
      setCurrentStep((prev) => Math.min(prev + 1, STEPS.length - 1));
    }
  };

  const handlePrevious = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const onSubmit = async (data: GuidelineGenerateFormData) => {
    try {
      // Backend expects anesthesia_type field (same as surgery_type)
      const requestData = {
        ...data,
        anesthesia_type: data.surgery_type,
        return_language: language, // Add current language to request
      };
      const guidelines = await generateGuideline.mutateAsync(requestData);
      
      // Handle both single guideline and array of guidelines
      let targetGuideline;
      if (Array.isArray(guidelines)) {
        // If backend returns array, find the guideline in current language
        targetGuideline = guidelines.find(g => g.language === language) || guidelines[0];
      } else {
        // If backend returns single guideline
        targetGuideline = guidelines;
      }
      
      router.push(`/guidelines/${targetGuideline.id}`);
    } catch (error) {
      console.error('Error generating guideline:', error);
      alert('Failed to generate guideline. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/guidelines">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {t.generateGuideline}
          </h1>
          <p className="text-muted-foreground">
            {t.generateGuidelineDescription}
          </p>
        </div>
      </div>

      {/* Progress Steps */}
      <div className="flex items-center justify-center gap-2">
        {STEPS.map((step, index) => (
          <div key={step} className="flex items-center">
            <div className="flex items-center gap-2">
              <div
                className={cn(
                  'flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium',
                  index <= currentStep
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted text-muted-foreground'
                )}
              >
                {index + 1}
              </div>
              <span
                className={cn(
                  'text-sm font-medium',
                  index <= currentStep ? 'text-primary' : 'text-muted-foreground'
                )}
              >
                {step}
              </span>
            </div>
            {index < STEPS.length - 1 && (
              <div className="mx-4 h-0.5 w-12 bg-muted" />
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <Card>
          <CardHeader>
            <CardTitle>{STEPS[currentStep]}</CardTitle>
          </CardHeader>
          <CardContent className="min-h-[400px]">
            {/* Step 1: Select Patient */}
            {currentStep === 0 && (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="patient_id">{t.selectPatient} *</Label>
                  <Select
                    value={formData.patient_id?.toString()}
                    onValueChange={(value) =>
                      setValue('patient_id', parseInt(value))
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder={t.choosePatient} />
                    </SelectTrigger>
                    <SelectContent>
                      {patientsData?.items?.map((patient) => (
                        <SelectItem key={patient.id} value={patient.id.toString()}>
                          {patient.full_name} - {patient.health_insurance_number}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  {errors.patient_id && (
                    <p className="text-sm text-red-500">
                      {errors.patient_id.message}
                    </p>
                  )}
                </div>

                {selectedPatient && (
                  <div className="rounded-lg border p-4">
                    <h4 className="mb-3 font-semibold">{t.patientInfo}</h4>
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div>
                        <span className="text-muted-foreground">{t.name}:</span>{' '}
                        {selectedPatient.full_name}
                      </div>
                      <div>
                        <span className="text-muted-foreground">{t.gender}:</span>{' '}
                        {selectedPatient.gender}
                      </div>
                      <div>
                        <span className="text-muted-foreground">{t.phone}:</span>{' '}
                        {selectedPatient.phone_number}
                      </div>
                      <div>
                        <span className="text-muted-foreground">{t.insurance}:</span>{' '}
                        {selectedPatient.health_insurance_number}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Step 2: Surgery Details */}
            {currentStep === 1 && (
              <div className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="surgery_name">{t.surgeryName} *</Label>
                    <Input id="surgery_name" {...register('surgery_name')} />
                    {errors.surgery_name && (
                      <p className="text-sm text-red-500">
                        {errors.surgery_name.message}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="surgery_type">{t.anesthesiaType} *</Label>
                    <Select
                      value={formData.surgery_type}
                      onValueChange={(value) =>
                        setValue(
                          'surgery_type',
                          value as 'general' | 'local' | 'regional' | 'sedation'
                        )
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder={t.selectType} />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="general">{t.general}</SelectItem>
                        <SelectItem value="local">{t.local}</SelectItem>
                        <SelectItem value="regional">{t.regional}</SelectItem>
                        <SelectItem value="sedation">{t.sedation}</SelectItem>
                      </SelectContent>
                    </Select>
                    {errors.surgery_type && (
                      <p className="text-sm text-red-500">
                        {errors.surgery_type.message}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="surgery_date">{t.surgeryDate} *</Label>
                    <Input
                      id="surgery_date"
                      type="date"
                      {...register('surgery_date')}
                    />
                    {errors.surgery_date && (
                      <p className="text-sm text-red-500">
                        {errors.surgery_date.message}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="surgeon_name">{t.surgeonName} *</Label>
                    <Input id="surgeon_name" {...register('surgeon_name')} />
                    {errors.surgeon_name && (
                      <p className="text-sm text-red-500">
                        {errors.surgeon_name.message}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2 md:col-span-2">
                    <Label htmlFor="anesthesiologist_name">
                      {t.anesthesiologistName} *
                    </Label>
                    <Input
                      id="anesthesiologist_name"
                      {...register('anesthesiologist_name')}
                    />
                    {errors.anesthesiologist_name && (
                      <p className="text-sm text-red-500">
                        {errors.anesthesiologist_name.message}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Review */}
            {currentStep === 2 && (
              <div className="space-y-6">
                <div className="rounded-lg border p-4">
                  <h4 className="mb-3 font-semibold">{t.patients}</h4>
                  <p className="text-sm">
                    {selectedPatient?.full_name} (
                    {selectedPatient?.health_insurance_number})
                  </p>
                </div>

                <div className="rounded-lg border p-4">
                  <h4 className="mb-3 font-semibold">{t.surgeryInfo}</h4>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <span className="text-muted-foreground">{t.surgery}:</span>{' '}
                      {formData.surgery_name}
                    </div>
                    <div>
                      <span className="text-muted-foreground">{t.type}:</span>{' '}
                      {formData.surgery_type}
                    </div>
                    <div>
                      <span className="text-muted-foreground">{t.date}:</span>{' '}
                      {formData.surgery_date}
                    </div>
                    <div>
                      <span className="text-muted-foreground">{t.surgeonName}:</span>{' '}
                      {formData.surgeon_name}
                    </div>
                    <div className="col-span-2">
                      <span className="text-muted-foreground">
                        {t.anesthesiologistName}:
                      </span>{' '}
                      {formData.anesthesiologist_name}
                    </div>
                  </div>
                </div>

                <div className="rounded-lg bg-blue-50 p-4">
                  <div className="flex items-start gap-3">
                    <Sparkles className="mt-1 h-5 w-5 text-blue-600" />
                    <div>
                      <h4 className="font-semibold text-blue-900">
                        {t.aiPoweredGeneration}
                      </h4>
                      <p className="text-sm text-blue-700">
                        {t.aiGenerationDescription}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="mt-8 flex justify-between">
              <Button
                type="button"
                variant="outline"
                onClick={handlePrevious}
                disabled={currentStep === 0}
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                {t.previous}
              </Button>

              {currentStep < STEPS.length - 1 ? (
                <Button type="button" onClick={handleNext}>
                  {t.next}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              ) : (
                <Button
                  type="submit"
                  disabled={generateGuideline.isPending}
                  className="bg-gradient-to-r from-blue-600 to-purple-600"
                >
                  {generateGuideline.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Sparkles className="mr-2 h-4 w-4" />
                      {t.generate}
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
