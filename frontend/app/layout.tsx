import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EquiAudit AI | Enterprise Compliance Platform",
  description: "Continuous EEOC & Algorithmic Bias Auditing for Enterprise ATS Systems",
  icons: {
    icon: "/logo.png", // Uses the image from public/logo.png
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
