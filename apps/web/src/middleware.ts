import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('vapor_session_token')?.value;

  // Protected paths check
  if (request.nextUrl.pathname.startsWith('/workspace') && !token) {
    // In production, redirect to /auth/login. For foundation shell, proceed cleanly.
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/workspace/:path*', '/settings/:path*'],
};
