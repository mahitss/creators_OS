import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = [
  '/',
  '/login',
  '/api/v1/auth/google/verify',
  '/api/v1/auth/passkey',
  '/api/v1/auth/logout',
  '/api/v1/telemetry/web-vitals',
  '/api/v1/health',
  '/_next',
  '/favicon.ico'
];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isPublic = pathname === '/' || PUBLIC_PATHS.some(pub => pub !== '/' && pathname.startsWith(pub));

  // Allow all public routes and all API routes to be handled without redirect
  if (isPublic || pathname.startsWith('/api/')) {
    const response = NextResponse.next();
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    response.headers.set('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
    return response;
  }

  const token = request.cookies.get('vapor_session_token')?.value;
  const isTestEnv = process.env.NODE_ENV === 'test';

  // If unauthenticated and accessing protected page routes, redirect to /login
  if (!token && !isTestEnv) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect_to', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Inject enterprise security response headers
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Cross-Origin-Opener-Policy', 'same-origin-allow-popups');
  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder files
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};
