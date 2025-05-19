"use client"

import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import { motion } from "framer-motion"
import { BookOpen } from "lucide-react"
import type { AvailableSource } from "@/lib/types"

export default function SourcesList() {
  const [sources, setSources] = useState<AvailableSource[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchSources() {
      try {
        console.log("[SourcesList] Fetching all sources");
        const data = await api.getSources()
        console.log("[SourcesList] Raw API response:", data);
        
        // Validate and transform the data
        const validSources = data
          .filter((source): source is AvailableSource => {
            const isValid = source && 
              typeof source === 'object' &&
              typeof source.source_title === 'string' &&
              typeof source.author === 'string' &&
              typeof source.url === 'string';
            
            if (!isValid) {
              console.warn("[SourcesList] Invalid source data:", source);
            }
            return isValid;
          });

        console.log("[SourcesList] Processed sources:", {
          count: validSources.length,
          firstSource: validSources[0]
        });
        
        setSources(validSources)
      } catch (err) {
        console.error("[SourcesList] Error fetching sources:", err)
        setError("Failed to load sources")
      } finally {
        setIsLoading(false)
      }
    }

    fetchSources()
  }, [])

  // Animation variants matching query interface
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.6,
        ease: [0.22, 1, 0.36, 1]
      }
    }
  }

  if (isLoading) {
    return (
      <motion.div 
        className="w-80 bg-surface rounded-lg p-6 border border-border shadow-sm hover:shadow-md transition-shadow duration-300"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="animate-pulse">
          <div className="h-6 bg-muted/50 rounded w-3/4 mb-4"></div>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-muted/50 rounded"></div>
            ))}
          </div>
        </div>
      </motion.div>
    )
  }

  if (error) {
    return (
      <motion.div 
        className="w-80 bg-surface rounded-lg p-6 border border-red-200 shadow-sm"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="text-red-600">
          <h3 className="text-lg font-bold mb-2">Error Loading Sources</h3>
          <p className="text-sm">{error}</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div 
      className="w-80 bg-surface rounded-lg p-6 border border-border shadow-sm hover:shadow-md transition-shadow duration-300 overflow-visible"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header section with icon and source count */}
      <div className="flex items-center gap-2 mb-4 pb-3 border-b border-border">
        <BookOpen className="h-5 w-5 text-accent" />
        <h3 className="text-lg font-bold text-primary">
          Available Sources
          <span className="ml-2 px-2 py-0.5 text-xs bg-muted/50 text-muted-foreground rounded-full">
            {sources.length} {sources.length === 1 ? 'source' : 'sources'}
          </span>
        </h3>
      </div>

      {/* Scrollable container for source items
          - px-2: Horizontal padding to prevent content from touching edges
          - overflow-y-auto: Enable vertical scrolling
          - overflow-x-visible: Allow hover effects to extend beyond container */}
      <div className="space-y-3 max-h-[calc(100vh-16rem)] overflow-y-auto px-2 overflow-x-visible">
        {sources.map((source, index) => (
          <motion.a 
            key={index}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-4 rounded-md bg-background border border-input hover:border-accent/50 hover:bg-accent/5 transition-all duration-200 overflow-visible mx-2 cursor-pointer"
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
          >
            <div className="font-medium text-primary">{source.source_title}</div>
            <div className="text-sm text-muted-foreground mt-1">
              {source.author}
            </div>
          </motion.a>
        ))}
      </div>
    </motion.div>
  )
} 