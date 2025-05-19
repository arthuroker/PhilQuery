export default function FeedbackButton() {
  return (
    <div className="w-full text-center py-8 mb-8">
      <a
        href="https://example.com/feedback"
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block text-accent hover:text-accent-light transition-colors duration-200 font-bold"
      >
        Give Feedback
      </a>
    </div>
  )
}
