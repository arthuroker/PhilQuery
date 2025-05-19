"use client";

import { useState, useCallback } from "react";
import Header from "@/components/header";
import QueryInterface from "@/components/query-interface";
import ResultsDisplay from "@/components/results-display";
import FeedbackButton from "@/components/feedback-button";
import { api } from "@/lib/api";
import type { QueryResult, Citation } from "@/lib/types";

export default function Home() {
  // State management with custom hook
  const {
    queryState,
    setMode,
    setChunkCount,
    processQuery,
    resetResults
  } = useQueryState();

  return (
    <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="w-full max-w-5xl px-4 sm:px-6 lg:px-8 mx-auto py-8">
        <Header />
        
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
      </div>
    </main>
  );
}

// Custom hook for query state management
function useQueryState() {
  const [queryState, setQueryState] = useState({
    mode: "understanding" as "understanding" | "retrieval",
    chunkCount: 5,
    isLoading: false,
    result: null as QueryResult | null,
    error: null as string | null
  });

  const setMode = useCallback((mode: "understanding" | "retrieval") => {
    setQueryState(prev => ({ ...prev, mode }));
  }, []);

  const setChunkCount = useCallback((chunkCount: number) => {
    setQueryState(prev => ({ ...prev, chunkCount }));
  }, []);

  const resetResults = useCallback(() => {
    setQueryState(prev => ({
      ...prev,
      result: null,
      error: null
    }));
  }, []);

  const processQuery = useCallback(async (query: string) => {
    if (!query.trim()) return;

    setQueryState(prev => ({
      ...prev,
      isLoading: true,
      error: null
    }));

    try {
      const response = await api.askQuestion(
        query, 
        queryState.chunkCount, 
        queryState.mode
      );
      
      // Parse citations
      const sources = parseCitations(response.citations);
      
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
      console.error("Query error:", err);
      setQueryState(prev => ({
        ...prev,
        isLoading: false,
        error: "An error occurred while processing your query. Please try again."
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
  try {
    return JSON.parse(citationsJson).map((citation: Citation) => ({
      id: citation.citation_id,
      title: citation.source_title,
      author: citation.author,
      excerpt: citation.excerpt,
      fullText: citation.full_text,
      url: citation.url
    }));
  } catch (err) {
    console.error("Citation parsing error:", err);
    return [];
  }
}