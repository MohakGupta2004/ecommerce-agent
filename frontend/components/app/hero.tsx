"use client";
import { motion } from "framer-motion";
import Image from "next/image";
import { ArrowRight, Star, CheckCircle2, Play } from "lucide-react";

interface HeroProps {
  onStartCall?: () => void;
}

export default function Hero({ onStartCall }: HeroProps) {
  return (
    <div className="border mx-8 my-3 rounded-[2.5rem] bg-linear-to-b from-gray-300 to-gray-100 p-6 lg:p-10 flex flex-col lg:flex-row items-center lg:justify-between gap-8 relative overflow-hidden h-[calc(100vh-120px)]">
      {/* Left Content */}
      <div className="flex-1 space-y-4 lg:space-y-6 z-10">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center gap-3"
        >
          <div className="w-10 h-10 rounded-full bg-black flex items-center justify-center">
            <div className="w-6 h-6 rounded-full border-2 border-white flex items-center justify-center">
              <div className="w-2 h-2 bg-white rounded-full"></div>
            </div>
          </div>
          <div>
            <p className="text-sm font-bold">20M+ User</p>
            <p className="text-sm text-gray-600">
              Read Our <span className="underline font-semibold">Success Stories</span>
            </p>
          </div>
        </motion.div>

        {/* Main Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h1
            className="text-[10rem] lg:text-[12rem] font-medium tracking-tight text-black leading-tight"
            style={{ fontFamily: "Radley, serif" }}
          >
            Grow<sup className="text-4xl lg:text-5xl">+</sup>
          </h1>
          <div className="w-full h-1 bg-black mt-3"></div>
        </motion.div>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-base lg:text-lg text-gray-700 max-w-md leading-relaxed"
        >
          Drive Sales Growth, And Harness Ai-Powered User Content — Up To 50× Faster.
        </motion.p>

        {/* Rating */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center gap-4"
        >
          <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center">
            <span className="text-xl">👤</span>
          </div>
          <div className="flex items-center gap-6">
            <div>
              <p className="text-sm font-medium text-gray-400">Loved the performance</p>
              <p className="text-sm font-bold text-gray-400">100% Satisfied</p>
            </div>
            <div className="h-8 w-px bg-gray-300"></div>
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-black" />
              <span className="font-bold text-lg text-black">4.9</span>
            </div>
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="flex flex-wrap items-center gap-4"
        >
          <button
            onClick={onStartCall}
            className="bg-black text-white px-6 py-3 rounded-full font-medium hover:bg-gray-800 transition-colors flex items-center gap-2 text-sm"
          >
            Try it Now
          </button>
          <button className="text-black px-5 py-3 rounded-full font-medium hover:bg-gray-100 transition-colors flex items-center gap-2 text-sm">
            Our Pricing
            <ArrowRight className="w-4 h-4" />
          </button>
        </motion.div>
      </div>

      {/* Right Content - Image with Cards */}
      <div className="flex-1 relative w-full lg:w-auto h-full flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="relative w-full max-w-md"
        >
          {/* Main Image Container */}
          <div className="relative w-full aspect-4/5 rounded-3xl overflow-hidden bg-linear-to-br from-orange-400 to-orange-500 max-h-[70vh]">
            <Image
              src="/sales.jpg"
              alt="Sales representative"
              fill
              className="object-cover"
              priority
            />
            
            {/* Play Button Overlay */}
            <div className="absolute inset-0 flex items-center justify-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.5, delay: 0.8 }}
                className="w-12 h-12 lg:w-16 lg:h-16 bg-white rounded-full flex items-center justify-center cursor-pointer hover:scale-110 transition-transform shadow-lg"
              >
                <Play className="w-5 h-5 lg:w-6 lg:h-6 fill-black ml-1" />
              </motion.div>
            </div>
          </div>

          {/* Floating Cards */}
          {/* Top Left - Questions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="absolute top-2 left-2 lg:top-4 lg:left-4 space-y-2"
          >
            <div className="bg-white/95 backdrop-blur-sm px-3 py-1.5 lg:px-4 lg:py-2 rounded-full shadow-lg flex items-center gap-2">
              <CheckCircle2 className="w-3 h-3 lg:w-4 lg:h-4 text-orange-500" />
              <span className="text-xs lg:text-sm font-medium">How is the fit?</span>
            </div>
            <div className="bg-white/95 backdrop-blur-sm px-3 py-1.5 lg:px-4 lg:py-2 rounded-full shadow-lg flex items-center gap-2">
              <CheckCircle2 className="w-3 h-3 lg:w-4 lg:h-4 text-blue-500" />
              <span className="text-xs lg:text-sm font-medium">Do you like the design?</span>
            </div>
          </motion.div>

          {/* Top Right - Sales Stats */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="absolute -top-2 -right-2 lg:-top-4 lg:-right-4 bg-orange-400/90 backdrop-blur-sm p-3 lg:p-4 rounded-2xl shadow-xl"
          >
            <p className="text-[10px] lg:text-xs text-white/80 mb-0.5 lg:mb-1">UP TO</p>
            <p className="text-3xl lg:text-4xl font-bold text-white mb-0.5 lg:mb-1">60%</p>
            <p className="text-[10px] lg:text-xs text-white">More sales this week</p>
          </motion.div>

          {/* Bottom Right - Product Card */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
            className="absolute -bottom-2 -right-2 lg:-bottom-4 lg:-right-4 bg-white/95 backdrop-blur-sm p-3 lg:p-4 rounded-2xl shadow-xl flex items-center gap-2 lg:gap-3 min-w-60"
          >
            <div className="w-16 h-16 lg:w-20 lg:h-20 bg-gray-100 rounded-xl overflow-hidden shrink-0">
              <Image
                src="/sales.jpg"
                alt="Nike Shoes"
                width={80}
                height={80}
                className="object-cover"
              />
            </div>
            <div>
              <p className="text-xs lg:text-sm font-semibold">Nike Shoes</p>
              <p className="text-xs lg:text-sm text-gray-600">Jordan</p>
              <p className="text-lg lg:text-xl font-bold">$849.99</p>
              <div className="flex items-center gap-1 mt-0.5 lg:mt-1">
                <Star className="w-3 h-3 fill-black" />
                <span className="text-xs lg:text-sm font-medium">4.6</span>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
