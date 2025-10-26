import time
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
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

        # selecting which algorithm to use
        if algorithm == "bfs":
            res_path, cost, nodes_expanded = bfs(state)

        elif algorithm == "dfs":
            res_path, cost, nodes_expanded = dfs(state)

        elif algorithm == "astar-manhattan":
            res = A_star_manhattan(state)
            res_path = res.get("path")
            cost = res.get("cost")
            nodes_expanded = res.get("nodes_expanded", 0)

        elif algorithm == "astar-euclidean":
            res = A_star_euclidean(state)
            res_path = res.get("path")
            cost = res.get("cost")
            nodes_expanded = res.get("nodes_expanded", 0)

        elif algorithm == "iddfs":
            # Fix: increase max_depth for hard puzzles
            res_path, cost, nodes_expanded, depth = iddfs(state, max_depth=31) 

        else:
            return jsonify({"error": "Unknown algorithm"}), 400

        end_time = time.time()
        time_taken = end_time - start_time

        if res_path is None:
            # Return stats even if no solution is found
            return jsonify({
                "error": "Solution not found within limits.",
                "nodesExpanded": nodes_expanded,
                "time": time_taken,
            }), 200  # 200 OK, not 404

        # Build response
        response = {
            "path": res_path,
            "cost": cost,
            "nodesExpanded": nodes_expanded,
            "time": time_taken,
        }
        if depth is not None:
            response["depth"] = depth

        return jsonify(response)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500



if __name__ == "__main__":
    print("=====================================================")
    print(" 8-Puzzle Flask API running at http://127.0.0.1:5000")
    print("=====================================================")
    app.run(debug=True, port=5000)


