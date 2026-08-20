import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from './providers';
import { WebVitalsReporter } from '../components/WebVitalsReporter';

export const metadata: Metadata = {
  title: 'KINETIQ — The Intelligence Operating Layer',
  description:
    'Kinetiq is an autonomous enterprise intelligence operating layer connecting AI, models, agents, workflows, knowledge, decisions, and secure execution.',
  openGraph: {
    title: 'KINETIQ — The Intelligence Operating Layer',
    description:
      'Kinetiq is an autonomous enterprise intelligence operating layer connecting AI, models, agents, workflows, knowledge, decisions, and secure execution.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="h-full bg-[#050505] text-[#F5F7FA] antialiased flex flex-col font-sans selection:bg-[#7CF7C5]/30 selection:text-[#7CF7C5]">
        <ThemeProvider>
          <WebVitalsReporter />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
