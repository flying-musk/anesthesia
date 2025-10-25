'use client';

import { use } from 'react';
import Link from 'next/link';
import { usePatient, useMedicalHistory, useSurgeryRecords } from '@/lib/hooks/use-patients';
import { useGuidelinesByPatient } from '@/lib/hooks/use-guidelines';
import { useTranslations } from '@/hooks/use-translations';
import { useLanguage } from '@/contexts/language-context';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, FileText, Calendar, Activity } from 'lucide-react';
import { format } from 'date-fns';

export default function PatientDetailsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const patientId = parseInt(resolvedParams.id);
  const t = useTranslations();
  const { language } = useLanguage();

  const { data: patient, isLoading: patientLoading } = usePatient(patientId, language);
  const { data: medicalHistory } = useMedicalHistory(patientId, language);
  const { data: surgeryRecords } = useSurgeryRecords(patientId, language);
  const { data: guidelines } = useGuidelinesByPatient(patientId, language);

  if (patientLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-16 w-full" />
        <Skeleton className="h-96 w-full" />
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-muted-foreground">{t.patientNotFound}</p>
        <Link href="/patients">
          <Button className="mt-4">{t.backToPatients}</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/patients">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold tracking-tight">
            {patient.full_name}
          </h1>
          <p className="text-muted-foreground">
            {patient.health_insurance_number}
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t.dateOfBirth}</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {format(new Date(patient.date_of_birth), 'MMM dd, yyyy')}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t.gender}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {patient.gender === 'M'
                ? t.male
                : patient.gender === 'F'
                ? t.female
                : t.other}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{t.phone}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{patient.phone_number}</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="details" className="space-y-4">
        <TabsList>
          <TabsTrigger value="details">{t.details}</TabsTrigger>
          <TabsTrigger value="medical-history">{t.medicalHistory}</TabsTrigger>
          <TabsTrigger value="surgeries">{t.surgeries}</TabsTrigger>
          <TabsTrigger value="guidelines">{t.guidelines}</TabsTrigger>
        </TabsList>

        <TabsContent value="details" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{t.patientInformation}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {t.insuranceNumber}
                  </p>
                  <p className="font-medium">{patient.health_insurance_number}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {t.fullName}
                  </p>
                  <p className="font-medium">{patient.full_name}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {t.dateOfBirth}
                  </p>
                  <p className="font-medium">
                    {format(new Date(patient.date_of_birth), 'MMMM dd, yyyy')}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {t.phoneNumber}
                  </p>
                  <p className="font-medium">{patient.phone_number}</p>
                </div>
              </div>

              {patient.emergency_contact_name && (
                <>
                  <div className="border-t pt-4">
                    <h3 className="mb-3 font-semibold">{t.emergencyContact}</h3>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          {t.name}
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_name}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          {t.relationship}
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_relationship || t.notAvailable}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          {t.phone}
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_phone || t.notAvailable}
                        </p>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="medical-history">
          <Card>
            <CardHeader>
              <CardTitle>{t.medicalHistory}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {medicalHistory ? (
                <>
                  {medicalHistory.allergies && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        {t.allergies}
                      </p>
                      <p className="mt-1">{medicalHistory.allergies}</p>
                    </div>
                  )}
                  {medicalHistory.chronic_conditions && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        {t.chronicConditions}
                      </p>
                      <p className="mt-1">{medicalHistory.chronic_conditions}</p>
                    </div>
                  )}
                  {medicalHistory.current_medications && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        {t.currentMedications}
                      </p>
                      <p className="mt-1">{medicalHistory.current_medications}</p>
                    </div>
                  )}
                  {medicalHistory.previous_surgeries && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        {t.previousSurgeries}
                      </p>
                      <p className="mt-1">{medicalHistory.previous_surgeries}</p>
                    </div>
                  )}
                  {medicalHistory.family_history && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        {t.familyHistory}
                      </p>
                      <p className="mt-1">{medicalHistory.family_history}</p>
                    </div>
                  )}
                </>
              ) : (
                <p className="text-muted-foreground">{t.noMedicalHistory}</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="surgeries">
          <Card>
            <CardHeader>
              <CardTitle>{t.surgeryRecords}</CardTitle>
            </CardHeader>
            <CardContent>
              {surgeryRecords && surgeryRecords.length > 0 ? (
                <div className="space-y-4">
                  {surgeryRecords.map((record) => (
                    <div key={record.id} className="rounded-lg border p-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-semibold">{record.surgery_name}</h4>
                          <p className="text-sm text-muted-foreground">
                            {format(new Date(record.surgery_date), 'MMMM dd, yyyy')}
                          </p>
                        </div>
                        <Badge>{record.surgery_type}</Badge>
                      </div>
                      <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <span className="text-muted-foreground">{t.surgeon}:</span>{' '}
                          {record.surgeon_name}
                        </div>
                        <div>
                          <span className="text-muted-foreground">
                            {t.anesthesiologist}:
                          </span>{' '}
                          {record.anesthesiologist_name}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground">{t.noSurgeryRecords}</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="guidelines">
          <Card>
            <CardHeader>
              <CardTitle>{t.anesthesiaGuidelines}</CardTitle>
            </CardHeader>
            <CardContent>
              {guidelines && guidelines.length > 0 ? (
                <div className="space-y-4">
                  {guidelines.map((guideline) => (
                    <Link
                      key={guideline.id}
                      href={`/guidelines/${guideline.id}`}
                      className="block"
                    >
                      <div className="rounded-lg border p-4 transition-colors hover:bg-accent">
                        <div className="flex items-start justify-between">
                          <div>
                            <h4 className="font-semibold">
                              {guideline.surgery_name}
                            </h4>
                            <p className="text-sm text-muted-foreground">
                              {format(
                                new Date(guideline.surgery_date),
                                'MMMM dd, yyyy'
                              )}
                            </p>
                          </div>
                          <Badge>{guideline.anesthesia_type}</Badge>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground">
                  {t.noGuidelinesAvailable}
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
