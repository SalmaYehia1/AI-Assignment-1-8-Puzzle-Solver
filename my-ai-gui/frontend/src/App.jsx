import React, { useState, useEffect, useMemo } from "react";

/* ----------------- Configuration (same design) ----------------- */
const GOAL_STATE = "012345678";
const MAX_IDDFS_DEPTH = 31;
const TILE_SIZE_CLASS = "w-20 h-20 sm:w-24 sm:h-24 md:w-28 md:h-28";

/* ----------------- Board component (identical style) --------------- */
const Board = ({ boardState }) => {
  const tiles = useMemo(() => boardState.split(""), [boardState]);

  return (
    <div className="grid grid-cols-3 gap-2 p-2 bg-gray-700 rounded-lg shadow-inner">
      {tiles.map((tile, index) => (
        <div
          key={index}
          className={`
            ${TILE_SIZE_CLASS}
            flex items-center justify-center 
            text-3xl sm:text-4xl md:text-5xl font-bold 
            rounded-md transition-all duration-300
            ${
              tile === "0"
                ? "bg-gray-800 shadow-inner"
                : "bg-blue-500 text-white shadow-md"
            }
          `}
        >
          {tile !== "0" && tile}
        </div>
      ))}
    </div>
  );
};

/* ----------------- Helper: client-side input validation -------------- */
const validateInput = (input) => {
  if (!input) return "Input required.";
  const cleaned = input.replace(/\s+/g, "");
  if (cleaned.length !== 9) return "Input must be 9 characters long (0-8).";
  const digits = new Set(cleaned.split(""));
  if (digits.size !== 9) return "Input must contain all digits 0-8 exactly once.";
  for (let i = 0; i < 9; i++) {
    if (!digits.has(String(i))) return `Missing digit: ${i}`;
  }
  return null;
};

