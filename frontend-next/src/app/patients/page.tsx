'use client';

import Link from 'next/link';
import { usePatients } from '@/lib/hooks/use-patients';
import { useTranslations } from '@/hooks/use-translations';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { UserPlus, Search, Eye } from 'lucide-react';
import { format } from 'date-fns';
import { useState } from 'react';

export default function PatientsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const { data, isLoading } = usePatients();
  const t = useTranslations();

  const filteredPatients = data?.items?.filter(
    (patient) =>
      patient.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      patient.health_insurance_number
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{t.patients}</h1>
          <p className="text-muted-foreground">
            {t.managePatients}
          </p>
        </div>
        <Link href="/patients/create">
          <Button>
            <UserPlus className="mr-2 h-4 w-4" />
            {t.createPatient}
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder={t.searchPlaceholder}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : filteredPatients && filteredPatients.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{t.insuranceNumber}</TableHead>
                  <TableHead>{t.fullName}</TableHead>
                  <TableHead>{t.dateOfBirth}</TableHead>
                  <TableHead>{t.gender}</TableHead>
                  <TableHead>{t.phone}</TableHead>
                  <TableHead className="text-right">{t.actions}</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPatients.map((patient) => (
                  <TableRow key={patient.id}>
                    <TableCell className="font-medium">
                      {patient.health_insurance_number}
                    </TableCell>
                    <TableCell>{patient.full_name}</TableCell>
                    <TableCell>
                      {format(new Date(patient.date_of_birth), 'MMM dd, yyyy')}
                    </TableCell>
                    <TableCell>
                      {patient.gender === 'M'
                        ? t.male
                        : patient.gender === 'F'
                        ? t.female
                        : 'Other'}
                    </TableCell>
                    <TableCell>{patient.phone_number}</TableCell>
                    <TableCell className="text-right">
                      <Link href={`/patients/${patient.id}`}>
                        <Button variant="ghost" size="sm">
                          <Eye className="mr-2 h-4 w-4" />
                          {t.view}
                        </Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground">No patients found</p>
              <Link href="/patients/create">
                <Button className="mt-4" variant="outline">
                  <UserPlus className="mr-2 h-4 w-4" />
                  Create your first patient
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
