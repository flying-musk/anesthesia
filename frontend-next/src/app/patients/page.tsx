'use client';

import Link from 'next/link';
import { usePatients } from '@/lib/hooks/use-patients';
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
import { useState, useEffect } from 'react';
import { getTranslation } from '@/lib/languages';

export default function PatientsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentLang, setCurrentLang] = useState<'en' | 'zh'>('en');
  const { data, isLoading } = usePatients();

  useEffect(() => {
    // 从localStorage获取保存的语言设置
    const savedLang = localStorage.getItem('language') as 'en' | 'zh';
    if (savedLang && (savedLang === 'en' || savedLang === 'zh')) {
      setCurrentLang(savedLang);
    }

    // 监听语言切换事件
    const handleLanguageChange = (event: CustomEvent) => {
      setCurrentLang(event.detail.language);
    };

    window.addEventListener('languageChanged', handleLanguageChange as EventListener);
    
    return () => {
      window.removeEventListener('languageChanged', handleLanguageChange as EventListener);
    };
  }, []);

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
          <h1 className="text-3xl font-bold tracking-tight">{getTranslation(currentLang, 'patients.title')}</h1>
          <p className="text-muted-foreground">
            {getTranslation(currentLang, 'patients.description')}
          </p>
        </div>
        <Link href="/patients/create">
          <Button>
            <UserPlus className="mr-2 h-4 w-4" />
            {getTranslation(currentLang, 'patients.createPatient')}
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder={getTranslation(currentLang, 'patients.search')}
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
                  <TableHead>{getTranslation(currentLang, 'patients.table.insuranceNumber')}</TableHead>
                  <TableHead>{getTranslation(currentLang, 'patients.table.fullName')}</TableHead>
                  <TableHead>{getTranslation(currentLang, 'patients.table.dateOfBirth')}</TableHead>
                  <TableHead>{getTranslation(currentLang, 'patients.table.gender')}</TableHead>
                  <TableHead>{getTranslation(currentLang, 'patients.table.phone')}</TableHead>
                  <TableHead className="text-right">{getTranslation(currentLang, 'patients.table.actions')}</TableHead>
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
                        ? (currentLang === 'zh' ? '男' : 'Male')
                        : patient.gender === 'F'
                        ? (currentLang === 'zh' ? '女' : 'Female')
                        : (currentLang === 'zh' ? '其他' : 'Other')}
                    </TableCell>
                    <TableCell>{patient.phone_number}</TableCell>
                    <TableCell className="text-right">
                      <Link href={`/patients/${patient.id}`}>
                        <Button variant="ghost" size="sm">
                          <Eye className="mr-2 h-4 w-4" />
                          {getTranslation(currentLang, 'patients.table.view')}
                        </Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground">{getTranslation(currentLang, 'patients.noPatients')}</p>
              <Link href="/patients/create">
                <Button className="mt-4" variant="outline">
                  <UserPlus className="mr-2 h-4 w-4" />
                  {getTranslation(currentLang, 'patients.createPatient')}
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
