import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Threat Intelligence",
  description: "OSINT-driven AI threat monitoring dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
