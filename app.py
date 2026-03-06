from flask import Flask, jsonify, request, send_from_directory
import heapq, os

app = Flask(__name__, static_folder="client/dist", static_url_path="")

# Singapore MRT Graph
# Edges: (station_a, station_b, travel_time_minutes)
MRT_EDGES = [
    # North-South Line (NS) - Red
    ("Jurong East","Buona Vista",6),("Buona Vista","Commonwealth",2),
    ("Commonwealth","Queenstown",2),("Queenstown","Redhill",2),
    ("Redhill","Tiong Bahru",3),("Tiong Bahru","Outram Park",3),
    ("Outram Park","Tanjong Pagar",2),("Tanjong Pagar","Raffles Place",2),
    ("Raffles Place","City Hall",1),("City Hall","Dhoby Ghaut",2),
    ("Dhoby Ghaut","Somerset",2),("Somerset","Orchard",2),
    ("Orchard","Newton",2),("Newton","Novena",2),
    ("Novena","Toa Payoh",3),("Toa Payoh","Braddell",2),
    ("Braddell","Bishan",2),("Bishan","Ang Mo Kio",4),
    ("Ang Mo Kio","Yio Chu Kang",3),("Yio Chu Kang","Khatib",4),
    ("Khatib","Yishun",4),("Yishun","Sembawang",4),
    ("Sembawang","Canberra",2),("Canberra","Woodlands",3),
    ("Woodlands","Marsiling",3),("Marsiling","Kranji",3),
    # East-West Line (EW) - Green
    ("Pasir Ris","Tampines",4),("Tampines","Simei",3),
    ("Simei","Tanah Merah",3),("Tanah Merah","Bedok",4),
    ("Bedok","Kembangan",2),("Kembangan","Eunos",2),
    ("Eunos","Paya Lebar",3),("Paya Lebar","Aljunied",2),
    ("Aljunied","Kallang",2),("Kallang","Lavender",2),
    ("Lavender","Bugis",2),("Bugis","City Hall",2),
    ("City Hall","Raffles Place",1),("Raffles Place","Tanjong Pagar",2),
    ("Tanjong Pagar","Outram Park",2),("Outram Park","Tiong Bahru",3),
    ("Tiong Bahru","Redhill",2),("Redhill","Queenstown",2),
    ("Queenstown","Commonwealth",2),("Commonwealth","Buona Vista",2),
    ("Buona Vista","Dover",2),("Dover","Clementi",2),
    ("Clementi","Jurong East",4),("Jurong East","Chinese Garden",3),
    ("Chinese Garden","Lakeside",2),("Lakeside","Boon Lay",3),
    ("Boon Lay","Pioneer",3),("Pioneer","Joo Koon",2),
    # North East Line (NE) - Purple
    ("HarbourFront","Outram Park",4),("Outram Park","Chinatown",3),
    ("Chinatown","Clarke Quay",2),("Clarke Quay","Dhoby Ghaut",2),
    ("Dhoby Ghaut","Little India",3),("Little India","Farrer Park",2),
    ("Farrer Park","Boon Keng",2),("Boon Keng","Potong Pasir",2),
    ("Potong Pasir","Woodleigh",2),("Woodleigh","Serangoon",3),
    ("Serangoon","Kovan",3),("Kovan","Hougang",3),
    ("Hougang","Buangkok",3),("Buangkok","Sengkang",3),
    ("Sengkang","Punggol",5),
    # Circle Line (CC) - Orange
    ("Dhoby Ghaut","Bras Basah",2),("Bras Basah","Esplanade",2),
    ("Esplanade","Promenade",2),("Promenade","Nicoll Highway",2),
    ("Nicoll Highway","Stadium",2),("Stadium","Mountbatten",2),
    ("Mountbatten","Dakota",2),("Dakota","Paya Lebar",3),
    ("Paya Lebar","MacPherson",2),("MacPherson","Tai Seng",2),
    ("Tai Seng","Bartley",2),("Bartley","Serangoon",3),
    ("Serangoon","Lorong Chuan",3),("Lorong Chuan","Bishan",3),
    ("Bishan","Marymount",3),("Marymount","Caldecott",3),
    ("Caldecott","Botanic Gardens",3),("Botanic Gardens","Farrer Road",2),
    ("Farrer Road","Holland Village",3),("Holland Village","Buona Vista",2),
    ("Buona Vista","one-north",3),("one-north","Kent Ridge",2),
    ("Kent Ridge","Haw Par Villa",2),("Haw Par Villa","Pasir Panjang",2),
    ("Pasir Panjang","Labrador Park",2),("Labrador Park","Telok Blangah",2),
    ("Telok Blangah","HarbourFront",3),
    # Downtown Line (DT) - Blue
    ("Bukit Panjang","Cashew",3),("Cashew","Hillview",3),
    ("Hillview","Beauty World",3),("Beauty World","King Albert Park",2),
    ("King Albert Park","Sixth Avenue",2),("Sixth Avenue","Tan Kah Kee",2),
    ("Tan Kah Kee","Botanic Gardens",2),("Botanic Gardens","Stevens",3),
    ("Stevens","Newton",2),("Newton","Little India",3),
    ("Little India","Rochor",2),("Rochor","Bugis",2),
    ("Bugis","Promenade",3),("Promenade","Bayfront",2),
    ("Bayfront","Downtown",2),("Downtown","Telok Ayer",2),
    ("Telok Ayer","Chinatown",2),("Chinatown","Fort Canning",2),
    ("Fort Canning","Bencoolen",2),("Bencoolen","Jalan Besar",2),
    ("Jalan Besar","Bendemeer",2),("Bendemeer","Geylang Bahru",2),
    ("Geylang Bahru","Mattar",2),("Mattar","MacPherson",2),
    ("MacPherson","Ubi",2),("Ubi","Kaki Bukit",2),
    ("Kaki Bukit","Bedok North",2),("Bedok North","Bedok Reservoir",2),
    ("Bedok Reservoir","Tampines West",3),("Tampines West","Tampines",2),
    ("Tampines","Tampines East",2),("Tampines East","Upper Changi",3),
    ("Upper Changi","Expo",2),
    # Thomson-East Coast Line (TE) - Brown
    ("Woodlands North","Woodlands",3),("Woodlands","Springleaf",4),
    ("Springleaf","Lentor",2),("Lentor","Mayflower",2),
    ("Mayflower","Bright Hill",2),("Bright Hill","Upper Thomson",3),
    ("Upper Thomson","Caldecott",3),("Caldecott","Stevens",4),
    ("Stevens","Napier",3),("Napier","Orchard Boulevard",2),
    ("Orchard Boulevard","Orchard",2),("Orchard","Great World",3),
    ("Great World","Havelock",2),("Havelock","Outram Park",2),
    ("Outram Park","Maxwell",2),("Maxwell","Shenton Way",2),
    ("Shenton Way","Marina Bay",3),("Marina Bay","Marina South",3),
]

