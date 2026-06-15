/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        ink: {
          DEFAULT: '#0a0a0a',
          muted: '#6b7280',
          soft: '#9ca3af',
        },
        surface: {
          DEFAULT: '#ffffff',
          alt: '#f5f5f7',
          deep: '#fafafa',
        },
        line: '#e5e7eb',
        accent: {
          DEFAULT: '#0a0a0a',
          soft: '#f5f5f7',
        },
      },
      borderRadius: {
        xl: '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
      boxShadow: {
        soft: '0 1px 2px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04)',
        lift: '0 4px 24px rgba(0,0,0,0.06), 0 8px 40px rgba(0,0,0,0.06)',
      },
      letterSpacing: {
        tightest: '-0.04em',
      },
      transitionTimingFunction: {
        smooth: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
  plugins: [],
}
