"use client";
import { motion } from "framer-motion";
import { Star } from "lucide-react";

interface HeroProps {
  onStartCall?: () => void;
}

export default function Hero({ onStartCall }: HeroProps) {
  return (
    <div className="relative min-h-screen pt-52 pb-12 overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute top-20 right-10 w-64 h-64 bg-rose-200/30 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 left-10 w-80 h-80 bg-orange-200/30 rounded-full blur-3xl"></div>

      <div className="relative max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center z-10">
        {/* Left Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7 }}
          className="space-y-8 z-10"
        >
          <h1 
            className="text-6xl lg:text-7xl font-normal text-gray-900 leading-tight"
            style={{ fontFamily: '"Playfair Display", serif' }}
          >
            Enjoy healthy and
            <br />
            delicious food.
          </h1>

          <p 
            className="text-gray-600 text-base leading-relaxed max-w-md"
            style={{ fontFamily: '"Inter", sans-serif' }}
          >
            Rice balls here are just like homemade. The texture is perfect. Design by Fluttertop and they have that comforting, home-cooked taste. Love them!
          </p>

          {/* Customer Review */}
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-white shadow-md">
              <div className="w-full h-full bg-gradient-to-br from-orange-400 to-rose-400"></div>
            </div>
            <div>
              <p className="font-medium text-gray-900" style={{ fontFamily: '"Inter", sans-serif' }}>
                John
              </p>
              <div className="flex gap-0.5">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-wrap gap-4 pt-4">
            <button
              onClick={onStartCall}
              className="px-8 py-3.5 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl"
              style={{ fontFamily: '"Inter", sans-serif' }}
            >
              Order now
            </button>
            <button
              className="px-8 py-3.5 bg-white text-gray-900 rounded-full font-medium hover:bg-gray-50 transition-all border border-gray-200 shadow-sm"
              style={{ fontFamily: '"Inter", sans-serif' }}
            >
              Reservation
            </button>
          </div>
        </motion.div>

        {/* Right Content - Custom Sushi Illustration */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="relative flex items-center justify-center min-h-[500px]"
        >
          {/* Rating Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="absolute top-8 right-8 rounded-2xl px-4 py-3 shadow-xl z-20 backdrop-blur-sm bg-white/90"
          >
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600 font-medium" style={{ fontFamily: '"Inter", sans-serif' }}>
                3.2k+ Rating
              </span>
              <div className="flex items-center gap-1">
                <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                <span className="font-bold text-gray-900" style={{ fontFamily: '"Inter", sans-serif' }}>
                  4.7
                </span>
              </div>
            </div>
          </motion.div>

          {/* Social Labels */}
          <div className="absolute right-4 top-1/2 -translate-y-1/2 flex flex-col gap-4 text-xs font-medium text-gray-500 z-20">
            <span className="writing-mode-vertical rotate-180" style={{ writingMode: 'vertical-rl' }}>
              INSTAGRAM
            </span>
            <span className="writing-mode-vertical rotate-180" style={{ writingMode: 'vertical-rl' }}>
              WHATSAPP
            </span>
            <span className="writing-mode-vertical rotate-180" style={{ writingMode: 'vertical-rl' }}>
              FACEBOOK
            </span>
          </div>

          {/* Custom Sushi Illustration */}
          <div className="relative w-full max-w-lg aspect-square">
            <motion.div
              animate={{ rotate: [0, 2, 0, -2, 0] }}
              transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
              className="relative w-full h-full"
            >
              {/* Sushi Roll */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64">
                {/* Main Sushi Body */}
                <div className="relative w-full h-full rounded-full bg-white shadow-2xl overflow-hidden">
                  {/* Rice base */}
                  <div className="absolute inset-0 bg-gradient-to-br from-gray-50 to-gray-100"></div>
                  
                  {/* Seaweed wrap */}
                  <div className="absolute inset-0 border-[16px] border-gray-800 rounded-full"></div>
                  
                  {/* Rice texture dots */}
                  {[...Array(40)].map((_, i) => (
                    <div
                      key={i}
                      className="absolute w-1 h-1 bg-white/60 rounded-full"
                      style={{
                        top: `${20 + Math.random() * 60}%`,
                        left: `${20 + Math.random() * 60}%`,
                      }}
                    />
                  ))}
                  
                  {/* Salmon/Fish - top left */}
                  <div className="absolute top-16 left-12 w-16 h-12 bg-gradient-to-br from-orange-400 to-rose-500 rounded-lg transform -rotate-12 shadow-lg"></div>
                  
                  {/* Avocado - bottom right */}
                  <div className="absolute bottom-20 right-14 w-14 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-full shadow-lg"></div>
                  
                  {/* Cucumber - top right */}
                  <div className="absolute top-20 right-16 w-10 h-10 bg-gradient-to-br from-green-300 to-green-500 rounded-full shadow-md"></div>
                  
                  {/* Orange roe/tobiko details */}
                  <div className="absolute top-24 left-20 w-3 h-3 bg-orange-500 rounded-full shadow-sm"></div>
                  <div className="absolute top-28 left-24 w-2 h-2 bg-orange-600 rounded-full"></div>
                  <div className="absolute bottom-24 left-24 w-2.5 h-2.5 bg-red-500 rounded-full shadow-sm"></div>
                </div>
              </div>

              {/* Chopsticks */}
              <motion.div
                animate={{ rotate: [0, -2, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
                className="absolute top-0 right-0 w-96 h-96"
              >
                {/* Chopstick 1 */}
                <div className="absolute top-1/4 right-1/4 w-[280px] h-2 bg-gradient-to-r from-amber-800 to-amber-600 rounded-full transform rotate-[25deg] shadow-xl origin-right">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                </div>
                
                {/* Chopstick 2 */}
                <div className="absolute top-1/3 right-1/4 w-[280px] h-2 bg-gradient-to-r from-amber-900 to-amber-700 rounded-full transform rotate-[35deg] shadow-xl origin-right">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"></div>
                </div>
              </motion.div>

              {/* Floating garnish elements */}
              <motion.div
                animate={{ y: [0, -10, 0], rotate: [0, 5, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="absolute top-12 left-12 w-8 h-8 bg-gradient-to-br from-red-400 to-red-600 rounded-sm transform rotate-45 shadow-lg"
              />
              <motion.div
                animate={{ y: [0, 10, 0], x: [0, 5, 0] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 1 }}
                className="absolute bottom-16 left-20 w-6 h-6 bg-gradient-to-br from-green-400 to-green-600 rounded-full shadow-md"
              />
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
