"use client"

import type React from "react"
import { Lora } from "next/font/google"
import "./globals.css"

const lora = Lora({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-lora",
  weight: ["400", "700"],
  style: ["normal", "italic"],
})

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body 
        className={`${lora.variable} font-serif bg-background text-primary antialiased`}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  )
}
