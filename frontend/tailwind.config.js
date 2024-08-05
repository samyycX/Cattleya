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
          0: "var(--theme-0)",
          1: "var(--theme-1)",
          2: "var(--theme-2)",
          3: "var(--theme-3)",
          4: "var(--theme-4)",
          5: "var(--theme-5)",
          6: "var(--theme-6)",
          7: "var(--theme-7)",
          8: "var(--theme-8)"
        },
        "success": "var(--success)",
        "error": "var(--error)"
      },
      typography: ({ theme }) => ({
        cattleya: {
          css: {
            '--tw-prose-headings': theme('colors.theme[7]'),
            '--tw-prose-body': theme('colors.theme[7]'),
            '--tw-prose-hr': theme('colors.theme[4]'),
            '--tw-prose-quotes': theme('colors.theme[5]'),
            '--tw-prose-bullets': theme('colors.theme[4]'),
            '--tw-prose-quote-borders': theme('colors.theme[5]'),
            blockquote: {
              backgroundColor: 'var(--theme-4)',
              color: 'var(--theme-1)',
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

