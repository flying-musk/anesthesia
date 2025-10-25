'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Form, FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';
import { useCreateMedicalHistory, useUpdateMedicalHistory } from '@/lib/hooks/use-patients';
import { medicalHistorySchema } from '@/lib/validators/patient';
import type { MedicalHistoryFormData } from '@/lib/validators/patient';

interface MedicalHistoryFormProps {
  patientId: number;
  existingData?: MedicalHistoryFormData;
  onSuccess?: () => void;
}

export function MedicalHistoryForm({ patientId, existingData, onSuccess }: MedicalHistoryFormProps) {
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  
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

  const onSubmit = async (data: MedicalHistoryFormData) => {
    try {
      if (existingData) {
        await updateMutation.mutateAsync({ patientId, data });
        setStatus({ type: 'success', message: 'Medical history updated successfully' });
      } else {
        await createMutation.mutateAsync({ patientId, data });
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
              <FormLabel>Allergies</FormLabel>
              <FormControl>
                <Textarea placeholder="List any allergies..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="chronic_conditions"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Chronic Conditions</FormLabel>
              <FormControl>
                <Textarea placeholder="List any chronic conditions..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="current_medications"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Current Medications</FormLabel>
              <FormControl>
                <Textarea placeholder="List current medications..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="previous_surgeries"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Previous Surgeries</FormLabel>
              <FormControl>
                <Textarea placeholder="List previous surgeries..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="family_history"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Family History</FormLabel>
              <FormControl>
                <Textarea placeholder="Describe relevant family medical history..." {...field} />
              </FormControl>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="other_medical_info"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Other Medical Information</FormLabel>
              <FormControl>
                <Textarea placeholder="Any other relevant medical information..." {...field} />
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
            ? 'Saving...'
            : existingData
            ? 'Update Medical History'
            : 'Create Medical History'
          }
        </Button>
      </form>
    </Form>
  );
}