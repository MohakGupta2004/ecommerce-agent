"use client";
import { motion } from "framer-motion";
import { Star } from "lucide-react";

interface HeroProps {
  onStartCall?: () => void;
}

export default function Hero({ onStartCall }: HeroProps) {
  return (
    <div className="relative h-screen pt-20 pb-6 overflow-hidden bg-gradient-to-b from-white to-gray-50 flex items-center">
      <div className="max-w-7xl mx-auto px-6 w-full">
        {/* Announcement Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex items-center justify-center gap-3 mb-4"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white border border-gray-200 rounded-full shadow-sm">
            <span className="text-sm">⚡</span>
            <span className="text-sm font-medium text-gray-900">
              Voice AI Raises $32.8M to Fuel-up
            </span>
            <div className="w-5 h-5 bg-black rounded-full flex items-center justify-center">
              <span className="text-white text-xs">→</span>
            </div>
          </div>
        </motion.div>

        {/* Main Headline */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          className="text-center mb-4"
        >
          <h1
            className="text-5xl md:text-6xl lg:text-7xl font-normal text-gray-900 leading-tight mb-3"
            style={{ fontFamily: '"DM Serif Text", serif' }}
          >
            AI-Powered Shopping to
            <br />
            Get Everything By Command
          </h1>
          <p className="text-base text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Command your shopping with AI-powered automation. Get everything you need at ease.
          </p>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="flex items-center justify-center gap-4 mb-6"
        >
          <button
            onClick={onStartCall}
            className="px-6 py-2.5 bg-black text-white rounded-full font-medium hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl text-sm"
          >
            Try it out
          </button>
        </motion.div>

        {/* Product Showcase Cards */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="grid md:grid-cols-2 gap-4 max-w-6xl mx-auto"
        >
          {/* Left Card - Product Image with Stats */}
          <div className="relative rounded-2xl overflow-hidden shadow-xl group">
            <div className="relative h-[280px]">
              <img
                src="/picture1.jpg"
                alt="Product showcase"
                className="w-full h-full object-cover"
              />

              {/* Gradient Overlay */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>

              {/* Stats Badge - Top Left */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 1 }}
                className="absolute top-4 left-4 bg-yellow-300 rounded-xl px-3 py-2 shadow-lg"
              >
                <div className="text-xs text-gray-700 font-medium">Total Sales</div>
                <div className="text-xl font-bold text-gray-900">$4.7k</div>
                <div className="text-xs text-green-700 font-medium">↑ Increased 7%</div>
              </motion.div>

              {/* Engagement Badge - Bottom */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 1.2 }}
                className="absolute bottom-4 left-4 bg-white rounded-full px-3 py-1.5 shadow-lg flex items-center gap-2"
              >
                <div className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
                  <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                    <path d="M8 2L9.5 5.5L13 6L10.5 8.5L11 12L8 10L5 12L5.5 8.5L3 6L6.5 5.5L8 2Z" />
                  </svg>
                </div>
                <span className="text-xs font-medium text-gray-900">Love it! Going to try it out</span>
              </motion.div>

              {/* Conversion Chart - Top Right */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 1.4 }}
                className="absolute top-4 right-4 bg-white/95 backdrop-blur-sm rounded-xl p-3 shadow-xl"
              >
                <div className="text-xs text-gray-600 mb-2">Funnel conversion</div>
                <div className="flex gap-2 items-end">
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-14 bg-pink-300 rounded-lg mb-1"></div>
                    <span className="text-xs font-medium">82%</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="w-12 h-20 bg-teal-400 rounded-lg mb-1"></div>
                    <span className="text-xs font-medium">76.6%</span>
                  </div>
                </div>
              </motion.div>

              {/* Live Watching Badge */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 1.6 }}
                className="absolute bottom-4 right-4 bg-emerald-500 rounded-full px-2.5 py-1 shadow-lg flex items-center gap-1.5"
              >
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div>
                <span className="text-xs font-medium text-white">2.5k live</span>
              </motion.div>
            </div>
          </div>

          {/* Right Card - Analytics Dashboard */}
          <div className="relative rounded-2xl overflow-hidden shadow-xl bg-gradient-to-br from-gray-900 to-gray-800 p-5">
            <h2 className="text-2xl font-semibold text-white mb-4">
              Get Analytics
              <br />
              Over all Products
            </h2>

            {/* Analytics Card */}
            <div className="bg-white rounded-xl p-4 shadow-xl">
              <div className="flex items-center gap-2 mb-4">
                <img
                  src="/picture2.jpg"
                  alt="Product"
                  className="w-10 h-10 rounded-lg object-cover"
                />
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 text-sm">Product visits</h3>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs text-gray-600 mb-3">
                <span className="flex items-center gap-1">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M2 4h12v8H2z" />
                  </svg>
                  Shoppable Videos
                </span>
                <span className="mx-1">vs</span>
                <span className="flex items-center gap-1">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                    <circle cx="8" cy="8" r="6" />
                  </svg>
                  Nike Burner
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-2xl font-bold text-gray-900">104,887</div>
                  <div className="text-xs text-gray-500 flex items-center gap-1">
                    <svg width="10" height="10" viewBox="0 0 12 12" fill="currentColor" className="text-gray-400">
                      <path d="M2 2h8v8H2z" />
                    </svg>
                    Product views
                  </div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">3,216</div>
                  <div className="text-xs text-gray-500 flex items-center gap-1">
                    <Star className="w-2.5 h-2.5 text-gray-400" />
                    Product conversion
                  </div>
                </div>
              </div>

              <div className="flex gap-2">
                <button className="flex-1 px-3 py-1.5 bg-black text-white rounded-full text-xs font-medium hover:bg-gray-800 transition-colors">
                  Session replay
                </button>
                <button className="px-3 py-1.5 bg-gray-100 text-gray-900 rounded-full text-xs font-medium hover:bg-gray-200 transition-colors whitespace-nowrap">
                  Save segment
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
