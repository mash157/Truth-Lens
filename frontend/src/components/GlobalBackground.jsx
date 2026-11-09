/**
 * Shared TruthLens background.
 *
 * One geometry, one set of layer rules: the colour stops are themed centrally
 * through CSS classes so light and dark mode always share the same silhouette.
 * `variant` only controls presence/intensity; `embedded` renders the layer
 * inside the homepage hero instead of the application shell.
 */
export default function GlobalBackground({ variant = 'page', embedded = false }) {
  return (
    <div
      className={`global-bg global-bg--${variant}${embedded ? ' global-bg--embedded' : ''}`}
      aria-hidden="true"
    >
      <svg viewBox="0 0 1440 640" preserveAspectRatio="none" role="presentation">
        <defs>
          <linearGradient id="tlBlue" x1="0" y1="0" x2="0.9" y2="1">
            <stop offset="0" className="st-tl-blue-a" />
            <stop offset="0.55" className="st-tl-blue-b" />
            <stop offset="1" className="st-tl-blue-c" />
          </linearGradient>
          <linearGradient id="tlLav" x1="0.05" y1="0" x2="0.95" y2="1">
            <stop offset="0" className="st-tl-lav-a" />
            <stop offset="0.5" className="st-tl-lav-b" />
            <stop offset="1" className="st-tl-lav-c" />
          </linearGradient>
          <linearGradient id="tlPink" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" className="st-tl-pink-a" />
            <stop offset="1" className="st-tl-pink-b" />
          </linearGradient>
          <linearGradient id="tlBand" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" className="st-tl-band-a" />
            <stop offset="0.42" className="st-tl-band-b" />
            <stop offset="0.76" className="st-tl-band-c" />
            <stop offset="1" className="st-tl-band-d" />
          </linearGradient>
          <linearGradient id="tlGloss" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" className="st-tl-gloss-a" />
            <stop offset="1" className="st-tl-gloss-b" />
          </linearGradient>
          <linearGradient id="tlEdge" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" className="st-tl-edge-a" />
            <stop offset="0.5" className="st-tl-edge-b" />
            <stop offset="1" className="st-tl-edge-c" />
          </linearGradient>
          <linearGradient id="brWash" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" className="st-br-wash-a" />
            <stop offset="0.5" className="st-br-wash-b" />
            <stop offset="1" className="st-br-wash-c" />
          </linearGradient>
          <linearGradient id="brLav" x1="1" y1="0" x2="0.15" y2="1">
            <stop offset="0" className="st-br-lav-a" />
            <stop offset="0.55" className="st-br-lav-b" />
            <stop offset="1" className="st-br-lav-c" />
          </linearGradient>
          <linearGradient id="brSoft" x1="1" y1="0" x2="0.3" y2="1">
            <stop offset="0" className="st-br-soft-a" />
            <stop offset="1" className="st-br-soft-b" />
          </linearGradient>
          <linearGradient id="brMain" x1="1" y1="0" x2="0" y2="1">
            <stop offset="0" className="st-br-main-a" />
            <stop offset="0.45" className="st-br-main-b" />
            <stop offset="0.8" className="st-br-main-c" />
            <stop offset="1" className="st-br-main-d" />
          </linearGradient>
          <linearGradient id="brEdge" x1="1" y1="0" x2="0.2" y2="1">
            <stop offset="0" className="st-br-edge-a" />
            <stop offset="0.55" className="st-br-edge-b" />
            <stop offset="1" className="st-br-edge-c" />
          </linearGradient>
          <radialGradient id="tlBloom">
            <stop offset="0" className="st-bloom-a" />
            <stop offset="1" className="st-bloom-b" />
          </radialGradient>
          <filter id="tlBlurSm" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="10" />
          </filter>
        </defs>

        <ellipse className="tl-bloom" cx="40" cy="150" rx="340" ry="250" fill="url(#tlBloom)" />
        <path className="tl-lav" d="M0 0 H452 C404 66 348 120 284 164 C200 219 104 264 0 312 Z" />
        <path className="tl-blue" d="M0 0 H350 C306 52 260 96 208 132 C142 177 72 216 0 250 Z" />
        <ellipse className="tl-pink" cx="0" cy="352" rx="318" ry="178" fill="url(#tlPink)" />
        <path className="tl-soft" d="M396 0 C342 74 282 136 214 186 C150 233 78 274 0 308 L0 372 C88 332 172 286 246 232 C318 179 380 108 440 0 Z" />
        <path className="tl-gloss" d="M352 0 C298 68 240 124 174 170 C116 210 56 244 0 272 L0 288 C62 258 124 224 184 182 C250 136 306 78 362 0 Z" />
        <path className="tl-band" d="M300 0 C244 54 192 100 138 138 C92 170 44 199 0 222 L0 266 C58 242 114 213 166 178 C232 132 288 74 344 0 Z" />
        <path className="tl-edge-glow" d="M344 0 C288 74 232 132 166 178 C114 213 58 242 0 266" />
        <path className="tl-edge" d="M344 0 C288 74 232 132 166 178 C114 213 58 242 0 266" />

        <ellipse className="br-bloom" cx="1420" cy="470" rx="310" ry="260" fill="url(#tlBloom)" />
        <path className="br-wash" d="M1440 286 C1346 322 1252 380 1172 452 C1096 520 1042 582 1012 640 L1440 640 Z" />
        <path className="br-lav" d="M1440 352 C1350 388 1268 440 1198 506 C1140 562 1100 606 1078 640 L1440 640 Z" />
        <path className="br-low" d="M1440 566 C1400 586 1364 612 1338 640 L1440 640 Z" />
        <path className="br-soft" d="M1440 486 C1372 518 1312 566 1268 640 L1352 640 C1382 596 1410 558 1440 532 Z" />
        <path className="br-main" d="M1440 398 C1348 430 1262 482 1192 550 C1148 592 1122 620 1108 640 L1196 640 C1214 616 1238 590 1268 562 C1336 498 1396 452 1440 430 Z" />
        <path className="br-glow" d="M1440 398 C1348 430 1262 482 1192 550 C1148 592 1122 620 1108 640" />
        <path className="br-edge" d="M1440 398 C1348 430 1262 482 1192 550 C1148 592 1122 620 1108 640" />
      </svg>
    </div>
  );
}
