import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EquiAudit AI | Enterprise Compliance Platform",
  description: "Continuous EEOC & Algorithmic Bias Auditing for Enterprise ATS Systems",
  icons: {
    icon: [
      {
        url: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect x='0' y='0' width='16' height='100' fill='%236B82C1'/><rect x='0' y='0' width='100' height='16' fill='%23F48873'/><path d='M25 65 C40 30, 65 30, 85 40 C60 65, 35 75, 75 75' stroke='%236B82C1' stroke-width='12' stroke-linecap='round'/></svg>",
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
