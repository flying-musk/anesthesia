import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { patientsApi } from '@/lib/api/patients';
import { QUERY_KEYS } from '@/config/api';
import type {
  PatientCreate,
  MedicalHistoryCreate,
  SurgeryRecordCreate,
} from '@/types';

// Patients
export const usePatients = (page = 1, size = 100) => {
  return useQuery({
    queryKey: QUERY_KEYS.patients.list(page),
    queryFn: () => patientsApi.getAll(page, size),
  });
};

export const usePatient = (id: number, language?: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.patients.detail(id, language),
    queryFn: () => patientsApi.getById(id, language),
    enabled: !!id,
    staleTime: 0, // Always consider data stale to ensure fresh fetch on language change
    gcTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
};

export const useCreatePatient = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (patient: PatientCreate) => patientsApi.create(patient),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.patients.all });
    },
  });
};

export const useUpdatePatient = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<PatientCreate> }) =>
      patientsApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.patients.all });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.patients.detail(variables.id),
      });
    },
  });
};

export const useDeletePatient = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => patientsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.patients.all });
    },
  });
};

// Medical History
export const useMedicalHistory = (patientId: number, language?: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.medicalHistory.byPatient(patientId, language),
    queryFn: async () => {
      try {
        return await patientsApi.getMedicalHistory(patientId, language);
      } catch (error: any) {
        // If medical history doesn't exist (404), return null instead of throwing
        if (error.response?.status === 404) {
          return null;
        }
        throw error;
      }
    },
    enabled: !!patientId,
    staleTime: 0, // Always consider data stale to ensure fresh fetch on language change
    gcTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
};

export const useCreateMedicalHistory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      patientId,
      data,
    }: {
      patientId: number;
      data: MedicalHistoryCreate;
    }) => patientsApi.createMedicalHistory(patientId, data),
    onSuccess: (data, variables) => {
      // Invalidate all language-specific queries for this patient
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.medicalHistory.byPatient(variables.patientId),
      });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.patients.detail(variables.patientId),
      });
    },
  });
};

export const useUpdateMedicalHistory = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      patientId,
      data,
    }: {
      patientId: number;
      data: Partial<MedicalHistoryCreate>;
    }) => patientsApi.updateMedicalHistory(patientId, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.medicalHistory.byPatient(variables.patientId),
      });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.patients.detail(variables.patientId),
      });
    },
  });
};

// Surgery Records
export const useSurgeryRecords = (patientId: number, language?: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.surgeryRecords.byPatient(patientId, language),
    queryFn: async () => {
      try {
        return await patientsApi.getSurgeryRecords(patientId, language);
      } catch (error: any) {
        // If no surgery records exist (404), return empty array instead of throwing
        if (error.response?.status === 404) {
          return [];
        }
        throw error;
      }
    },
    enabled: !!patientId,
    staleTime: 0, // Always consider data stale to ensure fresh fetch on language change
    gcTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
};

export const useCreateSurgeryRecord = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      patientId,
      data,
    }: {
      patientId: number;
      data: SurgeryRecordCreate;
    }) => patientsApi.createSurgeryRecord(patientId, data),
    onSuccess: (data, variables) => {
      // Invalidate all language-specific queries for this patient
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.surgeryRecords.byPatient(variables.patientId),
      });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.patients.detail(variables.patientId),
      });
    },
  });
};
