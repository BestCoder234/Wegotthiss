import { useState, useEffect } from 'react';

export default function TestAPI() {
  const [result, setResult] = useState<string>('Loading...');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const testAPI = async () => {
      try {
        const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        console.log('Testing API at:', API);
        
        const response = await fetch(`${API}/screener?limit=2`);
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        setResult(JSON.stringify(data, null, 2));
      } catch (err) {
        console.error('API test error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
        setResult('Error occurred');
      }
    };

    testAPI();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">API Test</h1>
        
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <div className="text-red-800">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}
        
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">API Response:</h2>
          <pre className="bg-gray-100 p-4 rounded-lg overflow-auto text-sm">
            {result}
          </pre>
        </div>
      </div>
    </div>
  );
} 