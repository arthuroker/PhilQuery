import Image from "next/image"
import { motion } from "framer-motion"

export default function Header() {
  return (
    <header className="relative py-20 mb-16 overflow-hidden">
      {/* Solid background color matching main page */}
      <div className="absolute inset-0 bg-slate-50 dark:bg-slate-900" />
      
      <div className="relative z-10 text-center max-w-3xl mx-auto px-4">
        {/* Animated decorative line */}
        <motion.div 
          className="h-px w-24 bg-slate-200 dark:bg-slate-700 mx-auto mb-8"
          initial={{ width: 0 }}
          animate={{ width: 96 }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
        >
          <h1 className="text-5xl font-bold mb-6 flex items-center justify-center gap-3">
            <span className="text-slate-900 dark:text-slate-100 tracking-tight">
              PhilQuery
            </span>
            <motion.span
              initial={{ rotate: -10, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.3, ease: "easeOut" }}
            >
              📜
            </motion.span>
          </h1>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
        >
          <p className="text-xl text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl mx-auto">
            Explore the depths of political philosophy through an AI-powered interface that helps you understand complex
            texts and ideas.
          </p>
        </motion.div>

        {/* Animated decorative line */}
        <motion.div 
          className="h-px w-24 bg-slate-200 dark:bg-slate-700 mx-auto mt-8"
          initial={{ width: 0 }}
          animate={{ width: 96 }}
          transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
        />
      </div>

      {/* Subtle background imagery with reduced opacity */}
      <div className="absolute inset-0 opacity-[0.02] z-0">
        <div className="relative w-full h-full">
          <Image
            src="/placeholder.svg?height=400&width=1200"
            alt="Classical philosophers background"
            fill
            className="object-cover grayscale"
            priority
          />
        </div>
      </div>
    </header>
  )
}
