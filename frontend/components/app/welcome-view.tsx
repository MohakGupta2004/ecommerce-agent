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
      className='relative h-screen overflow-auto bg-gradient-to-br from-rose-50 via-orange-50 to-yellow-50'
    >
      <Navbar/>
      <Hero onStartCall={onStartCall}/>
    </div>
  );
};
