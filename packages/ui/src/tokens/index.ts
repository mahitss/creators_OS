export const tokens = {
  colors: {
    // Semantic Backgrounds
    background: 'var(--vapor-bg, #050607)',
    surface: 'var(--vapor-surface, #090B0D)',
    elevatedSurface: 'var(--vapor-elevated, #0C0F11)',

    // Semantic Text
    primaryText: 'var(--vapor-text-primary, #F5F7FA)',
    secondaryText: 'var(--vapor-text-secondary, rgba(245, 247, 250, 0.65))',
    mutedText: 'var(--vapor-text-muted, rgba(245, 247, 250, 0.40))',

    // Semantic Borders
    border: 'var(--vapor-border, rgba(255, 255, 255, 0.08))',
    borderSubtle: 'var(--vapor-border-subtle, rgba(255, 255, 255, 0.04))',
    borderActive: 'var(--vapor-border-active, #6FF0C2)',

    // Semantic Accents
    primaryAccent: 'var(--vapor-emerald, #6FF0C2)',
    primaryAccentHover: '#5AE0B2',
    success: 'var(--vapor-emerald, #6FF0C2)',
    warning: 'var(--vapor-amber, #F59E0B)',
    danger: 'var(--vapor-crimson, #EF4444)',
    info: 'var(--vapor-cyan, #9BB7FF)',
  },

  typography: {
    fontFamily: {
      sans: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      mono: 'JetBrains Mono, Menlo, Monaco, Consolas, monospace',
    },
    fontSizes: {
      display: '32px',
      h1: '24px',
      h2: '18px',
      h3: '16px',
      body: '14px',
      bodySmall: '13px',
      caption: '12px',
      label: '11px',
      button: '13px',
    },
    fontWeights: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeights: {
      tight: 1.2,
      snug: 1.35,
      normal: 1.5,
      relaxed: 1.625,
    },
  },

  spacing: {
    '3xs': '2px',
    '2xs': '4px',
    xs: '8px',
    sm: '12px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
  },

  borderRadius: {
    none: '0px',
    sm: '4px',
    md: '6px',
    lg: '8px',
    xl: '12px',
    '2xl': '16px',
    full: '9999px',
  },

  shadows: {
    none: 'none',
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.25)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.3)',
  },

  opacity: {
    disabled: 0.4,
    hover: 0.85,
    focus: 1.0,
  },

  zIndex: {
    deep: -1,
    base: 0,
    dropdown: 100,
    sticky: 200,
    overlay: 300,
    modal: 400,
    popover: 500,
    toast: 600,
    tooltip: 700,
  },

  motion: {
    durations: {
      instant: '50ms',
      fast: '120ms',
      normal: '200ms',
      slow: '300ms',
    },
    easing: {
      spring: 'cubic-bezier(0.16, 1, 0.3, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    },
  },

  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
} as const;

export type DesignTokens = typeof tokens;
