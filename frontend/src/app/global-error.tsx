"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Global Error Caught:", error);
  }, [error]);

  return (
    <html>
      <body>
        <div style={{ padding: 20 }}>
          <h2>Global App Error</h2>
          <p style={{ color: "red" }}>{error.message}</p>
          <pre>{error.stack}</pre>
          <button onClick={() => reset()}>Try Again</button>
        </div>
      </body>
    </html>
  );
}
