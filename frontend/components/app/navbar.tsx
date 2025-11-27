"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { Search, User, ShoppingBag } from "lucide-react";
import Image from "next/image";

export default function Navbar() {
  const navlinks = [
    { name: "Home", href: "/" },
    { name: "Menu", href: "/menu" },
    { name: "About us", href: "/about" },
    { name: "Reservation", href: "/reservation" },
    { name: "Blog", href: "/blog" },
  ];

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-lg">🍜</span>
          </div>
          <span className="font-semibold text-xl text-gray-900" style={{ fontFamily: '"Inter", sans-serif' }}>
            Crave
          </span>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          {navlinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className={`text-sm font-medium transition-colors ${
                link.name === "Home" 
                  ? "text-orange-500" 
                  : "text-gray-600 hover:text-gray-900"
              }`}
              style={{ fontFamily: '"Inter", sans-serif' }}
            >
              {link.name}
            </Link>
          ))}
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <Search className="w-5 h-5 text-gray-600" />
          </button>
          <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
            <User className="w-5 h-5 text-gray-600" />
          </button>
          <button className="relative p-2 bg-orange-500 rounded-full hover:bg-orange-600 transition-colors">
            <ShoppingBag className="w-5 h-5 text-white" />
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-orange-600 rounded-full text-white text-xs flex items-center justify-center font-medium">
              0
            </span>
          </button>
        </div>
      </div>
    </motion.nav>
  );
}
