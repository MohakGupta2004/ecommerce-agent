"use client";
import { motion } from "framer-motion";
import Image from "next/image";
import Head from "next/head";

interface HeroProps {
  onStartCall?: () => void;
}

export default function Hero({ onStartCall }: HeroProps) {
  return (
    <>
      <header role="banner" className="relative w-full h-screen flex items-center justify-center px-4 overflow-hidden">
        <Image
          src="/dna.png"
          alt=""
          aria-hidden="true"
          width={1400}
          height={1400}
          className="absolute -right-40 -top-40 md:-right-60 md:-top-60 w-[1400px] h-[1400px] opacity-10 md:opacity-20 pointer-events-none transform -rotate-45"
        />

        <div className="relative z-10 flex flex-col items-center gap-8 px-4 text-center">
          <motion.h1
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-5xl md:text-7xl lg:text-8xl font-extrabold leading-tight tracking-tight text-gray-900"
        style={{ fontFamily: "'Vend Sans', 'VendSans', sans-serif" }}
        aria-label="Hero headline"
          >
        Revolutionizing{" "}
        <span className="inline-block p-2 rounded-3xl text-white bg-black">healthcare</span>
        <br />
        with AI and psychology
          </motion.h1>

          <div className="w-full flex justify-center">
        <button
          type="button"
          onClick={onStartCall}
          aria-label="Start call"
          className="inline-flex items-center justify-center px-7 py-3 bg-black text-white text-lg font-semibold rounded-full shadow-md hover:bg-gray-900 active:translate-y-0.5 transition-transform focus:outline-none focus-visible:ring-4 focus-visible:ring-black/20"
        >
          Start Call
        </button>
          </div>
        </div>
      </header>
    </>
  );
}
