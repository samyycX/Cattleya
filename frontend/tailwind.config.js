/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,tsx,jsx}"
  ],
  theme: {
    extend: {
      colors: {
        theme: {
          0: "rgb(var(--theme-0) / <alpha-value>)",
          1: "rgb(var(--theme-1) / <alpha-value>)",
          2: "rgb(var(--theme-2) / <alpha-value>)",
          3: "rgb(var(--theme-3) / <alpha-value>)",
          4: "rgb(var(--theme-4) / <alpha-value>)",
          5: "rgb(var(--theme-5) / <alpha-value>)",
          6: "rgb(var(--theme-6) / <alpha-value>)",
          7: "rgb(var(--theme-7) / <alpha-value>)",
          8: "rgb(var(--theme-8) / <alpha-value>)"
        },
        "success": "rgb(var(--success) / <alpha-value>)",
        "error": "rgb(var(--error) / <alpha-value>)"
      },
      typography: ({ theme }) => ({
        cattleya: {
          css: {
            '--tw-prose-headings': theme('colors.theme[7]/1'),
            '--tw-prose-body': theme('colors.theme[7]/1'),
            '--tw-prose-hr': theme('colors.theme[4]/1'),
            '--tw-prose-quotes': theme('colors.theme[5]/1'),
            '--tw-prose-bullets': theme('colors.theme[4]/1'),
            '--tw-prose-quote-borders': theme('colors.theme[5]/1'),
            blockquote: {
              backgroundColor: 'rgb(var(--theme-4))',
              color: 'rgb(var(--theme-1))',
            }
          }
        }
      }),
    },
  },
  plugins: [
    require("@tailwindcss/typography")
  ],
}

