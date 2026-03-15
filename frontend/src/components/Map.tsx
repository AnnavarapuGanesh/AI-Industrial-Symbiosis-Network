"use client";
import dynamic from 'next/dynamic';

const MapClient = dynamic(() => import('./MapClient'), {
  ssr: false,
  loading: () => <div className="h-full w-full bg-neutral-900 border border-neutral-800 rounded-xl flex items-center justify-center animate-pulse text-emerald-500">Initializing Geospacial Mapping...</div>
});

export default function Map(props: any) {
  return <MapClient {...props} />
}
