"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <pre className="bg-neutral-900 p-4 rounded text-red-400 max-w-2xl overflow-auto text-xs whitespace-pre-wrap">{error.message}</pre>
      <button
        className="mt-4 px-4 py-2 bg-emerald-500 text-black font-bold rounded"
        onClick={() => reset()}
      >
        Try again
      </button>
    </div>
  );
}
