"use client";

import { MapContainer, TileLayer, CircleMarker, Popup, Polyline } from 'react-leaflet';

export default function MapClient({ industries, latestMatch }: { industries: any[], latestMatch: any }) {
  const center: [number, number] = [37.7749, -122.1194]; // Bay Area center

  return (
    <div className="h-full w-full rounded-xl overflow-hidden shadow-2xl border border-neutral-800 relative z-0">
      <MapContainer center={center} zoom={9} style={{ height: '100%', width: '100%', backgroundColor: '#000000' }} zoomControl={false} attributionControl={false}>
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />
        {industries.map(ind => (
          <CircleMarker 
            key={ind.id} 
            center={[ind.lat, ind.lon]} 
            radius={4}
            pathOptions={{ 
              color: ind.role === 'producer' ? '#f43f5e' : '#3b82f6',
              fillColor: ind.role === 'producer' ? '#f43f5e' : '#3b82f6',
              fillOpacity: 1,
              weight: 1
            }}
          >
            <Popup>
              <div className="text-black p-1">
                <strong>{ind.name}</strong><br/>
                <span className="text-xs uppercase font-bold text-gray-500">{ind.role}</span>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {latestMatch && (
          <Polyline 
            positions={[
              [latestMatch.producer.lat, latestMatch.producer.lon],
              [latestMatch.consumer.lat, latestMatch.consumer.lon]
            ]} 
            pathOptions={{ color: '#10b981', weight: 4, opacity: 0.8 }} 
          />
        )}
      </MapContainer>
      
      {/* Map Legend */}
      <div className="absolute bottom-4 right-4 bg-neutral-900/80 backdrop-blur p-3 rounded-lg border border-neutral-800 flex flex-col gap-2 shadow-xl z-[1000] text-sm">
        <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-rose-500"></div> Producers</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-blue-500"></div> Consumers</div>
        {latestMatch && <div className="flex items-center gap-2"><div className="w-4 h-1 bg-emerald-500"></div> Active Match</div>}
      </div>
    </div>
  );
}
