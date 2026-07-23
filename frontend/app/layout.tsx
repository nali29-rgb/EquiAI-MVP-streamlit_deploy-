import "./globals.css";

export const metadata = {
  title: "EquiAudit AI | Continuous Compliance Engine",
  description: "Algorithmic Bias & EEOC Compliance Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
