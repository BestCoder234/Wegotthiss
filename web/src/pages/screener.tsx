import React, { useState, useEffect } from 'react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getPaginationRowModel,
} from '@tanstack/react-table';
import { Slider } from '@/components/ui/slider';

// Define the data type
interface StockData {
  symbol: string;
  close: number;
  pe: number;
  pb: number;
  eps: number;
  book_value: number;
}

const columnHelper = createColumnHelper<StockData>();

const columns = [
  columnHelper.accessor('symbol', {
    header: 'Symbol',
    cell: (info) => (
      <div className="font-semibold text-gray-900">{info.getValue()}</div>
    ),
  }),
  columnHelper.accessor('close', {
    header: 'Close Price',
    cell: (info) => (
      <div className="text-right">₹{info.getValue().toLocaleString()}</div>
    ),
  }),
  columnHelper.accessor('pe', {
    header: 'P/E Ratio',
    cell: (info) => (
      <div className={`text-right font-medium ${
        info.getValue() < 15 ? 'text-green-600' : 
        info.getValue() > 25 ? 'text-red-600' : 'text-gray-600'
      }`}>
        {info.getValue().toFixed(2)}
      </div>
    ),
  }),
  columnHelper.accessor('pb', {
    header: 'P/B Ratio',
    cell: (info) => (
      <div className={`text-right font-medium ${
        info.getValue() < 1 ? 'text-green-600' : 
        info.getValue() > 3 ? 'text-red-600' : 'text-gray-600'
      }`}>
        {info.getValue().toFixed(2)}
      </div>
    ),
  }),
];

export default function ScreenerPage() {
  const [rows, setRows] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Filter states
  const [pe, setPe] = useState<number[]>([25]);
  const [pb, setPb] = useState<number[]>([3]);
  
  // Pagination states
  const [offset, setOffset] = useState(0);
  const [limit] = useState(50);

  // Fetch data function
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString(),
      });
      
      if (pe[0] !== 25) {
        params.append('pe', pe[0].toString());
      }
      
      if (pb[0] !== 3) {
        params.append('pb', pb[0].toString());
      }
      
      console.log('🔍 Fetching from API:', `${API}/screener?${params}`);
      
      const response = await fetch(`${API}/screener?${params}`);
      console.log('📡 Response status:', response.status);
      console.log('📡 Response headers:', Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('📊 Received data:', result);
      setRows(result);
      
    } catch (err) {
      console.error('❌ Error fetching data:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount and when filters/pagination change
  useEffect(() => {
    fetchData();
  }, [pe, pb, offset]);

  // Table instance
  const table = useReactTable({
    data: rows,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    state: {
      pagination: {
        pageIndex: 0,
        pageSize: limit,
      },
    },
  });

  const handlePrevious = () => {
    setOffset(Math.max(0, offset - limit));
  };

  const handleNext = () => {
    setOffset(offset + limit);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Stock Screener
          </h1>
          <p className="text-gray-600">
            Filter stocks by P/E and P/B ratios
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* P/E Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum P/E Ratio: {pe[0]}
              </label>
              <Slider
                value={pe}
                onValueChange={setPe}
                max={50}
                min={0}
                step={1}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>50</span>
              </div>
            </div>

            {/* P/B Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum P/B Ratio: {pb[0]}
              </label>
              <Slider
                value={pb}
                onValueChange={setPb}
                max={10}
                min={0}
                step={0.1}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>10</span>
              </div>
            </div>
          </div>
        </div>

        {/* Results Summary */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Showing {rows.length} stocks
              {pe[0] !== 25 && ` with P/E ≤ ${pe[0]}`}
              {pb[0] !== 3 && ` and P/B ≤ ${pb[0]}`}
            </div>
            <div className="flex items-center gap-2">
              {loading && (
                <div className="text-sm text-blue-600">
                  Loading...
                </div>
              )}
              <button
                onClick={fetchData}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Test API
              </button>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="text-red-800">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {/* Table */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                {table.getHeaderGroups().map(headerGroup => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map(header => (
                      <th
                        key={header.id}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {table.getRowModel().rows.map(row => (
                  <tr key={row.id} className="hover:bg-gray-50">
                    {row.getVisibleCells().map(cell => (
                      <td
                        key={cell.id}
                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                      >
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Empty State */}
          {!loading && rows.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-500">
                No stocks found matching your criteria.
              </div>
            </div>
          )}
        </div>

        {/* Pagination */}
        <div className="bg-white rounded-lg shadow-sm p-4 mt-6">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Showing {offset + 1}-{offset + rows.length} of results
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handlePrevious}
                disabled={offset === 0}
                className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={handleNext}
                disabled={rows.length < limit}
                className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 