import type { QueryResult } from "@/lib/types"
import LoadingIndicator from "./loading-indicator"
import SourceItem from "./source-item"

interface ResultsDisplayProps {
  queryResult: QueryResult | null
  isLoading: boolean
  error: string | null
}

export default function ResultsDisplay({ queryResult, isLoading, error }: ResultsDisplayProps) {
  if (isLoading) {
    return (
      <div className="w-full flex justify-center py-16 animate-fadeIn">
        <LoadingIndicator />
      </div>
    )
  }

  if (error) {
    return (
      <div className="w-full py-8 text-center animate-fadeIn">
        <div className="p-6 rounded-lg border border-error-light bg-error-bg text-error">
          <h3 className="text-xl font-bold mb-2">Error</h3>
          <p>{error}</p>
        </div>
      </div>
    )
  }

  if (!queryResult) return null

  return (
    <div className="w-full mb-16 animate-fadeIn">
      {/* User Query Echo */}
      <div className="mb-6">
        <h2 className="text-xl font-bold mb-2">Your Query</h2>
        <p className="text-primary">{queryResult.query}</p>
      </div>

      {/* Chatbot Response */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Response</h2>
        <div className="prose prose-lg max-w-none">
          {queryResult.response.mode === "understanding" ? (
            <div
              dangerouslySetInnerHTML={{
                __html: formatUnderstandingResponse(queryResult.response.content),
              }}
            />
          ) : (
            <div
              dangerouslySetInnerHTML={{
                __html: formatRetrievalResponse(queryResult.response.content),
              }}
            />
          )}
        </div>
      </div>

      {/* Sources Consulted */}
      <div>
        <h2 className="text-xl font-bold mb-4">Sources Consulted</h2>
        <div className="space-y-4">
          {queryResult.sources.map((source, index) => (
            <SourceItem key={index} source={source} />
          ))}
        </div>
      </div>
    </div>
  )
}

function formatUnderstandingResponse(content: string): string {
  // Convert markdown to HTML with special handling for italics
  return content
    .replace(/## (.*?)$/gm, '<h3 class="text-xl font-bold mt-6 mb-3">$1</h3>')
    .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
    .replace(/\n\n/g, '</p><p class="mb-4">')
}

function formatRetrievalResponse(content: string): string {
  // Convert markdown to HTML with special handling for bold and italics
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
    .replace(/\n\n/g, '</p><p class="mb-4">')
}
