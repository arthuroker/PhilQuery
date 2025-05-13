"use client"

import { useState } from "react"
import Header from "@/components/header"
import QueryInterface from "@/components/query-interface"
import ResultsDisplay from "@/components/results-display"
import FeedbackButton from "@/components/feedback-button"
import type { QueryResult } from "@/lib/types"
import { api } from "@/lib/api"

export default function Home() {
  const [mode, setMode] = useState<"understanding" | "retrieval">("understanding")
  const [chunkCount, setChunkCount] = useState(5)
  const [isLoading, setIsLoading] = useState(false)
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (query: string) => {
    if (!query.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await api.askQuestion(query, chunkCount)
      
      // Parse sources
      const sources = response.sources.map(source => {
        // Extract title and author
        const titleMatch = source.match(/\[(\d+)\]\s*(.*?)\s*by\s*(.*?):/);
        if (!titleMatch) return null;
        
        const [, number, title, author] = titleMatch;
        
        // Extract excerpt
        const excerptMatch = source.match(/\(Excerpt: "(.*?)"\)/);
        const excerpt = excerptMatch ? excerptMatch[1] : "";
        
        return {
          title: `[${number}] ${title.trim()} by ${author.trim()}`,
          excerpt: excerpt,
          url: "#" // We don't have URLs in the sources
        };
      }).filter(Boolean); // Remove any null entries
      
      setQueryResult({
        query,
        response: {
          content: response.answer,
          mode: mode,
        },
        sources: sources
      })
    } catch (err) {
      setError("An error occurred while processing your query. Please try again.")
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="min-h-screen flex flex-col items-center">
      <div className="w-full max-w-5xl px-4 sm:px-6 lg:px-8 mx-auto">
        <Header />

        <QueryInterface
          mode={mode}
          setMode={setMode}
          chunkCount={chunkCount}
          setChunkCount={setChunkCount}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        <ResultsDisplay queryResult={queryResult} isLoading={isLoading} error={error} />

        <FeedbackButton />
      </div>
    </main>
  )
}
