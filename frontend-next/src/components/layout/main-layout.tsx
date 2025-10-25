'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Users,
  FileText,
  UserPlus,
  FilePlus,
  Video,
  Upload,
  Settings,
} from 'lucide-react';
import { ThemeToggle } from '@/components/theme-toggle';

const navigation = [
  {
    name: 'Dashboard',
    href: '/',
    icon: LayoutDashboard,
  },
  {
    name: 'Patients',
    href: '/patients',
    icon: Users,
  },
  {
    name: 'Create Patient',
    href: '/patients/create',
    icon: UserPlus,
  },
  {
    name: 'Guidelines',
    href: '/guidelines',
    icon: FileText,
  },
  {
    name: 'Generate Guideline',
    href: '/guidelines/generate',
    icon: FilePlus,
  },
  {
    name: 'Video Player',
    href: '/player',
    icon: Video,
  },
  {
    name: 'Upload Content',
    href: '/upload',
    icon: Upload,
  },
  {
    name: 'Manage Videos',
    href: '/manage',
    icon: Settings,
  },
];

export function MainLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-gray-50/40 dark:bg-gray-900/40" aria-label="Main navigation">
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center border-b px-6">
            <Link href="/" className="flex items-center gap-2 font-semibold" aria-label="Home - Anesthesia Management System">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground" aria-hidden="true">
                <FileText className="h-4 w-4" />
              </div>
              <span className="text-lg">Anesthesia</span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4" aria-label="Primary navigation">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              const Icon = item.icon;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-label={item.name}
                  aria-current={isActive ? 'page' : undefined}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="border-t p-4">
            <p className="text-xs text-muted-foreground">
              © 2025 Anesthesia System
            </p>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1" role="main">
        {/* Header with theme toggle */}
        <header className="sticky top-0 z-10 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto flex h-14 items-center justify-between px-6">
            <h1 className="text-lg font-semibold">Anesthesia Management</h1>
            <ThemeToggle />
          </div>
        </header>
        <div className="container mx-auto p-6">{children}</div>
      </main>
    </div>
  );
}
