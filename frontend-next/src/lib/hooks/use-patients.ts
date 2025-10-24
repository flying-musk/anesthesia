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

export const usePatient = (id: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.patients.detail(id),
    queryFn: () => patientsApi.getById(id),
    enabled: !!id,
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
export const useMedicalHistory = (patientId: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.medicalHistory.byPatient(patientId),
    queryFn: () => patientsApi.getMedicalHistory(patientId),
    enabled: !!patientId,
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
export const useSurgeryRecords = (patientId: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.surgeryRecords.byPatient(patientId),
    queryFn: () => patientsApi.getSurgeryRecords(patientId),
    enabled: !!patientId,
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
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.surgeryRecords.byPatient(variables.patientId),
      });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.patients.detail(variables.patientId),
      });
    },
  });
};
