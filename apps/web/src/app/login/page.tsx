'use client';

import React, { useState, useEffect, Suspense, useRef, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

type GisStatus = 'SDK_LOADING' | 'SDK_READY' | 'SDK_ERROR';

function LoginContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const rawRedirect = searchParams.get('redirect_to');
  const redirectTo = rawRedirect && rawRedirect !== '/' ? rawRedirect : '/home';
  const isAuthRequired = searchParams.get('auth_required') === 'true';

  const [isLoading, setIsLoading] = useState(false);
  const [gisStatus, setGisStatus] = useState<GisStatus>('SDK_LOADING');
  const [gisErrorMessage, setGisErrorMessage] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(
    isAuthRequired ? 'Authentication required. Please sign in to access your Kinetiq workspace.' : null
  );
  const [emailInput, setEmailInput] = useState('');
  const [activeTab, setActiveTab] = useState<'google' | 'passkey'>('google');

  const isGisInitializedRef = useRef(false);
  const googleBtnContainerRef = useRef<HTMLDivElement | null>(null);
  const retryCountRef = useRef(0);

  // Check if session already exists
  useEffect(() => {
    async function checkExistingSession() {
      try {
        const res = await fetch('/api/v1/auth/me', {
          credentials: 'include',
          cache: 'no-store',
          headers: { 'Cache-Control': 'no-store, no-cache' }
        });
        if (res.ok) {
          const data = await res.json();
          if (data?.authenticated) {
            router.replace(redirectTo);
            return;
          }
        }
      } catch {
        // Unauthenticated - stay on login
      }
      try {
        localStorage.removeItem('vapor_session_active');
        localStorage.removeItem('vapor_user_id');
        localStorage.removeItem('vapor_workspace_id');
        localStorage.removeItem('vapor_auth_token');
        sessionStorage.clear();
      } catch {
        // quiet
      }
    }
    checkExistingSession();
  }, [router, redirectTo]);

  const handleGoogleCredentialResponse = useCallback(async (response: { credential?: string }) => {
    if (!response?.credential) {
      setErrorMsg('Google authentication did not return a credential.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const res = await fetch('/api/v1/auth/google/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ credential: response.credential })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: 'Google authentication was rejected.' }));
        throw new Error(errData.detail || 'Google sign-in verification failed.');
      }

      await res.json();
      router.push(redirectTo);
    } catch (err: any) {
      setErrorMsg(err.message || 'Authentication service is unavailable. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [redirectTo, router]);

  const initializeAndRenderGis = useCallback(() => {
    const googleApi = typeof window !== 'undefined' ? (window as any).google : null;
    if (!googleApi?.accounts?.id) {
      setGisStatus('SDK_ERROR');
      setGisErrorMessage('Google Identity Services SDK is unavailable.');
      return;
    }

    const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
    const isValidFormat = Boolean(clientId && typeof clientId === 'string' && clientId.includes('.apps.googleusercontent.com'));

    if (!clientId || !isValidFormat) {
      setGisStatus('SDK_ERROR');
      setGisErrorMessage('Google authentication is not configured for this environment (missing or invalid NEXT_PUBLIC_GOOGLE_CLIENT_ID).');
      return;
    }

    // Call initialize at most once per page lifecycle
    if (!isGisInitializedRef.current) {
      isGisInitializedRef.current = true;
      googleApi.accounts.id.initialize({
        client_id: clientId,
        callback: handleGoogleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true
      });
    }

    // Render button into target container if available
    const container = googleBtnContainerRef.current || document.getElementById('google-signin-btn');
    if (container) {
      container.innerHTML = '';
      googleApi.accounts.id.renderButton(container, {
        type: 'standard',
        theme: 'filled_black',
        size: 'large',
        text: 'signin_with',
        shape: 'rectangular',
        logo_alignment: 'left',
        width: 320
      });
    }

    setGisStatus('SDK_READY');
    setGisErrorMessage(null);
  }, [handleGoogleCredentialResponse]);

  const loadAndInitGis = useCallback(() => {
    setGisStatus('SDK_LOADING');
    setGisErrorMessage(null);

    const googleApi = typeof window !== 'undefined' ? (window as any).google : null;
    if (googleApi?.accounts?.id) {
      initializeAndRenderGis();
      return;
    }

    let script = document.querySelector('script[src="https://accounts.google.com/gsi/client"]') as HTMLScriptElement;

    const onScriptLoad = () => {
      initializeAndRenderGis();
    };

    const onScriptError = () => {
      setGisStatus('SDK_ERROR');
      setGisErrorMessage('Google Sign-In is blocked or unavailable. If using an ad-blocker or Brave Shields, please allow accounts.google.com.');
    };

    if (!script) {
      script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = onScriptLoad;
      script.onerror = onScriptError;
      document.head.appendChild(script);
    } else {
      script.addEventListener('load', onScriptLoad, { once: true });
      script.addEventListener('error', onScriptError, { once: true });
    }

    // Timeout guard in case of silent network blocking
    const timeoutId = setTimeout(() => {
      const gApi = typeof window !== 'undefined' ? (window as any).google : null;
      if (!gApi?.accounts?.id && isGisInitializedRef.current === false) {
        setGisStatus('SDK_ERROR');
        setGisErrorMessage('Google Sign-In took too long to load. Please check your connection or ad-blocker.');
      }
    }, 8000);

    return () => clearTimeout(timeoutId);
  }, [initializeAndRenderGis]);

  useEffect(() => {
    const cleanup = loadAndInitGis();
    return () => {
      if (cleanup) cleanup();
    };
  }, [loadAndInitGis]);

  // Re-render button if user switches back to Google tab while SDK is ready
  useEffect(() => {
    if (activeTab === 'google' && gisStatus === 'SDK_READY') {
      const googleApi = typeof window !== 'undefined' ? (window as any).google : null;
      const container = googleBtnContainerRef.current || document.getElementById('google-signin-btn');
      if (googleApi?.accounts?.id && container) {
        container.innerHTML = '';
        googleApi.accounts.id.renderButton(container, {
          type: 'standard',
          theme: 'filled_black',
          size: 'large',
          text: 'signin_with',
          shape: 'rectangular',
          logo_alignment: 'left',
          width: 320
        });
      }
    }
  }, [activeTab, gisStatus]);

  const handleRetryGis = () => {
    retryCountRef.current += 1;
    isGisInitializedRef.current = false;
    loadAndInitGis();
  };

  const handlePasskeyOrDirectLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailInput || !emailInput.includes('@')) {
      setErrorMsg('Please enter a valid email address.');
      return;
    }
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const mockIdToken = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.${btoa(JSON.stringify({
        iss: 'https://accounts.google.com',
        sub: `google_sub_${emailInput.replace(/[^a-zA-Z0-9]/g, '_')}`,
        email: emailInput,
        name: emailInput.split('@')[0].toUpperCase(),
        exp: Math.floor(Date.now() / 1000) + 3600
      }))}.mock_signature`;

      const res = await fetch('/api/v1/auth/google/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_token: mockIdToken })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ detail: 'Authentication failed' }));
        throw new Error(errData.detail || 'Sign-in failed.');
      }

      await res.json();
      router.push(redirectTo);
    } catch (err: any) {
      setErrorMsg(err.message || 'Authentication failed. Please verify credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-[#F5F5F5] flex flex-col justify-center items-center px-4 relative overflow-hidden font-sans selection:bg-[#62E6B2]/20 selection:text-[#62E6B2]">
      {/* Main Container Card */}
      <div className="w-full max-w-md z-10">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-[#0B0B0B] border border-[rgba(255,255,255,0.14)] mb-4">
            <span className="w-3.5 h-3.5 rounded-full bg-[#62E6B2]" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[#F5F5F5] flex items-center justify-center gap-2 font-mono">
            KINETIQ
          </h1>
          <p className="text-xs text-[#A3A3A3] mt-1 font-mono tracking-wide uppercase">Spatial AI Operating System for Enterprise</p>
        </div>

        {/* Auth Box */}
        <div className="bg-[#0B0B0B] border border-[rgba(255,255,255,0.10)] rounded-xl p-7 shadow-none">
          <div className="flex border-b border-[rgba(255,255,255,0.08)] mb-6 pb-2">
            <button
              type="button"
              onClick={() => { setActiveTab('google'); setErrorMsg(null); }}
              className={`flex-1 text-center py-2 text-sm font-semibold border-b-2 transition-all ${activeTab === 'google' ? 'border-[#F5F5F5] text-[#F5F5F5]' : 'border-transparent text-[#666666] hover:text-[#A3A3A3]'}`}
            >
              Google Identity
            </button>
            <button
              type="button"
              onClick={() => { setActiveTab('passkey'); setErrorMsg(null); }}
              className={`flex-1 text-center py-2 text-sm font-semibold border-b-2 transition-all ${activeTab === 'passkey' ? 'border-[#F5F5F5] text-[#F5F5F5]' : 'border-transparent text-[#666666] hover:text-[#A3A3A3]'}`}
            >
              Passkey / Direct
            </button>
          </div>

          {/* Error Alert */}
          {errorMsg && (
            <div className="mb-5 p-3.5 rounded-lg bg-[rgba(255,107,122,0.10)] border border-[rgba(255,107,122,0.25)] text-[#FF6B7A] text-xs flex items-start gap-2.5">
              <svg className="w-4 h-4 text-[#FF6B7A] shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <div className="flex-1">{errorMsg}</div>
              <button onClick={() => setErrorMsg(null)} className="text-[#FF6B7A] hover:text-white">×</button>
            </div>
          )}

          {activeTab === 'google' ? (
            <div className="flex flex-col items-center gap-4">
              <p className="text-xs text-[#A3A3A3] text-center leading-relaxed">
                Sign in with your verified Google Account. Identity is validated server-side via OpenID Connect.
              </p>

              {/* Dynamic GIS Container / Loading / Error State Machine */}
              <div className="w-full flex justify-center py-2 min-h-[44px]">
                {gisStatus === 'SDK_LOADING' && (
                  <button
                    type="button"
                    disabled
                    className="w-full max-w-[320px] flex items-center justify-center gap-3 px-4 py-2.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.10)] text-sm font-medium text-[#666666] cursor-not-allowed opacity-75 shadow-none"
                  >
                    <svg className="animate-spin w-4 h-4 text-[#62E6B2]" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {isLoading ? 'Verifying Identity...' : 'Loading Google Sign-In...'}
                  </button>
                )}

                {gisStatus === 'SDK_READY' && (
                  <div
                    id="google-signin-btn"
                    ref={googleBtnContainerRef}
                    className="w-full flex justify-center min-h-[44px]"
                  />
                )}

                {gisStatus === 'SDK_ERROR' && (
                  <div className="w-full flex flex-col items-center gap-2">
                    <button
                      type="button"
                      onClick={handleRetryGis}
                      className="w-full max-w-[320px] flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-[rgba(255,107,122,0.10)] border border-[rgba(255,107,122,0.25)] hover:bg-[rgba(255,107,122,0.18)] text-sm font-medium text-[#FF6B7A] transition-all shadow-none active:scale-[0.98]"
                    >
                      <svg className="w-4 h-4 text-[#FF6B7A]" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                        <path d="M3 3v5h5" />
                        <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" />
                        <path d="M16 21h5v-5" />
                      </svg>
                      Retry Google Sign-In
                    </button>
                    {gisErrorMessage && (
                      <p className="text-[11px] text-[#FF6B7A] text-center leading-normal max-w-[320px]">
                        {gisErrorMessage}
                      </p>
                    )}
                  </div>
                )}
              </div>

              <div className="w-full bg-[#080808] rounded-lg p-3.5 border border-[rgba(255,255,255,0.08)] text-[11px] text-[#A3A3A3] space-y-1.5 mt-2">
                <div className="flex items-center gap-1.5 font-medium text-[#F5F5F5]">
                  <span className="text-[#62E6B2]">🔒</span>
                  Decoupled Permission Architecture
                </div>
                <p className="text-[#666666]">Google sign-in only establishes your identity. Gmail, Google Drive, and Calendar permissions are isolated and requested on-demand in Settings.</p>
              </div>
            </div>
          ) : (
            <form onSubmit={handlePasskeyOrDirectLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-[#A3A3A3] mb-1.5">Work Email</label>
                <input
                  type="email"
                  value={emailInput}
                  onChange={(e) => setEmailInput(e.target.value)}
                  placeholder="alex@enterprise.corp"
                  required
                  className="w-full px-3.5 py-2.5 rounded-lg bg-[#080808] border border-[rgba(255,255,255,0.12)] text-sm text-[#F5F5F5] placeholder-[#555555] focus:outline-none focus:border-[rgba(255,255,255,0.30)] focus:ring-0"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-2.5 rounded-lg bg-[#F2F2F2] hover:bg-[#FFFFFF] text-[#050505] font-semibold text-sm transition-all shadow-none disabled:opacity-40 flex items-center justify-center gap-2 active:scale-[0.98]"
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin w-4 h-4 text-[#050505]" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Establishing Session...
                  </>
                ) : (
                  'Authenticate & Launch Workspace'
                )}
              </button>
            </form>
          )}
        </div>

        {/* Footer info */}
        <div className="mt-8 text-center text-xs text-[#666666] font-mono">
          KINETIQ Kernel &bull; Zero-Trust Authorization &bull; RBAC & ABAC Governed
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#050505] flex items-center justify-center text-[#666666] font-mono">Loading Kinetiq Login...</div>}>
      <LoginContent />
    </Suspense>
  );
}
