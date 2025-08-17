import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full bg-white shadow sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="font-bold text-lg">Elyx Dashboard</Link>
        <div className="space-x-4">
          <Link href="/chat">Chat</Link>
          <Link href="/journey">Journey</Link>
          <Link href="/timeline">Timeline</Link>
          <Link href="/metrics">Metrics</Link>
        </div>
      </div>
    </nav>
  );
}
