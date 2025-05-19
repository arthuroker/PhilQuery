"use client"

import type React from "react"

import { useState } from "react"
import { ChevronDown, ChevronUp, Info, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { cn } from "@/lib/utils"
import { motion, AnimatePresence } from "framer-motion"

interface QueryInterfaceProps {
  mode: "understanding" | "retrieval"
  setMode: (mode: "understanding" | "retrieval") => void
  chunkCount: number
  setChunkCount: (count: number) => void
  onSubmit: (query: string) => void
  isLoading: boolean
  resetResults?: () => void  // Optional reset function
}

export default function QueryInterface({
  mode,
  setMode,
  chunkCount,
  setChunkCount,
  onSubmit,
  isLoading,
  resetResults,
}: QueryInterfaceProps) {
  const [query, setQuery] = useState("")
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [showChunkInfo, setShowChunkInfo] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(query)
  }

  const handleReset = () => {
    setQuery("")
    resetResults?.() // Only call if provided
  }

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        ease: [0.22, 1, 0.36, 1],
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.5 }
    }
  }

  return (
    <motion.div 
      className="w-full mb-12"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div 
        className="bg-surface rounded-lg p-6 border border-border shadow-sm hover:shadow-md transition-shadow duration-300"
        variants={itemVariants}
      >
        {/* Mode Switch */}
        <motion.div 
          className="flex justify-center mb-6"
          variants={itemVariants}
        >
          <div className="inline-flex rounded-md p-1 bg-muted/50 border border-border">
            <motion.button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-200 ease-in-out relative",
                mode === "understanding" 
                  ? "bg-accent text-white font-medium shadow-sm" 
                  : "text-muted-foreground hover:text-primary hover:bg-background/50"
              )}
              onClick={() => setMode("understanding")}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Understanding
            </motion.button>
            <motion.button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-200 ease-in-out relative",
                mode === "retrieval" 
                  ? "bg-accent text-white font-medium shadow-sm" 
                  : "text-muted-foreground hover:text-primary hover:bg-background/50"
              )}
              onClick={() => setMode("retrieval")}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Retrieval
            </motion.button>
          </div>
        </motion.div>

        {/* Query Input */}
        <motion.form onSubmit={handleSubmit} variants={itemVariants}>
          <motion.div 
            className="mb-4"
            whileHover={{ scale: 1.01 }}
            transition={{ duration: 0.2 }}
          >
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={
                mode === "understanding"
                  ? "Ask about a philosophical concept or thinker..."
                  : "Search for specific passages or quotes..."
              }
              className="w-full p-4 h-32 rounded-md bg-background border border-input focus:border-accent focus:ring-1 focus:ring-accent/30 transition-all duration-200 text-primary placeholder:text-muted-foreground resize-none"
              disabled={isLoading}
            />
          </motion.div>

          {/* Submit and Reset Buttons */}
          <motion.div 
            className="flex gap-3"
            variants={itemVariants}
          >
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                type="submit"
                className="bg-accent hover:bg-accent-light text-white font-normal py-2 px-6 rounded-md transition-all duration-200"
                disabled={!query.trim() || isLoading}
              >
                {isLoading ? "Processing..." : "Submit Query"}
              </Button>
            </motion.div>
            
            {resetResults && (
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleReset}
                  className="border-input hover:bg-muted/50 text-secondary hover:text-primary py-2 px-4 rounded-md transition-all duration-200"
                  disabled={isLoading || (!query.trim() && !resetResults)}
                >
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Reset
                </Button>
              </motion.div>
            )}
          </motion.div>
        </motion.form>

        {/* Advanced Options */}
        <div className="mt-4">
          <button
            type="button"
            className="flex items-center text-secondary hover:text-primary transition-colors duration-200"
            onClick={() => setShowAdvanced(!showAdvanced)}
          >
            Advanced Options
            <ChevronDown className={`ml-1 h-4 w-4 transition-transform duration-200 ${showAdvanced ? 'rotate-180' : ''}`} />
          </button>

          {showAdvanced && (
            <div className="mt-4 p-4 bg-surface-alt rounded-md">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <span className="text-primary mr-2">Chunk Count: {chunkCount}</span>
                  <button
                    type="button"
                    className="text-secondary hover:text-primary"
                    onClick={() => setShowChunkInfo(!showChunkInfo)}
                  >
                    <Info className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {showChunkInfo && (
                <div className="mb-4 text-sm text-secondary italic">
                  Higher chunk counts provide more context for broad queries but may include irrelevant information for specific questions. 
                  Lower counts are better for precise queries, while higher counts work well for exploring broader topics.
                </div>
              )}

              <div>
                <Slider
                  value={[chunkCount]}
                  min={1}
                  max={10}
                  step={1}
                  onValueChange={(value) => setChunkCount(value[0])}
                  className="my-4"
                />
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}