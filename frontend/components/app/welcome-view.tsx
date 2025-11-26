import Hero from './hero';
import Navbar from './navbar';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div 
      ref={ref} 
      className='h-screen overflow-hidden'
      style={{
        backgroundColor: '#030305',
        backgroundImage: `
          radial-gradient(circle at 0% 0%, rgba(56, 27, 105, 0.4) 0%, transparent 50%),
          radial-gradient(circle at 100% 0%, rgba(20, 20, 50, 0.3) 0%, transparent 50%),
          radial-gradient(circle at 80% 50%, rgba(60, 20, 120, 0.15) 0%, transparent 50%)
        `,
      }}
    >
      <Navbar/>
      <Hero onStartCall={onStartCall}/>
    </div>
  );
};
