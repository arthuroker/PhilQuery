"use client";

import { useState, useCallback } from "react";
import Header from "@/components/header";
import QueryInterface from "@/components/query-interface";
import ResultsDisplay from "@/components/results-display";
import FeedbackButton from "@/components/feedback-button";
import SourcesList from "@/components/sources-list";
import { api } from "@/lib/api";
import type { QueryResult, Citation } from "@/lib/types";

export default function Home() {
  console.log("[Home] Component rendering");
  
  // State management with custom hook
  const {
    queryState,
    setMode,
    setChunkCount,
    processQuery,
    resetResults
  } = useQueryState();

  console.log("[Home] Current queryState:", {
    hasResult: !!queryState.result,
    hasSources: queryState.result?.sources?.length,
    isLoading: queryState.isLoading,
    error: queryState.error
  });

  return (
    // Main container with gradient background
    <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Content container with relative positioning for absolute child elements */}
      <div className="w-full max-w-5xl px-4 sm:px-6 lg:px-8 mx-auto py-8 relative">
        <Header />
        
        {/* Main content area with consistent vertical spacing */}
        <div className="space-y-8">
          <QueryInterface
            mode={queryState.mode}
            setMode={setMode}
            chunkCount={queryState.chunkCount}
            setChunkCount={setChunkCount}
            onSubmit={processQuery}
            isLoading={queryState.isLoading}
            resetResults={resetResults}
          />

          <ResultsDisplay 
            queryResult={queryState.result}
            isLoading={queryState.isLoading}
            error={queryState.error}
          />

          <div className="mt-12">
            <FeedbackButton />
          </div>
        </div>

        {/* Sources list positioned absolutely to the right of main content
            - Uses absolute positioning to avoid affecting main content layout
            - Negative margin (-mr-[32rem]) pushes it further outside the main container to prevent hover effects from being cut off
            - top-24 aligns it with content below the header
            - This approach maintains the original main content width while utilizing available space */}
        <div className="absolute right-0 top-24 -mr-[32rem]">
          <SourcesList />
        </div>
      </div>
    </main>
  );
}

// Custom hook for query state management
function useQueryState() {
  console.log("[useQueryState] Initializing state");
  
  const [queryState, setQueryState] = useState({
    mode: "understanding" as "understanding" | "retrieval",
    chunkCount: 5,
    isLoading: false,
    result: null as QueryResult | null,
    error: null as string | null
  });

  const setMode = useCallback((mode: "understanding" | "retrieval") => {
    console.log("[useQueryState] Setting mode:", mode);
    setQueryState(prev => ({ ...prev, mode }));
  }, []);

  const setChunkCount = useCallback((chunkCount: number) => {
    console.log("[useQueryState] Setting chunkCount:", chunkCount);
    setQueryState(prev => ({ ...prev, chunkCount }));
  }, []);

  const resetResults = useCallback(() => {
    console.log("[useQueryState] Resetting results");
    setQueryState(prev => ({
      ...prev,
      result: null,
      error: null
    }));
  }, []);

  const processQuery = useCallback(async (query: string) => {
    console.log("[useQueryState] Processing query:", { query, mode: queryState.mode, chunkCount: queryState.chunkCount });
    
    if (!query.trim()) {
      console.log("[useQueryState] Empty query, returning");
      return;
    }

    setQueryState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      console.log("[useQueryState] Calling API");
      const response = await api.askQuestion(
        query, 
        queryState.chunkCount, 
        queryState.mode
      );
      
      console.log("[useQueryState] API response received:", {
        hasAnswer: !!response.answer,
        citationsLength: response.citations?.length
      });
      
      // Parse citations
      const sources = parseCitations(response.citations);
      console.log("[useQueryState] Parsed sources:", {
        count: sources.length,
        firstSource: sources[0]
      });
      
      setQueryState(prev => ({
        ...prev,
        isLoading: false,
        result: {
          query,
          response: {
            content: response.answer,
            mode: queryState.mode,
          },
          sources
        }
      }));
    } catch (err) {
      console.error("[useQueryState] Query error:", err);
      setQueryState(prev => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : "An error occurred while processing your query. Please try again."
      }));
    }
  }, [queryState.chunkCount, queryState.mode]);

  return {
    queryState,
    setMode,
    setChunkCount,
    processQuery,
    resetResults
  };
}

// Helper function to parse citations
function parseCitations(citationsJson: string) {
  console.log("[parseCitations] Parsing citations JSON:", citationsJson?.substring(0, 100) + "...");
  try {
    const parsed = JSON.parse(citationsJson).map((citation: any) => ({
      id: citation.citation_id,
      title: citation.metadata?.source_title || citation.source_title,
      author: citation.metadata?.author || citation.author,
      excerpt: citation.excerpt,
      fullText: citation.full_text,
      url: citation.metadata?.url || citation.url
    }));
    console.log("[parseCitations] Successfully parsed citations:", {
      count: parsed.length,
      firstCitation: parsed[0]
    });
    return parsed;
  } catch (err) {
    console.error("[parseCitations] Citation parsing error:", err);
    return [];
  }
}