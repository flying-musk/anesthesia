import { z } from 'zod';

export const guidelineGenerateSchema = z.object({
  patient_id: z.number().min(1, 'Please select a patient'),
  surgery_name: z.string().min(1, 'Surgery name is required'),
  surgery_type: z.enum(['general', 'local', 'regional', 'sedation'], {
    message: 'Please select a surgery type',
  }),
  surgery_date: z.string().min(1, 'Surgery date is required'),
  surgeon_name: z.string().min(1, 'Surgeon name is required'),
  anesthesiologist_name: z.string().min(1, 'Anesthesiologist name is required'),
});

export type GuidelineGenerateFormData = z.infer<typeof guidelineGenerateSchema>;
