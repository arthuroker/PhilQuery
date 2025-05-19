import { motion } from "framer-motion"

export default function FeedbackButton() {
  return (
    <motion.div 
      className="w-full text-center py-8 mb-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      <motion.a
        href="https://example.com/feedback"
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-2 px-4 py-2 rounded-md bg-accent/5 hover:bg-accent/10 text-accent hover:text-accent-light transition-all duration-200 font-medium"
        whileHover={{ scale: 1.02, x: 4 }}
        whileTap={{ scale: 0.98 }}
      >
        <span>Give Feedback</span>
        <motion.span
          initial={{ x: 0 }}
          animate={{ x: [0, 4, 0] }}
          transition={{ 
            duration: 1.5,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          →
        </motion.span>
      </motion.a>
    </motion.div>
  )
}
