import type { Metadata } from "next";
import { Inter, Lora } from "next/font/google";

import "./globals.css";

const lora = Lora({ subsets: ["latin"], variable: "--font-serif" });
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "ShelfTxt",
  description: "Shelves, recommendations, and CSV import for your reading list",
  icons: {
    icon: [{ url: "/app-icon-mono.svg", type: "image/svg+xml" }],
    apple: [{ url: "/app-icon-mono.svg", type: "image/svg+xml", sizes: "512x512" }]
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${lora.variable} ${inter.variable}`}>{children}</body>
    </html>
  );
}