LINE_COLORS = {
    "NS": "#d42e12", "EW": "#009645", "NE": "#9900aa",
    "CC": "#fa9e0d", "DT": "#005ec4", "TE": "#9D5B25",
}

def build_graph(edges):
    graph = {}
    for a, b, w in edges:
        graph.setdefault(a, {})[b] = w
        graph.setdefault(b, {})[a] = w
    return graph

def dijkstra(graph, start, end):
    dist = {n: float("inf") for n in graph}
    prev = {n: None for n in graph}
    dist[start] = 0
    visited_order = []
    pq = [(0, start)]
    while pq:
        cost, u = heapq.heappop(pq)
        if cost > dist[u]:
            continue
        visited_order.append(u)
        if u == end:
            break
        for v, w in graph[u].items():
            nc = cost + w
            if nc < dist[v]:
                dist[v] = nc
                prev[v] = u
                heapq.heappush(pq, (nc, v))
    path, node = [], end
    while node:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path if path[0] == start else [], dist[end], visited_order

GRAPH = build_graph(MRT_EDGES)
ALL_STATIONS = sorted(GRAPH.keys())

@app.route("/api/stations")
def stations():
    return jsonify(ALL_STATIONS)

@app.route("/api/route", methods=["POST"])
def route():
    data = request.get_json()
    start, end = data.get("start"), data.get("end")
    if start not in GRAPH or end not in GRAPH:
        return jsonify({"error": "Invalid station"}), 400
    if start == end:
        return jsonify({"error": "Start and end must differ"}), 400
    path, cost, visited = dijkstra(GRAPH, start, end)
    if not path:
        return jsonify({"error": "No path found"}), 404
    return jsonify({"path": path, "duration": cost, "stops": len(path) - 1, "visited": visited})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