/* ----------------- Main App ----------------- */
export default function App() {
  const [initialState, setInitialState] = useState("867254301");
  const [boardState, setBoardState] = useState("867254301");
  const [algorithm, setAlgorithm] = useState("astar-manhattan");
  const [solution, setSolution] = useState(null); 
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (solution?.path) setBoardState(solution.path[currentStep]);
  }, [currentStep, solution]);

  const handleSolve = async () => {
    const cleaned = initialState.replace(/\s+/g, "");
    const err = validateInput(cleaned);
    if (err) {
      setMessage(err);
      return;
    }

    setIsLoading(true);
    setSolution(null);
    setMessage("");
    setBoardState(cleaned);
    setCurrentStep(0);

    try {
      const res = await fetch("http://127.0.0.1:5000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: cleaned, algorithm }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Server returned ${res.status}`);
      }

      const data = await res.json();
      if (!data || !Array.isArray(data.path)) {
        throw new Error("Invalid response from server");
      }

      setSolution({
        path: data.path,
        cost: data.cost ?? data.path.length - 1,
        nodesExpanded: data.nodesExpanded ?? 0,
        time: data.time ?? 0,
        depth: data.depth,
      });
      setMessage(`Solution found in ${(data.time ?? 0).toFixed(4)}s`);
    } catch (err) {
      console.error("Solve error:", err);
      setMessage(`Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    const defaultState = "867254301";
    setInitialState(defaultState);
    setBoardState(defaultState);
    setAlgorithm("astar-manhattan");
    setSolution(null);
    setIsLoading(false);
    setMessage("");
    setCurrentStep(0);
  };

  const handleSliderChange = (e) => {
    setCurrentStep(Number(e.target.value));
  };

  const handleStep = (dir) => {
    if (!solution?.path) return;
    setCurrentStep((prev) => {
      const next = prev + dir;
      if (next < 0) return 0;
      if (next >= solution.path.length) return solution.path.length - 1;
      return next;
    });
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center text-blue-400 mb-8">
          8-Puzzle Solver
        </h1>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left controls */}
          <div className="w-full lg:w-1/3 bg-gray-800 p-6 rounded-2xl shadow-xl flex-shrink-0">
            <div className="space-y-6">
              <div>
                <label htmlFor="initialState" className="block text-sm font-medium text-gray-300 mb-1">
                  Initial State (0-8)
                </label>
                <input
                  type="text"
                  id="initialState"
                  value={initialState}
                  onChange={(e) => setInitialState(e.target.value)}
                  maxLength={17}
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., 867254301 or 8 6 7 2 5 4 3 0 1"
                  disabled={isLoading}
                />
              </div>

              <div>
                <label htmlFor="algorithm" className="block text-sm font-medium text-gray-300 mb-1">
                  Algorithm
                </label>
                <select
                  id="algorithm"
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg shadow-inner focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  disabled={isLoading}
                >
                  <option value="astar-manhattan">A* (Manhattan)</option>
                  <option value="astar-euclidean">A* (Euclidean)</option>
                  <option value="bfs">Breadth-First Search (BFS)</option>
                  <option value="iddfs">Iterative Deepening (IDDFS)</option>
                  <option value="dfs">Depth-First Search (DFS)</option>
                </select>
                {algorithm === "dfs" && (
                  <p className="text-xs text-yellow-400 mt-1">Warning: DFS may be slow or freeze the browser.</p>
                )}
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={handleSolve}
                  disabled={isLoading}
                  className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200 disabled:bg-gray-600 disabled:cursor-not-allowed"
                >
                  {isLoading ? "Solving..." : "Solve"}
                </button>
                <button
                  onClick={handleReset}
                  disabled={isLoading}
                  className="flex-1 px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition duration-200 disabled:opacity-50"
                >
                  Reset
                </button>
              </div>

              <div className="pt-6 border-t border-gray-700">
                <h3 className="text-lg font-semibold text-gray-200 mb-3">Results</h3>
                {isLoading && (
                  <div className="flex items-center gap-3">
                    <div className="w-5 h-5 border-t-2 border-b-2 border-blue-400 rounded-full animate-spin" />
                    <span className="text-gray-300">Searching...</span>
                  </div>
                )}
                {message && (
                  <p className={`text-sm ${solution?.path ? "text-green-400" : "text-yellow-400"}`}>{message}</p>
                )}
                {solution && (
                  <div className="space-y-2 mt-3 text-sm text-gray-300">
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-400">Path Cost (Moves):</span>
                      <span className="font-mono text-blue-300">{solution.cost}</span>
                    </div>
                    {solution.depth !== undefined && (
                      <div className="flex justify-between">
                        <span className="font-medium text-gray-400">Found at Depth:</span>
                        <span className="font-mono text-blue-300">{solution.depth}</span>
                      </div>
                    )}
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-400">Nodes Expanded:</span>
                      <span className="font-mono text-blue-300">{Number(solution.nodesExpanded).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-400">Time Taken:</span>
                      <span className="font-mono text-blue-300">{(solution.time ?? 0).toFixed(4)} s</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right visualizer */}
          <div className="w-full lg:w-2/3 flex flex-col items-center justify-center gap-6">
            <Board boardState={boardState} />

            {solution?.path && (
              <div className="w-full max-w-md bg-gray-800 p-4 rounded-lg shadow-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-300">
                    Step: {currentStep + 1} / {solution.path.length}
                  </span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleStep(-1)}
                      disabled={currentStep === 0}
                      className="px-3 py-1 bg-gray-700 rounded-md hover:bg-gray-600 disabled:opacity-50"
                    >
                      &larr; Prev
                    </button>
                    <button
                      onClick={() => handleStep(1)}
                      disabled={currentStep === solution.path.length - 1}
                      className="px-3 py-1 bg-gray-700 rounded-md hover:bg-gray-600 disabled:opacity-50"
                    >
                      Next &rarr;
                    </button>
                  </div>
                </div>

                <input
                  type="range"
                  min="0"
                  max={solution.path.length - 1}
                  value={currentStep}
                  onChange={handleSliderChange}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
