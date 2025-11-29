"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { Search, User, ShoppingBag } from "lucide-react";
import Image from "next/image";

export default function Navbar() {
  const navlinks = [
    { name: "Products", href: "/", hasDropdown: true },
    { name: "Customer Stories", href: "/stories" },
    { name: "Resources", href: "/resources" },
    { name: "Pricing", href: "/pricing" },
  ];

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-100"
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center transition-transform group-hover:scale-105">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 2L3 7V13L10 18L17 13V7L10 2Z" fill="white" />
            </svg>
          </div>
          <span className="font-semibold text-lg text-gray-900">
            ACP
          </span>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          {navlinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className="text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors flex items-center gap-1"
            >
              {link.name}
              {link.hasDropdown && (
                <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
                  <path d="M6 8L3 5h6L6 8z" />
                </svg>
              )}
            </Link>
          ))}
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/demo"
            className="hidden sm:block text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors px-4 py-2"
          >
            Book A Demo
          </Link>
          <button className="text-sm font-medium text-white bg-black hover:bg-gray-800 transition-all px-6 py-2.5 rounded-full shadow-sm hover:shadow-md">
            Get Started
          </button>
        </div>
      </div>
    </motion.nav>
  );
}
