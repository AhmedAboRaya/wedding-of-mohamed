import { useState } from 'react';
import './index.css';
import Intro from './components/Intro';
import Hero from './components/Hero';
import Countdown from './components/Countdown';
import ScrollStack, { ScrollStackItem } from './components/ScrollStack';
import CommentsSection from './components/CommentsSection';
import LocationSection from './components/LocationSection';

const scrollImages = [
  '/images/photo1.jpg',
  '/images/photo2.jpg',
  '/images/photo3.jpg',
];

function App() {
  const [introComplete, setIntroComplete] = useState(false);

  return (
    <>
      {!introComplete && <Intro onComplete={() => setIntroComplete(true)} />}

      <div className={`app ${introComplete ? 'app-visible' : 'app-hidden'}`}>
        <Hero />
        <Countdown />

        <ScrollStack useWindowScroll={true}>
          {scrollImages.map((src, i) => (
            <ScrollStackItem key={i}>
              <div className="stack-card stack-card-image">
                <img src={src} alt={`Wedding moment ${i + 1}`} loading="lazy" />
              </div>
            </ScrollStackItem>
          ))}
        </ScrollStack>
        <LocationSection />
        <CommentsSection />

      </div>
    </>
  );
}

export default App;
