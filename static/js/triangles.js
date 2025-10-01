// 3D triangles, CodePen-like flight
document.addEventListener('DOMContentLoaded', () => {
    const stage = document.getElementById('tri-wrap');
    if (!stage) return;
  
    // clear on hot reload
    stage.innerHTML = '';
  
    // tune these to taste
    const COUNT = 120;          // how many triangles (the pen uses ~200)
    const DURATION = 10;        // seconds per loop
    const SIZE_MIN = 6;         // px
    const SIZE_MAX = 48;        // px
    const SPREAD_X = 1000;      // px range from center on X at the "near" frame
    const SPREAD_Y = 1000;      // px range from center on Y at the "near" frame
  
    for (let i = 0; i < COUNT; i++) {
      const tri = document.createElement('div');
      tri.className = 'tri';
  
      // random size → border-bottom defines the visible triangle
      const size = randInt(SIZE_MIN, SIZE_MAX);
      // grayscale shade similar to pen
      const light = randInt(55, 90);
  
      tri.style.borderLeft   = `${size}px solid transparent`;
      tri.style.borderRight  = `${size}px solid transparent`;
      tri.style.borderBottom = `${Math.round(size * 1.6)}px solid hsl(0 0% ${light}%)`;
  
      // random rotation and a "near" XY position (when Z is 1000px)
      tri.style.setProperty('--rot', randInt(0, 359));
      tri.style.setProperty('--tx',  `${randInt(-SPREAD_X/2, SPREAD_X/2)}px`);
      tri.style.setProperty('--ty',  `${randInt(-SPREAD_Y/2, SPREAD_Y/2)}px`);
  
      // shared time but offset each instance so the field looks continuous
      tri.style.setProperty('--time',  `${DURATION}s`);
      tri.style.setProperty('--delay', (i * (DURATION / COUNT)).toFixed(3) + 's');
  
      stage.appendChild(tri);
    }
  
    console.debug('[tri-3d] created:', stage.children.length, 'triangles');
  
    function randInt(min, max){ return Math.floor(Math.random() * (max - min + 1)) + min; }
  });
  