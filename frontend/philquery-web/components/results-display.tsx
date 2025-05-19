import type { QueryResult } from "@/lib/types"
import LoadingIndicator from "./loading-indicator"
import { motion, AnimatePresence } from "framer-motion"
import { AlertCircle, FileText, ChevronUp } from "lucide-react"
import { useState } from "react"
import SourceItem from "./source-item"

interface ResultsDisplayProps {
  queryResult: QueryResult | null
  isLoading: boolean
  error: string | null
}

export default function ResultsDisplay({ queryResult, isLoading, error }: ResultsDisplayProps) {
  const [showSources, setShowSources] = useState(false)
  console.log('[ResultsDisplay] Rendered with props:', { queryResult, isLoading, error });

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        duration: 0.5,
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  }

  const fadeInUp = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.5 }
    }
  };

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  // Log when component is loading
  if (isLoading) {
    console.log('[ResultsDisplay] Loading state active');
    return (
      <div className="w-full flex flex-col items-center justify-center py-16">
        <LoadingIndicator />
        <p className="mt-4 text-gray-500 animate-pulse">Processing your query...</p>
      </div>
    )
  }

  // Log if there is an error
  if (error) {
    console.log('[ResultsDisplay] Error state:', error);
    return (
      <motion.div 
        className="w-full py-8 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="p-6 rounded-lg border border-red-300 bg-red-50 text-red-700">
          <div className="flex items-center justify-center mb-2">
            <AlertCircle className="w-6 h-6 mr-2" />
            <h3 className="text-xl font-bold">Error Occurred</h3>
          </div>
          <p>{error}</p>
          <p className="mt-4 text-sm text-red-600">Please try again with a different query or check your connection.</p>
        </div>
      </motion.div>
    )
  }

  // Log the query result
  if (queryResult) {
    console.log('[ResultsDisplay] queryResult present:', queryResult);
    if (queryResult.sources) {
      console.log('[ResultsDisplay] queryResult.sources:', queryResult.sources);
      if (Array.isArray(queryResult.sources)) {
        queryResult.sources.forEach((src, idx) => {
          console.log(`[ResultsDisplay] Source[${idx}]:`, src);
        });
      } else {
        console.log('[ResultsDisplay] queryResult.sources is not an array:', queryResult.sources);
      }
    } else {
      console.log('[ResultsDisplay] queryResult.sources is missing or falsy:', queryResult.sources);
    }
  } else {
    console.log('[ResultsDisplay] queryResult is null or undefined');
    return null
  }

  const isUnderstandingMode = queryResult.response.mode === "understanding"

  return (
    <motion.div 
      className="w-full mb-16"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Response Header */}
      <motion.div variants={itemVariants} className="mb-2 flex items-center">
        <FileText className="w-5 h-5 mr-2 text-blue-600" />
        <h2 className="text-2xl font-bold">Response</h2>
        {isUnderstandingMode && (
          <span className="ml-3 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">Understanding Mode</span>
        )}
        {!isUnderstandingMode && (
          <span className="ml-3 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">Retrieval Mode</span>
        )}
      </motion.div>

      {/* Response Content */}
      <motion.div 
        variants={itemVariants}
        className="mb-8 p-6 bg-gray-50 rounded-lg"
      >
        <motion.div 
          className="prose prose-lg max-w-none"
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
        >
          {isUnderstandingMode ? (
            <motion.div
              variants={fadeInUp}
              dangerouslySetInnerHTML={{
                __html: formatUnderstandingResponse(queryResult.response.content),
              }}
            />
          ) : (
            <motion.div
              variants={fadeInUp}
              dangerouslySetInnerHTML={{
                __html: formatRetrievalResponse(queryResult.response.content),
              }}
            />
          )}
        </motion.div>
      </motion.div>

      {/* Sources Consulted Section */}
      {(() => {
        if (queryResult.sources && queryResult.sources.length > 0) {
          console.log('[ResultsDisplay] Rendering sources consulted section:', queryResult.sources);
          return (
            <motion.div variants={itemVariants}>
              <motion.div 
                className="flex items-center justify-between cursor-pointer mb-4"
                onClick={() => setShowSources(!showSources)}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                <h2 className="text-xl font-bold flex items-center">
                  Sources Consulted 
                  <motion.span 
                    className="ml-2 px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 500, damping: 15 }}
                  >
                    {queryResult.sources.length} {queryResult.sources.length === 1 ? 'source' : 'sources'}
                  </motion.span>
                </h2>
                <motion.button 
                  className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                  animate={{ rotate: showSources ? 180 : 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <ChevronUp size={20} />
                </motion.button>
              </motion.div>
              
              <AnimatePresence>
                {showSources && (
                  <motion.div 
                    className="space-y-4"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {queryResult.sources.map((source, index) => (
                      <motion.div
                        key={index}
                        variants={fadeInUp}
                        initial="hidden"
                        animate="visible"
                        transition={{ delay: index * 0.1 }}
                      >
                        <SourceItem source={source} isConsulted={true} />
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          );
        } else {
          console.log('[ResultsDisplay] No sources consulted to render or sources array is empty:', queryResult.sources);
          return null;
        }
      })()}
    </motion.div>
  )
}

function formatUnderstandingResponse(content: string): string {
  console.log("Original content:", content);
  
  let formattedContent = content
    // Handle markdown-style bold headers
    .replace(/\*\*([^*]+)\*\*/g, (match, header) => {
      console.log("Found potential header:", header);
      // Check if the header is a standalone line (no other text on the same line)
      const isStandaloneLine = !header.includes('\n') && header.trim().length > 0;
      console.log("Is standalone line:", isStandaloneLine);
      if (isStandaloneLine) {
        console.log("Formatting as header:", header.trim());
        return `<div class="my-6"><h4 class="font-bold text-lg text-gray-900 mb-2">${header.trim()}</h4></div>`;
      }
      console.log("Not formatting as header (not standalone)");
      return match;
    })
    // Handle lists with clean styling
    .replace(/^\s*[-*]\s+(.*?)$/gm, '<li class="ml-6 list-disc mb-2 text-gray-800">$1</li>')
    // Handle italics with clean styling
    .replace(/\*(.*?)\*/g, '<em class="italic text-gray-800">$1</em>')
    // Handle paragraphs with clean styling
    .replace(/\n\n/g, '</p><p class="mb-4 text-gray-800">')
  
  console.log("Formatted content:", formattedContent);
  
  // Wrap with paragraph tags if not already done
  if (!formattedContent.startsWith('<p>')) {
    formattedContent = `<p class="mb-4 text-gray-800">${formattedContent}</p>`
  }
  
  return formattedContent
}

function formatRetrievalResponse(content: string): string {
  // First make sure we have proper paragraph structure
  let formattedContent = content;
  
  // Replace sections that look like source headers with properly formatted HTML
  const sourcePattern = /Source: (.*?)\nSummary: (.*?)\nQuote: (.*?)(?=\n\nSource:|$)/g;
  let match;
  let processedContent = formattedContent;
  let result = '';
  let lastIndex = 0;
  
  // Find each match and replace it
  while ((match = sourcePattern.exec(formattedContent)) !== null) {
    // Add any text before this match
    result += processedContent.substring(lastIndex, match.index);
    
    // Add the formatted source block with bolder headers
    result += '<div class="border-l-2 border-gray-200 pl-4 my-6">' +
      '<h4 class="font-bold text-lg text-gray-900 mb-2">Source: ' + match[1] + '</h4>' +
      '<p class="text-sm text-gray-600 mb-3"><span class="font-bold text-gray-700">Summary: </span>' + match[2] + '</p>' +
      '<blockquote class="border-l-2 border-gray-300 pl-4 my-3">' +
      '<p class="text-gray-700 italic"><span class="font-bold text-gray-700">Quote: </span>' + match[3] + '</p>' +
      '</blockquote>' +
      '</div>';
    
    // Update lastIndex to continue after this match
    lastIndex = match.index + match[0].length;
  }
  
  // Add any remaining text
  result += processedContent.substring(lastIndex);
  formattedContent = result;
  
  // Handle any remaining formatting with clean styling
  formattedContent = formattedContent
    // Handle bold with clean styling
    .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-gray-900">$1</strong>')
    // Handle italics with clean styling
    .replace(/\*(.*?)\*/g, '<em class="italic text-gray-800">$1</em>')
    // Handle links with clean styling
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">$1</a>')
    // Handle paragraphs with clean styling
    .replace(/\n\n/g, '</p><p class="mb-4 text-gray-800">');
  
  // If the content doesn't begin with an HTML tag, wrap it in a paragraph
  if (!formattedContent.startsWith('<')) {
    formattedContent = `<p class="mb-4 text-gray-800">${formattedContent}</p>`;
  }
  
  return formattedContent;
}