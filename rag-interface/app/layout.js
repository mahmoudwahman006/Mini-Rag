import { JetBrains_Mono, Inter } from "next/font/google";
import "./globals.css";

const mono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-mono",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-body",
});

export const metadata = {
  title: "RAG Pipeline Console",
  description: "Upload, process, index, and search project documents.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${mono.variable} ${inter.variable}`}>{children}</body>
    </html>
  );
}
