'use client';

import { use } from 'react';
import Link from 'next/link';
import { usePatient, useMedicalHistory, useSurgeryRecords } from '@/lib/hooks/use-patients';
import { useGuidelinesByPatient } from '@/lib/hooks/use-guidelines';
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

  const { data: patient, isLoading: patientLoading } = usePatient(patientId);
  const { data: medicalHistory } = useMedicalHistory(patientId);
  const { data: surgeryRecords } = useSurgeryRecords(patientId);
  const { data: guidelines } = useGuidelinesByPatient(patientId);

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
        <p className="text-muted-foreground">Patient not found</p>
        <Link href="/patients">
          <Button className="mt-4">Back to Patients</Button>
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
            <CardTitle className="text-sm font-medium">Date of Birth</CardTitle>
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
            <CardTitle className="text-sm font-medium">Gender</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {patient.gender === 'M'
                ? 'Male'
                : patient.gender === 'F'
                ? 'Female'
                : 'Other'}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Phone</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{patient.phone_number}</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="details" className="space-y-4">
        <TabsList>
          <TabsTrigger value="details">Details</TabsTrigger>
          <TabsTrigger value="medical-history">Medical History</TabsTrigger>
          <TabsTrigger value="surgeries">Surgeries</TabsTrigger>
          <TabsTrigger value="guidelines">Guidelines</TabsTrigger>
        </TabsList>

        <TabsContent value="details" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Patient Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Insurance Number
                  </p>
                  <p className="font-medium">{patient.health_insurance_number}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Full Name
                  </p>
                  <p className="font-medium">{patient.full_name}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Date of Birth
                  </p>
                  <p className="font-medium">
                    {format(new Date(patient.date_of_birth), 'MMMM dd, yyyy')}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Phone Number
                  </p>
                  <p className="font-medium">{patient.phone_number}</p>
                </div>
              </div>

              {patient.emergency_contact_name && (
                <>
                  <div className="border-t pt-4">
                    <h3 className="mb-3 font-semibold">Emergency Contact</h3>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          Name
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_name}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          Relationship
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_relationship || 'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">
                          Phone
                        </p>
                        <p className="font-medium">
                          {patient.emergency_contact_phone || 'N/A'}
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
              <CardTitle>Medical History</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {medicalHistory ? (
                <>
                  {medicalHistory.allergies && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Allergies
                      </p>
                      <p className="mt-1">{medicalHistory.allergies}</p>
                    </div>
                  )}
                  {medicalHistory.chronic_conditions && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Chronic Conditions
                      </p>
                      <p className="mt-1">{medicalHistory.chronic_conditions}</p>
                    </div>
                  )}
                  {medicalHistory.current_medications && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Current Medications
                      </p>
                      <p className="mt-1">{medicalHistory.current_medications}</p>
                    </div>
                  )}
                  {medicalHistory.previous_surgeries && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Previous Surgeries
                      </p>
                      <p className="mt-1">{medicalHistory.previous_surgeries}</p>
                    </div>
                  )}
                  {medicalHistory.family_history && (
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Family History
                      </p>
                      <p className="mt-1">{medicalHistory.family_history}</p>
                    </div>
                  )}
                </>
              ) : (
                <p className="text-muted-foreground">No medical history available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="surgeries">
          <Card>
            <CardHeader>
              <CardTitle>Surgery Records</CardTitle>
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
                          <span className="text-muted-foreground">Surgeon:</span>{' '}
                          {record.surgeon_name}
                        </div>
                        <div>
                          <span className="text-muted-foreground">
                            Anesthesiologist:
                          </span>{' '}
                          {record.anesthesiologist_name}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-muted-foreground">No surgery records available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="guidelines">
          <Card>
            <CardHeader>
              <CardTitle>Anesthesia Guidelines</CardTitle>
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
                  No guidelines available for this patient
                </p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
