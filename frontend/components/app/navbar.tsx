"use client";
import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 px-10 py-5 text-gray-600">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <motion.div
          initial={{ opacity: 0, y: -6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-2xl font-extrabold text-black cursor-pointer"
        >
          genomic
        </motion.div>

        <motion.ul
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="flex gap-14 font-medium text-lg"
        >
          <li className="cursor-pointer hover:text-black">For partners</li>
          <li className="cursor-pointer hover:text-black">For investors</li>
        </motion.ul>
        <motion.ul
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="flex gap-14 font-medium text-lg"
        >
          <li className="cursor-pointer hover:text-black bg-gray-200 p-3 rounded-3xl w-full px-7 flex items-center gap-3">
            <svg
              aria-hidden="true"
              className="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M12 5v14M5 12h14" />
            </svg>
            <span className="select-none">menu</span>
          </li>
        </motion.ul>


        
      </div>
    </nav>
  );
}
