'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';
import { useCreateMedicalHistory, useUpdateMedicalHistory } from '@/lib/hooks/use-patients';
import { useLanguage } from '@/contexts/language-context';
import { useTranslations } from '@/hooks/use-translations';
import { medicalHistorySchema } from '@/lib/validators/patient';
import type { MedicalHistoryFormData } from '@/lib/validators/patient';

interface MedicalHistoryFormProps {
  patientId: number;
  existingData?: MedicalHistoryFormData;
  onSuccess?: () => void;
}

export function MedicalHistoryForm({ patientId, existingData, onSuccess }: MedicalHistoryFormProps) {
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const { language } = useLanguage();
  const t = useTranslations();
  
  const createMutation = useCreateMedicalHistory();
  const updateMutation = useUpdateMedicalHistory();
  
  const form = useForm<MedicalHistoryFormData>({
    resolver: zodResolver(medicalHistorySchema),
    defaultValues: {
      allergies: existingData?.allergies || '',
      chronic_conditions: existingData?.chronic_conditions || '',
      current_medications: existingData?.current_medications || '',
      previous_surgeries: existingData?.previous_surgeries || '',
      family_history: existingData?.family_history || '',
      other_medical_info: existingData?.other_medical_info || '',
    },
  });

  // Update form values when existingData changes (e.g., language switch)
  useEffect(() => {
    if (existingData) {
      form.reset({
        allergies: existingData.allergies || '',
        chronic_conditions: existingData.chronic_conditions || '',
        current_medications: existingData.current_medications || '',
        previous_surgeries: existingData.previous_surgeries || '',
        family_history: existingData.family_history || '',
        other_medical_info: existingData.other_medical_info || '',
      });
    }
  }, [existingData, form]);

  const onSubmit = async (data: MedicalHistoryFormData) => {
    try {
      const dataWithLanguage = { ...data, language };
      if (existingData) {
        await updateMutation.mutateAsync({ patientId, data: dataWithLanguage });
        setStatus({ type: 'success', message: 'Medical history updated successfully' });
      } else {
        await createMutation.mutateAsync({ patientId, data: dataWithLanguage });
        setStatus({ type: 'success', message: 'Medical history created successfully' });
        form.reset(); // Reset form after successful creation
      }
      onSuccess?.();
    } catch (error) {
      const errorMessage = 
        error instanceof Error ? error.message :
        typeof error === 'object' && error !== null && 'response' in error && typeof error.response === 'object' && error.response !== null && 'data' in error.response && typeof error.response.data === 'object' && error.response.data !== null && 'detail' in error.response.data ? String(error.response.data.detail) :
        'An error occurred while saving medical history';
      
      setStatus({ 
        type: 'error', 
        message: errorMessage
      });
    }
  };

  return (
    <Form {...form}>
      {status && (
        <Alert className="mb-4" variant={status.type === 'success' ? 'default' : 'destructive'}>
          <AlertDescription>{status.message}</AlertDescription>
        </Alert>
      )}
      
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="allergies"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.allergies}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.allergies} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="chronic_conditions"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.chronicConditions}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.chronicConditions} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="current_medications"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.currentMedications}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.currentMedications} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="previous_surgeries"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.previousSurgeries}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.previousSurgeries} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="family_history"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.familyHistory}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.familyHistory} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="other_medical_info"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.otherMedicalInfo}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.otherMedicalInfo} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          className="w-full"
          disabled={createMutation.isPending || updateMutation.isPending}
        >
          {createMutation.isPending || updateMutation.isPending
            ? t.saving
            : existingData
            ? t.updateMedicalHistory
            : t.createMedicalHistory
          }
        </Button>
      </form>
    </Form>
  );
}