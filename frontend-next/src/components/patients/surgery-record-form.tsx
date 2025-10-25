'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useCreateSurgeryRecord } from '@/lib/hooks/use-patients';
import { useLanguage } from '@/contexts/language-context';
import { useTranslations } from '@/hooks/use-translations';
import { surgeryRecordSchema } from '@/lib/validators/patient';
import type { SurgeryRecordFormData } from '@/lib/validators/patient';

interface SurgeryRecordFormProps {
  patientId: number;
  onSuccess?: () => void;
}

export function SurgeryRecordForm({ patientId, onSuccess }: SurgeryRecordFormProps) {
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const { language } = useLanguage();
  const t = useTranslations();
  
  const createMutation = useCreateSurgeryRecord();
  
  const form = useForm<SurgeryRecordFormData>({
    resolver: zodResolver(surgeryRecordSchema),
    defaultValues: {
      surgery_name: '',
      surgery_type: 'general',
      surgery_date: new Date().toISOString().split('T')[0],
      surgeon_name: '',
      anesthesiologist_name: '',
      surgery_duration: 0,
      anesthesia_duration: 0,
      pre_surgery_assessment: '',
      post_surgery_notes: '',
      complications: '',
    },
  });

  const onSubmit = async (data: SurgeryRecordFormData) => {
    try {
      const dataWithLanguage = { ...data, language };
      await createMutation.mutateAsync({ patientId, data: dataWithLanguage });
      setStatus({ type: 'success', message: 'Surgery record created successfully' });
      form.reset(); // Reset form after successful creation
      onSuccess?.();
    } catch (error) {
      const errorMessage = 
        error instanceof Error ? error.message :
        typeof error === 'object' && error !== null && 'response' in error && typeof error.response === 'object' && error.response !== null && 'data' in error.response && typeof error.response.data === 'object' && error.response.data !== null && 'detail' in error.response.data ? String(error.response.data.detail) :
        'An error occurred while saving surgery record';
      
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
          name="surgery_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.surgeryName}</FormLabel>
              <FormControl>
                <Input placeholder={t.surgeryName} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="surgery_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.surgeryType}</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder={t.selectSurgeryType} />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="general">{t.generalAnesthesia}</SelectItem>
                  <SelectItem value="local">{t.localAnesthesia}</SelectItem>
                  <SelectItem value="regional">{t.regionalAnesthesia}</SelectItem>
                  <SelectItem value="sedation">{t.sedationAnesthesia}</SelectItem>
                </SelectContent>
              </Select>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="surgery_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.surgeryDate}</FormLabel>
              <FormControl>
                <Input type="date" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="surgeon_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.surgeon}</FormLabel>
              <FormControl>
                <Input placeholder={t.surgeon} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="anesthesiologist_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.anesthesiologist}</FormLabel>
              <FormControl>
                <Input placeholder={t.anesthesiologist} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="surgery_duration"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t.surgeryDuration}</FormLabel>
                <FormControl>
                  <Input 
                    type="number" 
                    min="0"
                    {...field}
                    onChange={e => field.onChange(e.target.valueAsNumber)}
                  />
                </FormControl>
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="anesthesia_duration"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t.anesthesiaDuration}</FormLabel>
                <FormControl>
                  <Input 
                    type="number"
                    min="0"
                    {...field}
                    onChange={e => field.onChange(e.target.valueAsNumber)}
                  />
                </FormControl>
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="pre_surgery_assessment"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.preSurgeryAssessment}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.preSurgeryAssessment} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="post_surgery_notes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.postSurgeryNotes}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.postSurgeryNotes} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="complications"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t.complications}</FormLabel>
              <FormControl>
                <Textarea placeholder={t.complications} {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          className="w-full"
          disabled={createMutation.isPending}
        >
          {createMutation.isPending ? t.saving : t.createSurgeryRecord}
        </Button>
      </form>
    </Form>
  );
}