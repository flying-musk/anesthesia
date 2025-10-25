import { apiClient } from './client';
import type {
  Patient,
  PatientCreate,
  MedicalHistory,
  MedicalHistoryCreate,
  SurgeryRecord,
  SurgeryRecordCreate,
  PaginatedResponse,
} from '@/types';

export const patientsApi = {
  // Get all patients
  getAll: async (page = 1, size = 100) => {
    const { data } = await apiClient.get<PaginatedResponse<Patient>>('/patients/', {
      params: { page, size },
    });
    return data;
  },

  // Get patient by ID
  getById: async (id: number, language?: string) => {
    const { data } = await apiClient.get<Patient>(`/patients/${id}`, {
      params: language ? { language } : {},
    });
    return data;
  },

  // Create patient
  create: async (patient: PatientCreate) => {
    const { data } = await apiClient.post<Patient>('/patients/', patient);
    return data;
  },

  // Update patient
  update: async (id: number, patient: Partial<PatientCreate>) => {
    const { data } = await apiClient.put<Patient>(`/patients/${id}`, patient);
    return data;
  },

  // Delete patient
  delete: async (id: number) => {
    await apiClient.delete(`/patients/${id}`);
  },

  // Search patients
  search: async (searchParams: {
    health_insurance_number?: string;
    full_name?: string;
    date_of_birth?: string;
  }) => {
    const { data } = await apiClient.post<Patient[]>('/patients/search', searchParams);
    return data;
  },

  // Medical History
  getMedicalHistory: async (patientId: number, language?: string) => {
    const { data } = await apiClient.get<MedicalHistory>(
      `/patients/${patientId}/medical-history`,
      {
        params: language ? { language } : {},
      }
    );
    return data;
  },

  createMedicalHistory: async (patientId: number, history: MedicalHistoryCreate) => {
    const { data } = await apiClient.post<MedicalHistory[]>(
      `/patients/${patientId}/medical-history`,
      history
    );
    return data;
  },

  updateMedicalHistory: async (patientId: number, history: Partial<MedicalHistoryCreate>) => {
    const { data } = await apiClient.put<MedicalHistory>(
      `/patients/${patientId}/medical-history`,
      history
    );
    return data;
  },

  // Surgery Records
  getSurgeryRecords: async (patientId: number, language?: string) => {
    const { data } = await apiClient.get<SurgeryRecord[]>(
      `/patients/${patientId}/surgery-records`,
      {
        params: language ? { language } : {},
      }
    );
    return data;
  },

  createSurgeryRecord: async (patientId: number, record: SurgeryRecordCreate) => {
    const { data } = await apiClient.post<SurgeryRecord[]>(
      `/patients/${patientId}/surgery-records`,
      record
    );
    return data;
  },
};
