"use client";

import { useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL!;

export default function Home() {
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      setError("");
      setLoading(true);

      const res = await axios.post(
        `${BACKEND_URL}/process`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setFiles(res.data.files);
    } catch (err: unknown) {
      console.error(err);
      setError("Failed to process CSV. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center py-16 px-6">
      <h1 className="text-3xl font-semibold mb-6">
        CSV Bias & SMOTE Analyzer
      </h1>

      <input
        type="file"
        accept=".csv"
        onChange={handleUpload}
        className="mb-6"
      />

      {loading && (
        <p className="text-lg">Processing dataset...</p>
      )}

      {error && (
        <p className="text-red-600">{error}</p>
      )}

      {files.length > 0 && (
        <div className="mt-8 w-full max-w-lg">
          <h2 className="text-xl font-semibold mb-4">
            Generated Files
          </h2>

          <ul className="space-y-2">
            {files.map((url, i) => (
              <li key={i}>
                <a
                  href={`${BACKEND_URL}${url}`}
                  className="text-blue-600 underline"
                  target="_blank"
                >
                  Download {url.split("/").pop()}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
