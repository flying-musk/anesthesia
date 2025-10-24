import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { guidelinesApi } from '@/lib/api/guidelines';
import { QUERY_KEYS } from '@/config/api';
import type { GuidelineGenerateRequest } from '@/types';

// Guidelines
export const useGuidelines = (page = 1, size = 100) => {
  return useQuery({
    queryKey: QUERY_KEYS.guidelines.list(page),
    queryFn: () => guidelinesApi.getAll(page, size),
  });
};

export const useGuideline = (id: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.guidelines.detail(id),
    queryFn: () => guidelinesApi.getById(id),
    enabled: !!id,
  });
};

export const useGuidelinesByPatient = (patientId: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.guidelines.byPatient(patientId),
    queryFn: () => guidelinesApi.getByPatient(patientId),
    enabled: !!patientId,
  });
};

export const useGenerateGuideline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: GuidelineGenerateRequest) =>
      guidelinesApi.generate(request),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.guidelines.all });
      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.guidelines.byPatient(data.patient_id),
      });
    },
  });
};

export const useDeleteGuideline = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => guidelinesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: QUERY_KEYS.guidelines.all });
    },
  });
};

// Templates
export const useTemplates = () => {
  return useQuery({
    queryKey: QUERY_KEYS.templates.all,
    queryFn: () => guidelinesApi.getTemplates(),
  });
};

export const useTemplate = (id: number) => {
  return useQuery({
    queryKey: QUERY_KEYS.templates.detail(id),
    queryFn: () => guidelinesApi.getTemplateById(id),
    enabled: !!id,
  });
};

export const useTemplatesByType = (type: string) => {
  return useQuery({
    queryKey: QUERY_KEYS.templates.byType(type),
    queryFn: () => guidelinesApi.getTemplatesByType(type),
    enabled: !!type,
  });
};
