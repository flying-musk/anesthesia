import { z } from 'zod';

export const patientSchema = z.object({
  health_insurance_number: z
    .string()
    .min(1, 'Health insurance number is required')
    .length(10, 'Health insurance number must be exactly 10 digits')
    .regex(/^\d+$/, 'Health insurance number must contain only numbers'),
  full_name: z.string().min(1, 'Full name is required'),
  date_of_birth: z.string().min(1, 'Date of birth is required'),
  gender: z.enum(['M', 'F', 'O'], {
    message: 'Please select a gender',
  }),
  phone_number: z.string().optional(),
  emergency_contact_name: z.string().optional(),
  emergency_contact_relationship: z.string().optional(),
  emergency_contact_phone: z.string().optional(),
});

export const medicalHistorySchema = z.object({
  allergies: z.string().optional(),
  chronic_conditions: z.string().optional(),
  current_medications: z.string().optional(),
  previous_surgeries: z.string().optional(),
  family_history: z.string().optional(),
  other_medical_info: z.string().optional(),
});

export const surgeryRecordSchema = z.object({
  surgery_name: z.string().min(1, 'Surgery name is required'),
  surgery_type: z.enum(['general', 'local', 'regional', 'sedation'], {
    message: 'Please select a surgery type',
  }),
  surgery_date: z.string().min(1, 'Surgery date is required'),
  surgeon_name: z.string().min(1, 'Surgeon name is required'),
  anesthesiologist_name: z.string().min(1, 'Anesthesiologist name is required'),
  surgery_duration: z.number().optional(),
  anesthesia_duration: z.number().optional(),
  pre_surgery_assessment: z.string().optional(),
  post_surgery_notes: z.string().optional(),
  complications: z.string().optional(),
});

export type PatientFormData = z.infer<typeof patientSchema>;
export type MedicalHistoryFormData = z.infer<typeof medicalHistorySchema>;
export type SurgeryRecordFormData = z.infer<typeof surgeryRecordSchema>;
