import time
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
# Import the new Python logic file
from AI_Assignment_1 import (
    bfs, dfs, A_star_manhattan, A_star_euclidean, iddfs, is_solvable
)

GOAL_STATE = "012345678"  # Define the goal state

app = Flask(__name__)
CORS(app)  # Allow requests from your React app

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    # Clean spaces from input, as handled in new React app
    state = data.get("state", "").replace(" ", "")
    algorithm = data.get("algorithm")

    # --- Validation ---
    if not state or len(state) != 9 or not all(c in '012345678' for c in state) or len(set(state)) != 9:
        return jsonify({"error": "Invalid state. Must be 9 unique digits from 0-8."}), 400

    if not is_solvable(state):
        return jsonify({"error": "Unsolvable puzzle (Odd number of inversions)"}), 400

    try:
        start_time = time.time()
        
        res_path = None
        cost = None
        nodes_expanded = 0
        depth = None

        # --- Algorithm Selection (Updated) ---
        if algorithm == "bfs":
            res_path, cost, nodes_expanded = bfs(state)

        elif algorithm == "dfs":
            res_path, cost, nodes_expanded = dfs(state)

        elif algorithm == "astar-manhattan":
            # Handles the dict return from your notebook's A*
            res = A_star_manhattan(state)
            res_path = res.get("path")
            cost = res.get("cost")
            nodes_expanded = res.get("nodes_expanded", 0)

        elif algorithm == "astar-euclidean":
            # Handles the dict return from your notebook's A*
            res = A_star_euclidean(state)
            res_path = res.get("path")
            cost = res.get("cost")
            nodes_expanded = res.get("nodes_expanded", 0)

        elif algorithm == "iddfs":
            # Handles the new standardized tuple return
            res_path, cost, nodes_expanded, depth = iddfs(state) 

        else:
            return jsonify({"error": "Unknown algorithm"}), 400

        # --- FIX: Append Goal State ---
        # The get_path() in the notebook file forgets to add the goal state itself.
        if res_path is not None and (not res_path or res_path[-1] != GOAL_STATE):
            res_path.append(GOAL_STATE)
            # Ensure cost matches the new path length
            if cost is not None:
                cost = len(res_path) - 1
        # --- End Fix ---

        end_time = time.time()
        time_taken = end_time - start_time

        # --- Response ---
        if res_path is None:
            # Send back stats even if no solution is found
            return jsonify({
                "error": "No solution found.",
                "nodesExpanded": nodes_expanded,
                "time": time_taken,
            }), 404

        response = {
            "path": res_path,
            "cost": cost,
            "nodesExpanded": nodes_expanded,
            "time": time_taken,
        }
        # Only add depth key if it's relevant (for IDDFS)
        if depth is not None:
            response["depth"] = depth

        return jsonify(response)

    except Exception as e:
        # Log the full error to the console for debugging
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    print("=====================================================")
    print("✅ 8-Puzzle Flask API running at http://127.0.0.1:5000")
    print("=====================================================")
    app.run(debug=True, port=5000)


