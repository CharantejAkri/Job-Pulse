import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { SupabaseProvider } from "@/components/SupabaseProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "JobPulse India - Smart Job Lead Generation",
  description: "Extract verified job leads with HR contacts from LinkedIn, Naukri, and Indeed. AI-powered match scoring for Indian professionals.",
  keywords: ["jobs", "india", "recruitment", "leads", "naukri", "linkedin", "indeed"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SupabaseProvider>
          {children}
        </SupabaseProvider>
      </body>
    </html>
  );
}
