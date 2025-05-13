"use client"

import type React from "react"

import { useState } from "react"
import { ChevronDown, ChevronUp, Info } from "lucide-react"
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
}

export default function QueryInterface({
  mode,
  setMode,
  chunkCount,
  setChunkCount,
  onSubmit,
  isLoading,
}: QueryInterfaceProps) {
  const [query, setQuery] = useState("")
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [showChunkInfo, setShowChunkInfo] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(query)
  }

  return (
    <div className="w-full mb-12 transition-all duration-300 ease-in-out">
      <div className="bg-surface rounded-lg p-6 border border-border">
        {/* Mode Switch */}
        <div className="flex justify-center mb-6">
          <div className="inline-flex rounded-md p-1 bg-muted">
            <button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-300 ease-in-out relative",
                mode === "understanding" ? "text-accent-foreground font-bold" : "text-secondary hover:text-primary",
              )}
              onClick={() => setMode("understanding")}
            >
              {mode === "understanding" && (
                <span className="absolute inset-0 bg-accent rounded-md -z-10 transition-all duration-300 ease-in-out"></span>
              )}
              Understanding
            </button>
            <button
              type="button"
              className={cn(
                "px-4 py-2 rounded-md text-base transition-all duration-300 ease-in-out relative",
                mode === "retrieval" ? "text-accent-foreground font-bold" : "text-secondary hover:text-primary",
              )}
              onClick={() => setMode("retrieval")}
            >
              {mode === "retrieval" && (
                <span className="absolute inset-0 bg-accent rounded-md -z-10 transition-all duration-300 ease-in-out"></span>
              )}
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

          {/* Submit Button */}
          <div className="flex justify-center">
            <Button
              type="submit"
              className="bg-accent hover:bg-accent-light text-white font-normal py-2 px-6 rounded-md transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
              disabled={!query.trim() || isLoading}
            >
              {isLoading ? "Processing..." : "Submit Query"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}
