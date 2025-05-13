export default function LoadingIndicator() {
  return (
    <div className="flex space-x-2 justify-center items-center">
      <div className="h-3 w-3 bg-accent rounded-full animate-pulse-slow"></div>
      <div className="h-3 w-3 bg-accent rounded-full animate-pulse-slow animation-delay-200"></div>
      <div className="h-3 w-3 bg-accent rounded-full animate-pulse-slow animation-delay-400"></div>
    </div>
  )
}
