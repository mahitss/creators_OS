export const tokens = {
  colors: {
    // Semantic Backgrounds
    background: 'var(--kinetic-black, #050505)',
    surface: 'var(--kinetic-surface, #0B0B0B)',
    elevatedSurface: 'var(--kinetic-elevated, #101010)',

    // Semantic Text
    primaryText: 'var(--kinetic-white, #F5F5F5)',
    secondaryText: 'var(--kinetic-gray, #A3A3A3)',
    mutedText: 'var(--kinetic-muted, #666666)',

    // Semantic Borders
    border: 'var(--kinetic-border, rgba(255, 255, 255, 0.10))',
    borderSubtle: 'var(--kinetic-border-subtle, rgba(255, 255, 255, 0.05))',
    borderActive: 'var(--kinetic-green, #62E6B2)',

    // Semantic Accents
    primaryAccent: 'var(--kinetic-green, #62E6B2)',
    primaryAccentHover: '#52D6A2',
    success: 'var(--kinetic-green, #62E6B2)',
    warning: 'var(--kinetic-warning, #E7B95E)',
    danger: 'var(--kinetic-error, #FF6B7A)',
    info: 'var(--kinetic-green, #62E6B2)',
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
