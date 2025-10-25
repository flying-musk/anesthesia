'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';
import { useCreateSurgeryRecord } from '@/lib/hooks/use-patients';
import { useLanguage } from '@/contexts/language-context';
import { surgeryRecordSchema } from '@/lib/validators/patient';
import type { SurgeryRecordFormData } from '@/lib/validators/patient';

interface SurgeryRecordFormProps {
  patientId: number;
  onSuccess?: () => void;
}

export function SurgeryRecordForm({ patientId, onSuccess }: SurgeryRecordFormProps) {
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const { language } = useLanguage();
  
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
              <FormLabel>Surgery Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter surgery name" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="surgery_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Surgery Type</FormLabel>
              <FormControl>
                <Input placeholder="Enter surgery type (e.g., general, local)" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="surgery_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Surgery Date</FormLabel>
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
              <FormLabel>Surgeon Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter surgeon name" {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="anesthesiologist_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Anesthesiologist Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter anesthesiologist name" {...field} />
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
                <FormLabel>Surgery Duration (minutes)</FormLabel>
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
                <FormLabel>Anesthesia Duration (minutes)</FormLabel>
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
              <FormLabel>Pre-Surgery Assessment</FormLabel>
              <FormControl>
                <Textarea placeholder="Enter pre-surgery assessment notes..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="post_surgery_notes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Post-Surgery Notes</FormLabel>
              <FormControl>
                <Textarea placeholder="Enter post-surgery notes..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="complications"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Complications</FormLabel>
              <FormControl>
                <Textarea placeholder="List any complications..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          className="w-full"
          disabled={createMutation.isPending}
        >
          {createMutation.isPending ? 'Creating...' : 'Create Surgery Record'}
        </Button>
      </form>
    </Form>
  );
}