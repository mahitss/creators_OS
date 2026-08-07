export const tokens = {
  colors: {
    bgBase: '#090A0F',
    bgPanel: '#12141C',
    bgElevated: '#1C1F2B',
    borderSubtle: 'rgba(255, 255, 255, 0.08)',
    borderActive: '#10B981',
    textPrimary: '#F9FAFB',
    textSecondary: '#9CA3AF',
    textMuted: '#6B7280',
    accentEmerald: '#10B981',
    accentCyan: '#06B6D4',
    accentAmber: '#F59E0B',
    accentCrimson: '#EF4444',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  fontFamily: {
    sans: 'Inter, system-ui, -apple-system, sans-serif',
    mono: 'JetBrains Mono, Menlo, monospace',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    full: '9999px',
  },
} as const;
