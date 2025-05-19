"use client"

import type React from "react"

import { useState } from "react"
import { ChevronDown, ChevronUp, Info, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { cn } from "@/lib/utils"

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

  return (
    <div className="w-full mb-12 transition-all duration-300 ease-in-out">
      <div className="bg-surface rounded-lg p-6 border border-border">
        {/* Mode Switch */}
        <div className="flex justify-center mb-6">
          <div className="inline-flex rounded-md p-1 bg-muted/50 border border-border">
            <button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-200 ease-in-out relative",
                mode === "understanding" 
                  ? "bg-accent text-white font-medium shadow-sm" 
                  : "text-muted-foreground hover:text-primary hover:bg-background/50"
              )}
              onClick={() => setMode("understanding")}
            >
              Understanding
            </button>
            <button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-200 ease-in-out relative",
                mode === "retrieval" 
                  ? "bg-accent text-white font-medium shadow-sm" 
                  : "text-muted-foreground hover:text-primary hover:bg-background/50"
              )}
              onClick={() => setMode("retrieval")}
            >
              Retrieval
            </button>
          </div>
        </div>

        {/* Query Input */}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={
                mode === "understanding"
                  ? "Ask about a philosophical concept or thinker..."
                  : "Search for specific passages or quotes..."
              }
              className="w-full p-4 h-32 rounded-md bg-background border border-input focus:border-accent focus:ring-1 focus:ring-accent/30 transition-all duration-200 text-primary placeholder:text-muted-foreground"
              disabled={isLoading}
            />
          </div>

          {/* Advanced Options */}
          <div className="mb-6">
            <button
              type="button"
              className="flex items-center text-secondary hover:text-primary transition-colors duration-200"
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              Advanced Options
              {showAdvanced ? (
                <ChevronUp className="ml-1 h-4 w-4 transition-transform duration-200" />
              ) : (
                <ChevronDown className="ml-1 h-4 w-4 transition-transform duration-200" />
              )}
            </button>

            {showAdvanced && (
              <div className="mt-4 p-4 surface-alt rounded-md animate-slideDown">
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
                  <div className="mb-4 text-sm text-secondary italic animate-fadeIn">
                    Controls how many text chunks are used for context. Higher values may provide more comprehensive
                    answers but could be slower.
                  </div>
                )}

                <Slider
                  value={[chunkCount]}
                  min={1}
                  max={10}
                  step={1}
                  onValueChange={(value) => setChunkCount(value[0])}
                  className="my-4"
                />
              </div>
            )}
          </div>

          {/* Submit and Reset Buttons */}
          <div className="flex justify-center space-x-4">
            <Button
              type="submit"
              className="bg-accent hover:bg-accent-light text-white font-normal py-2 px-6 rounded-md transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
              disabled={!query.trim() || isLoading}
            >
              {isLoading ? "Processing..." : "Submit Query"}
            </Button>
            
            {resetResults && (
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
            )}
          </div>
        </form>
      </div>
    </div>
  )
}