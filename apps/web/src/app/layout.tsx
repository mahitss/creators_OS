import type { Metadata } from 'next';
import './globals.css';
import { ThemeProvider } from './providers';
import { WebVitalsReporter } from '../components/WebVitalsReporter';

export const metadata: Metadata = {
  title: 'KINETIQ — The Next Layer of Intelligence',
  description:
    'A unified infrastructure platform to help teams build, ship, and scale AI systems with confidence.',
  openGraph: {
    title: 'KINETIQ — The Next Layer of Intelligence',
    description:
      'A unified infrastructure platform to help teams build, ship, and scale AI systems with confidence.',
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
          href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="h-full bg-[#050505] text-[#fafafa] antialiased flex flex-col font-['Manrope',system-ui,sans-serif]">
        <ThemeProvider>
          <WebVitalsReporter />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
