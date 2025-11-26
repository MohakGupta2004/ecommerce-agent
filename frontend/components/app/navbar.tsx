"use client";
import Head from "next/head";
import { motion } from "framer-motion";

export default function Navbar() {
  const navlinks = [
    { name: "Product", href: "/product" },
    { name: "Solutions", href: "/solutions" },
    { name: "Pricing", href: "/pricing" },
    { name: "Developers", href: "/developers" }
  ]
  return (
   <>
   <div className="flex justify-between items-center px-6 py-4 bg-white border-b border-gray-200 mx-10 rounded-[2.5rem] mt-3">
    {/* Logo and Brand */}
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 bg-black rounded-md flex items-center justify-center">
        <div className="w-5 h-5 rounded-sm border-2 border-white flex items-center justify-center">
          <div className="w-2 h-2 bg-white rounded-sm"></div>
        </div>
      </div>
      <span className="text-black font-medium text-sm">Zerodha Sales</span>
    </div>
    
    {/* Navigation Links */}
    <nav className="hidden md:flex items-center gap-8">
      {navlinks.map((link) => (
        <a 
          key={link.name} 
          href={link.href} 
          className="text-black text-sm font-medium hover:text-gray-600 transition-colors"
        >
          {link.name}
        </a>
      ))}
    </nav>
    
    {/* Right Side Buttons */}
    <div className="flex items-center gap-4">
      <button className="text-black text-sm font-medium hover:text-gray-600 transition-colors">
        Log in
      </button>
      <span className="w-px h-6 bg-gray-300"></span>
      <button className="border-2 border-black text-black px-6 py-2.5 rounded-full text-sm font-medium hover:bg-black hover:text-white transition-colors">
        Get it Now — It's Free
      </button>
    </div>
   </div>
   </> 
  );
}
