'use client';

import Link from 'next/link';
import { useGuidelines } from '@/lib/hooks/use-guidelines';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { FilePlus, Search, Eye } from 'lucide-react';
import { format } from 'date-fns';
import { useState, useEffect } from 'react';
import { getTranslation } from '@/lib/languages';

export default function GuidelinesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [currentLang, setCurrentLang] = useState<'en' | 'zh'>('en');
  const { data, isLoading } = useGuidelines();

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

  const filteredGuidelines = data?.items?.filter(
    (guideline) =>
      guideline.surgery_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      guideline.anesthesia_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {getTranslation(currentLang, 'guidelines.title')}
          </h1>
          <p className="text-muted-foreground">
            {getTranslation(currentLang, 'guidelines.description')}
          </p>
        </div>
        <Link href="/guidelines/generate">
          <Button>
            <FilePlus className="mr-2 h-4 w-4" />
            {getTranslation(currentLang, 'guidelines.generateGuideline')}
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search by surgery name or anesthesia type..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-24 w-full" />
              ))}
            </div>
          ) : filteredGuidelines && filteredGuidelines.length > 0 ? (
            <div className="space-y-4">
              {filteredGuidelines.map((guideline) => (
                <div
                  key={guideline.id}
                  className="flex items-center justify-between rounded-lg border p-4 transition-colors hover:bg-accent"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-semibold">{guideline.surgery_name}</h3>
                      <Badge variant={guideline.is_generated ? 'default' : 'secondary'}>
                        {guideline.anesthesia_type}
                      </Badge>
                      {guideline.is_generated && (
                        <Badge variant="outline">AI Generated</Badge>
                      )}
                    </div>
                    <div className="mt-2 flex gap-6 text-sm text-muted-foreground">
                      <div>
                        <span className="font-medium">Date:</span>{' '}
                        {format(new Date(guideline.surgery_date), 'MMM dd, yyyy')}
                      </div>
                      <div>
                        <span className="font-medium">Surgeon:</span>{' '}
                        {guideline.surgeon_name}
                      </div>
                      <div>
                        <span className="font-medium">Anesthesiologist:</span>{' '}
                        {guideline.anesthesiologist_name}
                      </div>
                    </div>
                  </div>
                  <Link href={`/guidelines/${guideline.id}`}>
                    <Button variant="ghost" size="sm">
                      <Eye className="mr-2 h-4 w-4" />
                      View
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground">No guidelines found</p>
              <Link href="/guidelines/generate">
                <Button className="mt-4" variant="outline">
                  <FilePlus className="mr-2 h-4 w-4" />
                  Generate your first guideline
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
