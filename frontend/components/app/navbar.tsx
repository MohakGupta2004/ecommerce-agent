"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { Shield } from "lucide-react";

export default function Navbar() {
  const navlinks = [
    { name: "Home", href: "/" },
    { name: "About us", href: "/about" },
    { name: "User-guide", href: "/guide" },
    { name: "Pricing", href: "/pricing" },
  ];

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-full px-6 py-6 flex items-center justify-between max-w-7xl mx-auto relative z-50"
    >
      {/* Logo */}
      <div className="flex items-center gap-2">
        <div className="relative">
          <div className="absolute inset-0 bg-blue-500 blur-lg opacity-50"></div>
        </div>
        <span className="text-white font-medium text-lg tracking-wide">NovaCox</span>
      </div>

      {/* Center Links */}
      <div className="hidden md:flex items-center bg-white/5 backdrop-blur-md border border-white/10 rounded-full px-6 py-2 gap-8">
        {navlinks.map((link) => (
          <Link
            key={link.name}
            href={link.href}
            className="text-sm text-gray-300 hover:text-white transition-colors font-light"
          >
            {link.name}
          </Link>
        ))}
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-6">
        <Link href="/signup" className="text-sm text-gray-300 hover:text-white transition-colors">
          Sign up
        </Link>
        <Link
          href="/login"
          className="text-sm text-white border border-white/20 bg-white/5 px-5 py-2 rounded-full hover:bg-white/10 transition-colors"
        >
          Login
        </Link>
      </div>
    </motion.nav>
  );
}
