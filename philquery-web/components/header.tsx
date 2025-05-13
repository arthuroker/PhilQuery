import Image from "next/image"

export default function Header() {
  return (
    <header className="relative py-12 mb-8 overflow-hidden">
      <div className="relative z-10 text-center">
        <h1 className="text-4xl font-bold mb-4">PhilQuery 📜</h1>
        <p className="text-lg text-secondary max-w-2xl mx-auto">
          Explore the depths of political philosophy through an AI-powered interface that helps you understand complex
          texts and ideas.
        </p>
      </div>

      {/* Background imagery - subtle classical philosophers */}
      <div className="absolute inset-0 opacity-10 z-0">
        <div className="relative w-full h-full">
          <Image
            src="/placeholder.svg?height=400&width=1200"
            alt="Classical philosophers background"
            fill
            className="object-cover grayscale"
            priority
          />
        </div>
      </div>
    </header>
  )
}
