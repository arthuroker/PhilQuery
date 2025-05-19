import type { AvailableSource, ConsultedSource } from "@/lib/types"
import { ExternalLink } from "lucide-react"

interface SourceItemProps {
  source: AvailableSource | ConsultedSource
  isConsulted?: boolean
}

export default function SourceItem({ source, isConsulted = false }: SourceItemProps) {
  const title = 'source_title' in source ? source.source_title : source.title
  const author = source.author
  const url = source.url

  return (
    <div className="p-4 rounded-md border border-border surface-alt">
      <div className="font-bold text-lg mb-1">{title}</div>
      {author && (
        <div className="text-gray-600 mb-2">{author}</div>
      )}
      {isConsulted && 'excerpt' in source && (
        <p className="text-primary mb-3">"{source.excerpt}"</p>
      )}
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center text-accent hover:text-accent/80 transition-colors duration-200"
      >
        See online source <ExternalLink className="ml-1 h-4 w-4" />
      </a>
    </div>
  )
}
