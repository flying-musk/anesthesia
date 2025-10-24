// Patient types
export interface Patient {
  id: number;
  health_insurance_number: string;
  full_name: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  phone_number?: string;
  emergency_contact_name?: string;
  emergency_contact_relationship?: string;
  emergency_contact_phone?: string;
  created_at: string;
  updated_at: string;
  medical_history?: MedicalHistory;
  surgery_records?: SurgeryRecord[];
  anesthesia_guidelines?: AnesthesiaGuideline[];
}

export interface MedicalHistory {
  id: number;
  patient_id: number;
  allergies?: string;
  chronic_conditions?: string;
  current_medications?: string;
  previous_surgeries?: string;
  family_history?: string;
  other_medical_info?: string;
  created_at: string;
  updated_at: string;
}

export interface SurgeryRecord {
  id: number;
  patient_id: number;
  surgery_name: string;
  surgery_type: 'general' | 'local' | 'regional' | 'sedation';
  surgery_date: string;
  surgeon_name: string;
  anesthesiologist_name: string;
  surgery_duration?: number;
  anesthesia_duration?: number;
  pre_surgery_assessment?: string;
  post_surgery_notes?: string;
  complications?: string;
  created_at: string;
  updated_at: string;
}

// Anesthesia types
export interface AnesthesiaGuideline {
  id: number;
  patient_id: number;
  surgery_name: string;
  anesthesia_type: string;
  surgery_date: string;
  surgeon_name: string;
  anesthesiologist_name: string;
  anesthesia_type_info?: string;
  surgery_process?: string;
  expected_sensations?: string;
  potential_risks?: string;
  pre_surgery_instructions?: string;
  fasting_instructions?: string;
  medication_instructions?: string;
  common_questions?: string;
  post_surgery_care?: string;
  additional_notes?: string;
  is_generated: boolean;
  generation_notes?: string;
  created_at: string;
  updated_at: string;
  patient?: Patient;
}

export interface AnesthesiaTemplate {
  id: number;
  template_name: string;
  anesthesia_type: string;
  anesthesia_type_template?: string;
  surgery_process_template?: string;
  expected_sensations_template?: string;
  potential_risks_template?: string;
  pre_surgery_template?: string;
  fasting_template?: string;
  medication_template?: string;
  common_questions_template?: string;
  post_surgery_template?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// API Request/Response types
export interface PatientCreate {
  health_insurance_number: string;
  full_name: string;
  date_of_birth: string;
  gender: 'M' | 'F' | 'O';
  phone_number?: string;
  emergency_contact_name?: string;
  emergency_contact_relationship?: string;
  emergency_contact_phone?: string;
}

export interface MedicalHistoryCreate {
  allergies?: string;
  chronic_conditions?: string;
  current_medications?: string;
  previous_surgeries?: string;
  family_history?: string;
  other_medical_info?: string;
}

export interface SurgeryRecordCreate {
  surgery_name: string;
  surgery_type: 'general' | 'local' | 'regional' | 'sedation';
  surgery_date: string;
  surgeon_name: string;
  anesthesiologist_name: string;
  surgery_duration?: number;
  anesthesia_duration?: number;
  pre_surgery_assessment?: string;
  post_surgery_notes?: string;
  complications?: string;
}

export interface GuidelineGenerateRequest {
  patient_id: number;
  surgery_name: string;
  surgery_type: 'general' | 'local' | 'regional' | 'sedation';
  anesthesia_type: 'general' | 'local' | 'regional' | 'sedation';
  surgery_date: string;
  surgeon_name: string;
  anesthesiologist_name: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
