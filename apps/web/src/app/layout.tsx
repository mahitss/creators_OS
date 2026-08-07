import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Vapor OS — AI Chief of Staff',
  description: 'An AI Chief of Staff that transforms work into background execution.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full">
      <body className="h-full bg-[#090A0F] text-slate-100 antialiased flex flex-col">
        {children}
      </body>
    </html>
  );
}
