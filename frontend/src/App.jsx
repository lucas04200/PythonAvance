import React, { useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import polyline from '@mapbox/polyline';

function App() {
  const [path, setPath] = useState([]);
  const [start, setStart] = useState({ lat: 48.8566, lon: 2.3522 });
  const [end, setEnd] = useState({ lat: 48.858844, lon: 2.294351 });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/route`, {
        start_lat: start.lat,
        start_lon: start.lon,
        end_lat: end.lat,
        end_lon: end.lon
      });
      const decodedPath = polyline.decode(response.data.path);
      setPath(decodedPath.map(coord => [coord[0], coord[1]]));
    } catch (error) {
      console.error("Error fetching route:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Start Latitude: </label>
          <input type="number" value={start.lat} onChange={(e) => setStart({ ...start, lat: e.target.value })} />
        </div>
        <div>
          <label>Start Longitude: </label>
          <input type="number" value={start.lon} onChange={(e) => setStart({ ...start, lon: e.target.value })} />
        </div>
        <div>
          <label>End Latitude: </label>
          <input type="number" value={end.lat} onChange={(e) => setEnd({ ...end, lat: e.target.value })} />
        </div>
        <div>
          <label>End Longitude: </label>
          <input type="number" value={end.lon} onChange={(e) => setEnd({ ...end, lon: e.target.value })} />
        </div>
        <button type="submit">Get Route</button>
      </form>
      <MapContainer center={[start.lat, start.lon]} zoom={13} style={{ height: "600px", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        {path.length > 0 && <Polyline positions={path} color="blue" />}
      </MapContainer>
    </div>
  );
}

export default App;