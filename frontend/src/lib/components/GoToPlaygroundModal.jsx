import { Button } from '@headlessui/react';
import { Link } from 'react-router-dom';

const example = [
  'NebulaVision',
  'QuantumForge',
  'AetherFlow',
  'ChronoSync',
  'TitanPulse',
  'EclipseGrid',
  'CipherNest',
  'NovaPath',
  'SpectraCore',
  'ZenithTrack',
  'HorizonByte',
  'OmniLink',
  'EchoDrive',
  'OrionSphere',
  'FusionStack',
  'CelestialNode',
  'HyperVortex',
  'CyberHorizon',
];

export default function GoToPlaygroundModal({className}) {
  return (
    <section className={className}>
      <section className="row-span-2 flex flex-col items-center justify-center gap-4">
        <h1 className="text-xl font-bold underline">Playground</h1>
        <Link className="transition-color w-1/2 rounded-full border-2 border-amber-700 shadow-amber-600/50 duration-100 hover:bg-amber-700 hover:shadow active:bg-amber-800 text-center overflow-auto">
          New
        </Link>
      </section>

      <section className="row-span-2 m-2 flex flex-1 flex-col gap-1 overflow-auto rounded border-10 border-zinc-900 bg-zinc-900">
        <h1 className="sticky top-0 bg-zinc-900">
          Recent Projects <hr className="text-zinc-700" />
        </h1>
        {example.map((project, key) => {
          return (
            <Button
              className="rounded bg-zinc-800 p-1 text-sm text-zinc-500 hover:not-active:text-zinc-100"
              key={key}
            >
              {project}
            </Button>
          );
        })}
      </section>
    </section>
  );
}
