import { apiClient } from './client';
import type {
  AnesthesiaGuideline,
  GuidelineGenerateRequest,
  AnesthesiaTemplate,
  PaginatedResponse,
} from '@/types';

export const guidelinesApi = {
  // Generate guideline
  generate: async (request: GuidelineGenerateRequest) => {
    const { data } = await apiClient.post<AnesthesiaGuideline>(
      '/anesthesia/guidelines/generate',
      request
    );
    return data;
  },

  // Get all guidelines
  getAll: async (page = 1, size = 100) => {
    const { data } = await apiClient.get<PaginatedResponse<AnesthesiaGuideline>>(
      '/anesthesia/guidelines',
      {
        params: { page, size },
      }
    );
    return data;
  },

  // Get guideline by ID
  getById: async (id: number, language?: string) => {
    const { data } = await apiClient.get<AnesthesiaGuideline>(
      `/anesthesia/guidelines/${id}`,
      {
        params: language ? { language } : {},
      }
    );
    return data;
  },

  // Update guideline
  update: async (id: number, guideline: Partial<AnesthesiaGuideline>) => {
    const { data } = await apiClient.put<AnesthesiaGuideline>(
      `/anesthesia/guidelines/${id}`,
      guideline
    );
    return data;
  },

  // Delete guideline
  delete: async (id: number) => {
    await apiClient.delete(`/anesthesia/guidelines/${id}`);
  },

  // Get guidelines by patient
  getByPatient: async (patientId: number, language?: string) => {
    const { data } = await apiClient.get<AnesthesiaGuideline[]>(
      `/anesthesia/guidelines/patient/${patientId}`,
      {
        params: language ? { language } : {},
      }
    );
    return data;
  },

  // Get guidelines by date
  getByDate: async (startDate?: string, endDate?: string) => {
    const { data } = await apiClient.get<AnesthesiaGuideline[]>(
      '/anesthesia/guidelines/by-date',
      {
        params: { start_date: startDate, end_date: endDate },
      }
    );
    return data;
  },

  // Templates
  getTemplates: async () => {
    const { data } = await apiClient.get<AnesthesiaTemplate[]>('/anesthesia/templates');
    return data;
  },

  getTemplateById: async (id: number) => {
    const { data } = await apiClient.get<AnesthesiaTemplate>(
      `/anesthesia/templates/${id}`
    );
    return data;
  },

  getTemplatesByType: async (anesthesiaType: string) => {
    const { data } = await apiClient.get<AnesthesiaTemplate[]>(
      '/anesthesia/templates/by-type',
      {
        params: { anesthesia_type: anesthesiaType },
      }
    );
    return data;
  },
};
