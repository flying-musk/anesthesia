'use client';

import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useCreatePatient } from '@/lib/hooks/use-patients';
import { useTranslations } from '@/hooks/use-translations';
import { patientSchema, type PatientFormData } from '@/lib/validators/patient';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ArrowLeft, Loader2, AlertCircle } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import axios from 'axios';

export default function CreatePatientPage() {
  const router = useRouter();
  const createPatient = useCreatePatient();
  const [apiError, setApiError] = useState<string | null>(null);
  const t = useTranslations();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<PatientFormData>({
    resolver: zodResolver(patientSchema),
  });

  const selectedGender = watch('gender');

  const onSubmit = async (data: PatientFormData) => {
    try {
      setApiError(null);

      // Remove empty strings and convert them to undefined
      const cleanedData = Object.fromEntries(
        Object.entries(data).map(([key, value]) => [
          key,
          value === '' ? undefined : value,
        ])
      ) as PatientFormData;

      console.log('Submitting patient data:', cleanedData);
      const patient = await createPatient.mutateAsync(cleanedData);
      router.push(`/patients/${patient.id}`);
    } catch (error: any) {
      console.error('Error creating patient:', error);
      console.error('Error response data:', error.response?.data);

      // Extract error message from API response
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        setApiError(error.response.data.detail);
      } else {
        setApiError('Failed to create patient. Please try again.');
      }
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/patients">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{t.createPatient}</h1>
          <p className="text-muted-foreground">{t.addNewPatient}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)}>
        <Card>
          <CardHeader>
            <CardTitle>{t.patientInformation}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {apiError && (
              <div className="flex items-center gap-2 rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                <AlertCircle className="h-4 w-4 flex-shrink-0" />
                <p>{apiError}</p>
              </div>
            )}

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="health_insurance_number">
                  {t.healthInsuranceNumber} *
                </Label>
                <Input
                  id="health_insurance_number"
                  {...register('health_insurance_number')}
                />
                {errors.health_insurance_number && (
                  <p className="text-sm text-red-500">
                    {errors.health_insurance_number.message}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="full_name">{t.fullName} *</Label>
                <Input id="full_name" {...register('full_name')} />
                {errors.full_name && (
                  <p className="text-sm text-red-500">
                    {errors.full_name.message}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="date_of_birth">{t.dateOfBirth} *</Label>
                <Input
                  id="date_of_birth"
                  type="date"
                  {...register('date_of_birth')}
                />
                {errors.date_of_birth && (
                  <p className="text-sm text-red-500">
                    {errors.date_of_birth.message}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="gender">{t.gender} *</Label>
                <Select
                  value={selectedGender || ''}
                  onValueChange={(value) =>
                    setValue('gender', value as 'M' | 'F' | 'O')
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder={t.selectGender} />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="M">{t.male}</SelectItem>
                    <SelectItem value="F">{t.female}</SelectItem>
                    <SelectItem value="O">{t.other}</SelectItem>
                  </SelectContent>
                </Select>
                {errors.gender && (
                  <p className="text-sm text-red-500">{errors.gender.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone_number">{t.phone}</Label>
                <Input id="phone_number" {...register('phone_number')} />
                {errors.phone_number && (
                  <p className="text-sm text-red-500">
                    {errors.phone_number.message}
                  </p>
                )}
              </div>
            </div>

            <div className="border-t pt-6">
              <h3 className="mb-4 text-lg font-semibold">
                {t.emergencyContact}
              </h3>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="emergency_contact_name">{t.emergencyContactName}</Label>
                  <Input
                    id="emergency_contact_name"
                    {...register('emergency_contact_name')}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="emergency_contact_relationship">
                    {t.emergencyContactRelationship}
                  </Label>
                  <Input
                    id="emergency_contact_relationship"
                    {...register('emergency_contact_relationship')}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="emergency_contact_phone">{t.emergencyContactPhone}</Label>
                  <Input
                    id="emergency_contact_phone"
                    {...register('emergency_contact_phone')}
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-4">
              <Link href="/patients">
                <Button type="button" variant="outline">
                  {t.cancel}
                </Button>
              </Link>
              <Button type="submit" disabled={createPatient.isPending}>
                {createPatient.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                {t.create}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
