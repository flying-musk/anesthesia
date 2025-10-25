export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
} as const;

export const QUERY_KEYS = {
  patients: {
    all: ['patients'] as const,
    list: (page?: number) => ['patients', 'list', page] as const,
    detail: (id: number) => ['patients', 'detail', id] as const,
    search: (query: string) => ['patients', 'search', query] as const,
  },
  guidelines: {
    all: ['guidelines'] as const,
    list: (page?: number) => ['guidelines', 'list', page] as const,
    detail: (id: number, language?: string) => ['guidelines', 'detail', id, language] as const,
    byPatient: (patientId: number, language?: string) => ['guidelines', 'patient', patientId, language] as const,
  },
  medicalHistory: {
    byPatient: (patientId: number) => ['medical-history', patientId] as const,
  },
  surgeryRecords: {
    byPatient: (patientId: number) => ['surgery-records', patientId] as const,
  },
  templates: {
    all: ['templates'] as const,
    detail: (id: number) => ['templates', 'detail', id] as const,
    byType: (type: string) => ['templates', 'type', type] as const,
  },
} as const;
