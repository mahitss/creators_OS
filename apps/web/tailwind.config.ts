import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        vapor: {
          bg: '#050607',
          panel: '#090B0D',
          elevated: '#0C0F11',
          border: 'rgba(255, 255, 255, 0.08)',
          emerald: '#6FF0C2',
          cyan: '#9BB7FF',
          amber: '#F59E0B',
          crimson: '#EF4444',
        },
        slate: {
          950: '#050607',
          900: '#090B0D',
          800: 'rgba(255, 255, 255, 0.08)',
          700: 'rgba(255, 255, 255, 0.14)',
          600: 'rgba(255, 255, 255, 0.25)',
          500: 'rgba(245, 247, 250, 0.40)',
          400: 'rgba(245, 247, 250, 0.60)',
          300: 'rgba(245, 247, 250, 0.75)',
          200: 'rgba(245, 247, 250, 0.88)',
          100: '#F5F7FA',
          50: '#FFFFFF',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
