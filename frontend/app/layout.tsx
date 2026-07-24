import type { Metadata } from "next";
import "./globals.css";

// SVG Data URL for Browser Tab Icon
const faviconSvg = `data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect x='0' y='0' width='16' height='100' fill='%236B82C1'/><rect x='0' y='0' width='100' height='16' fill='%23F48873'/><path d='M44 58 L76 58' stroke='%23F48873' stroke-width='8' stroke-linecap='round'/><path d='M46 70 L74 70' stroke='%23F48873' stroke-width='8' stroke-linecap='round'/><path d='M 18 52 C 22 32, 42 16, 54 26 C 62 34, 28 62, 20 68 C 12 74, 26 78, 44 60 C 58 46, 70 34, 82 46 C 88 52, 68 76, 96 20' stroke='%236B82C1' stroke-width='8' stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>`;

export const metadata: Metadata = {
  title: "EquiAudit AI | Enterprise Compliance Platform",
  description: "Continuous EEOC & Algorithmic Bias Auditing for Enterprise ATS Systems",
  icons: {
    icon: [
      {
        url: faviconSvg,
        type: "image/svg+xml",
      },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-50">{children}</body>
    </html>
  );
}
