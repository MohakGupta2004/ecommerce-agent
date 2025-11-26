"use client";
import { motion } from "framer-motion";
import { ArrowRight, Shield, Sparkles } from "lucide-react";

interface HeroProps {
  onStartCall?: () => void;
}

export default function Hero({ onStartCall }: HeroProps) {
  return (
    <div className="relative min-h-[calc(100vh-100px)] flex flex-col lg:flex-row items-center justify-center max-w-7xl mx-auto px-6 py-12 lg:py-0">
      
      {/* Left Content */}
      <div className="flex-1 z-10 space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{ fontFamily: '"Orbitron", "Roboto Mono", monospace', letterSpacing: '0.06em' }}
        >
          <h1 className="text-5xl lg:text-7xl font-semibold text-white leading-[1.1] tracking-tight">
            <span className="whitespace-nowrap">Report Your Fraud</span>
            <br />
            <span className="whitespace-nowrap text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
              Against Fraudsters
            </span>
          </h1>
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-gray-400 text-lg max-w-xl leading-relaxed font-mono"
          style={{ fontFamily: '"Orbitron", "Roboto Mono", monospace', letterSpacing: '0.02em' }}
        >
          Report fraudulent activities with ease using our intuitive platform. Help us combat fraud and create a safer environment for everyone.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex flex-col sm:flex-row items-start sm:items-center gap-4"
        >
          <button
            onClick={onStartCall}
            className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-8 py-3.5 rounded-full font-medium transition-all shadow-[0_0_20px_-5px_rgba(37,99,235,0.5)] hover:shadow-[0_0_25px_-5px_rgba(37,99,235,0.6)]"
          >
            Report here 
          </button>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center gap-2 text-sm text-gray-500 pt-4"
        >
          <Sparkles className="w-4 h-4 text-blue-500" />
          <span>Beta release date June 30th, 2023</span>
        </motion.div>
      </div>

      {/* Right Content - Abstract Visuals */}
      <div className="flex-1 w-full h-[500px] relative flex items-center justify-center mt-12 lg:mt-0">
        {/* Glowing Orb Effect */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[300px] bg-blue-600/20 rounded-full blur-[100px]"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200px] h-[200px] bg-purple-600/20 rounded-full blur-[80px] mix-blend-screen"></div>

        {/* Abstract Cube/Structure Representation */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="relative w-full max-w-md aspect-square"
        >
          {/* Wireframe Box Container */}
          <div className="absolute inset-0 border border-white/5 rounded-3xl transform rotate-6 scale-90"></div>
          <div className="absolute inset-0 border border-white/5 rounded-3xl transform -rotate-3 scale-95"></div>
          
          {/* Main Glowing Element */}
          <div className="absolute inset-10 bg-gradient-to-br from-blue-900/40 to-purple-900/40 backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl flex items-center justify-center overflow-hidden">
            {/* Inner Glow */}
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-blue-500/10 to-transparent"></div>
            
            {/* Sphere */}
            <div className="relative w-32 h-32 lg:w-48 lg:h-48 rounded-full bg-gradient-to-br from-blue-400 to-purple-600 shadow-[0_0_50px_rgba(59,130,246,0.5)] flex items-center justify-center">
               <div className="absolute inset-0 bg-white/20 rounded-full blur-md"></div>
               <div className="w-full h-full rounded-full bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>

            {/* Floating Elements */}
            <motion.div 
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              className="absolute top-10 right-10 w-3 h-3 bg-white rounded-full shadow-[0_0_10px_white]"
            />
            <motion.div 
              animate={{ y: [0, 15, 0] }}
              transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
              className="absolute bottom-20 left-10 w-2 h-2 bg-blue-400 rounded-full shadow-[0_0_10px_#60a5fa]"
            />
          </div>

          {/* Decorative Lines */}
          <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-30" viewBox="0 0 400 400">
            <path d="M0,200 Q100,100 200,200 T400,200" fill="none" stroke="url(#grad1)" strokeWidth="1" />
            <path d="M0,250 Q150,150 250,250 T400,250" fill="none" stroke="url(#grad1)" strokeWidth="1" />
            <defs>
              <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="transparent" />
                <stop offset="50%" stopColor="rgba(255,255,255,0.5)" />
                <stop offset="100%" stopColor="transparent" />
              </linearGradient>
            </defs>
          </svg>
        </motion.div>
      </div>
    </div>
  );
}
