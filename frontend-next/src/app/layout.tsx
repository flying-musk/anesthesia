import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import { MainLayout } from "@/components/layout/main-layout";
import { StructuredData } from "@/components/structured-data";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  title: {
    default: "Anesthesia Management System | AI-Powered Guidelines",
    template: "%s | Anesthesia Management System",
  },
  description: "AI-Powered Anesthesia Guidelines Generation System with multi-language support. Manage patients, generate personalized anesthesia guidelines, and ensure safety with cutting-edge AI technology.",
  keywords: [
    "anesthesia",
    "medical guidelines",
    "AI healthcare",
    "patient management",
    "anesthesia safety",
    "medical AI",
    "healthcare technology",
  ],
  authors: [{ name: "Anesthesia Management Team" }],
  creator: "Anesthesia Management System",
  publisher: "Anesthesia Management System",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    title: "Anesthesia Management System | AI-Powered Guidelines",
    description: "AI-Powered Anesthesia Guidelines Generation System with multi-language support for healthcare professionals.",
    siteName: "Anesthesia Management System",
  },
  twitter: {
    card: "summary_large_image",
    title: "Anesthesia Management System | AI-Powered Guidelines",
    description: "AI-Powered Anesthesia Guidelines Generation System with multi-language support for healthcare professionals.",
    creator: "@anesthesia_ai",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: "/favicon.ico",
    shortcut: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="canonical" href={process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'} />
        <StructuredData />
      </head>
      <body className={inter.className} suppressHydrationWarning>
        <Providers>
          <MainLayout>{children}</MainLayout>
        </Providers>
      </body>
    </html>
  );
}
