import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from './providers';
import { WebVitalsReporter } from '../components/WebVitalsReporter';

export const metadata: Metadata = {
  title: 'KINETIQ — Intelligence Operating Layer',
  description:
    'Kinetiq is an autonomous enterprise intelligence operating layer connecting AI, agents, workflows, knowledge, decisions, and secure execution.',
  openGraph: {
    title: 'KINETIQ — Intelligence Operating Layer',
    description:
      'Kinetiq is an autonomous enterprise intelligence operating layer connecting AI, agents, workflows, knowledge, decisions, and secure execution.',
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
      <body className="h-full bg-[#050505] text-[#F5F7FA] antialiased flex flex-col selection:bg-[#7CF7C5]/30 selection:text-[#7CF7C5]">
        <ThemeProvider>
          <WebVitalsReporter />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}

