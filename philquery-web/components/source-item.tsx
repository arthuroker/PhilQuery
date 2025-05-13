import type { Source } from "@/lib/types"
import { ExternalLink } from "lucide-react"

interface SourceItemProps {
  source: Source
}

export default function SourceItem({ source }: SourceItemProps) {
  return (
    <div className="p-4 rounded-md border border-border surface-alt">
      <h3 className="font-bold text-lg mb-2">{source.title}</h3>
      <p className="text-primary mb-3">"{source.excerpt}"</p>
      <a
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center text-accent hover:text-accent/80 transition-colors duration-200"
      >
        See online source <ExternalLink className="ml-1 h-4 w-4" />
      </a>
    </div>
  )
}
