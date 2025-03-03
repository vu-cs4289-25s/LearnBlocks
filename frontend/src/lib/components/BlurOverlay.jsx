export default function BlurOverlay({ open, children }) {
  return (
    <div className={`absolute top-0 left-0 h-screen w-screen backdrop-blur-sm ${open? '': 'hidden'}`}>
      {children}
    </div>
  );
}
