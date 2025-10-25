'use client';

import Link from 'next/link';
import { usePatients } from '@/lib/hooks/use-patients';
import { useGuidelines } from '@/lib/hooks/use-guidelines';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Users, FileText, UserPlus, FilePlus } from 'lucide-react';
import { format } from 'date-fns';
import { useState, useEffect } from 'react';
import { getTranslation } from '@/lib/languages';

export default function DashboardPage() {
  const { data: patientsData, isLoading: patientsLoading } = usePatients(1, 5);
  const { data: guidelinesData, isLoading: guidelinesLoading } = useGuidelines(1, 5);
  const [currentLang, setCurrentLang] = useState<'en' | 'zh'>('en');

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

  const stats = [
    {
      title: getTranslation(currentLang, 'dashboard.stats.totalPatients'),
      value: patientsData?.total ?? 0,
      icon: Users,
      href: '/patients',
      color: 'text-blue-600',
    },
    {
      title: getTranslation(currentLang, 'dashboard.stats.totalGuidelines'),
      value: guidelinesData?.total ?? 0,
      icon: FileText,
      href: '/guidelines',
      color: 'text-green-600',
    },
  ];

  const actions = [
    {
      title: getTranslation(currentLang, 'dashboard.actions.createPatient'),
      description: getTranslation(currentLang, 'dashboard.actions.createPatientDesc'),
      icon: UserPlus,
      href: '/patients/create',
      color: 'bg-blue-500 hover:bg-blue-600',
    },
    {
      title: getTranslation(currentLang, 'dashboard.actions.generateGuideline'),
      description: getTranslation(currentLang, 'dashboard.actions.generateGuidelineDesc'),
      icon: FilePlus,
      href: '/guidelines/generate',
      color: 'bg-green-500 hover:bg-green-600',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{getTranslation(currentLang, 'dashboard.title')}</h1>
        <p className="text-muted-foreground">
          {getTranslation(currentLang, 'dashboard.welcome')}
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <Link href={stat.href}>
                  <Button variant="link" className="px-0 text-xs">
                    {getTranslation(currentLang, 'dashboard.viewAll')}
                  </Button>
                </Link>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <Link key={action.title} href={action.href}>
              <Card className="transition-all hover:shadow-lg">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className={`rounded-lg p-3 text-white ${action.color}`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{action.title}</CardTitle>
                      <p className="text-sm text-muted-foreground">
                        {action.description}
                      </p>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            </Link>
          );
        })}
      </div>

      {/* Recent Activity */}
      <div className="grid gap-4 md:grid-cols-2">
        {/* Recent Patients */}
        <Card>
          <CardHeader>
            <CardTitle>{getTranslation(currentLang, 'dashboard.recent.patients')}</CardTitle>
          </CardHeader>
          <CardContent>
            {patientsLoading ? (
              <div className="space-y-2">
                {[...Array(3)].map((_, i) => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : patientsData?.items?.length ? (
              <div className="space-y-3">
                {patientsData.items.map((patient) => (
                  <Link
                    key={patient.id}
                    href={`/patients/${patient.id}`}
                    className="block rounded-lg border p-3 transition-colors hover:bg-accent"
                  >
                    <div className="font-medium">{patient.full_name}</div>
                    <div className="text-sm text-muted-foreground">
                      {patient.health_insurance_number}
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">{getTranslation(currentLang, 'dashboard.recent.noPatients')}</p>
            )}
          </CardContent>
        </Card>

        {/* Recent Guidelines */}
        <Card>
          <CardHeader>
            <CardTitle>{getTranslation(currentLang, 'dashboard.recent.guidelines')}</CardTitle>
          </CardHeader>
          <CardContent>
            {guidelinesLoading ? (
              <div className="space-y-2">
                {[...Array(3)].map((_, i) => (
                  <Skeleton key={i} className="h-12 w-full" />
                ))}
              </div>
            ) : guidelinesData?.items?.length ? (
              <div className="space-y-3">
                {guidelinesData.items.map((guideline) => (
                  <Link
                    key={guideline.id}
                    href={`/guidelines/${guideline.id}`}
                    className="block rounded-lg border p-3 transition-colors hover:bg-accent"
                  >
                    <div className="font-medium">{guideline.surgery_name}</div>
                    <div className="text-sm text-muted-foreground">
                      {format(new Date(guideline.surgery_date), 'MMM dd, yyyy')} -{' '}
                      {guideline.anesthesia_type}
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                {getTranslation(currentLang, 'dashboard.recent.noGuidelines')}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
