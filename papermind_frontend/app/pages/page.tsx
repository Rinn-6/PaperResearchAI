"use client";

import { useState } from "react";
import axios from "axios";
import { endpoints } from "../lib/api";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [paperId, setPaperId] = useState<number | null>(null);
  const [similarPapers, setSimilarPapers] = useState<string[]>([]);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(endpoints.analyze, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setData(res.data);
      setPaperId(res.data.paper_id);
      setSimilarPapers([]);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchSimilar = async () => {
    if (!paperId) return;

    try {
      const res = await axios.get(endpoints.similarPapers, {
        params: { paper_id: paperId },
      });
      setSimilarPapers(res.data.similar_titles || []);
    } catch (err) {
      console.error("Fetching similar papers failed:", err);
    }
  };

  return (
    <main className="min-h-screen p-6 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">AI Research Assistant</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>

      {data && (
        <div className="mt-6 bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold">Summary</h2>
          <p className="mt-2">{data.summary}</p>

          <h3 className="text-lg font-semibold mt-4">Insights</h3>
          <p className="mt-2">{data.insights}</p>

          <h3 className="text-lg font-semibold mt-4">Citation</h3>
          <p className="mt-2">{data.citation}</p>

          <h3 className="text-lg font-semibold mt-4">Named Entities</h3>
          <ul className="list-disc pl-6 mt-2">
            {data.named_entities?.map(([text, label]: [string, string], i: number) => (
              <li key={i}>
                <strong>{label}</strong>: {text}
              </li>
            ))}
          </ul>
        </div>
      )}

      {paperId && (
        <button
          onClick={handleFetchSimilar}
          className="mt-6 bg-green-600 text-white px-4 py-2 rounded"
        >
          Find Similar Papers
        </button>
      )}

      {similarPapers.length > 0 && (
        <div className="mt-6 bg-white p-4 rounded shadow">
          <h3 className="text-xl font-semibold mb-2">Similar Papers</h3>
          <ul className="list-disc pl-6">
            {similarPapers.map((title, i) => (
              <li key={i}>{title}</li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
