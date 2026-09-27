import sys
import os
from collections import deque
import matplotlib
matplotlib.use("TkAgg" if "DISPLAY" in os.environ else "Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from colorama import init, Fore, Back, Style

init(autoreset=True)



# DATA: GRAF ITERA
    
EDGES = [
    ("Labtek 3",      "Labtek 1",      150),
    
    ("Labtek 1",      "GKU 1",         110),
    ("GKU 1",         "Labtek 2",      190),
    ("Labtek 2",      "Labtek OZT",    110),
    ("Labtek OZT",    "BDR GKU 1",     220),
    ("Gerbang Barat", "BDR GKU 1",     260),
    ("BDR GKU 1",     "Kebun Raya",    850),
    ("BDR GKU 1",     "BDR F",         100),
    ("BDR F",         "Gedung F",      400),
    ("Gedung F",      "BDR GKU 2",     100),
    ("Gedung A",      "Gerbang Utama", 120),
    ("Gedung A",      "Gedung C/D",    120),
    ("Gedung C/D",    "Labtek 1",      450),
    ("Gedung A",      "Perempatan",     50),
    ("Gerbang Utama", "Gedung B",      120),
    ("Gedung B",      "Perempatan",     50),
    ("Perempatan",    "GKU 2",         240),
    ("GKU 2",         "BDR GKU 2",      40),
    ("Perempatan",    "Gedung E",      210),
    ("Gedung E",      "BDR GKU 2",     180),
    ("BDR GKU 2",     "Labtek 4",       40),
    ("Labtek 4",      "GSG",           400),
    ("GSG",           "Rima",         1000),
    ("Rima",          "Asrama",        350),
    ("Asrama",        "Masjid At-Tanwir", 250),
    ("Perempatan",    "Asrama",        320),
]

# Koordinat node untuk visualisasi (x, y)
NODE_POS = {
    "Labtek 3":          (0.5,  8.5),
    "Labtek 1":          (2.5,  8.5),
    "Gedung A":          (5.0,  8.5),
    "Gedung C/D":        (5.0,  7.6),
    "Gerbang Utama":     (6.5,  9.8),
    "Gedung B":          (8.0,  8.5),
    "Masjid At-Tanwir":  (11.5, 9.0),
    "GKU 1":             (2.5,  6.8),
    "Perempatan":        (6.5,  6.8),
    "Asrama":            (9.5,  6.8),
    "Labtek 2":          (2.5,  5.2),
    "GKU 2":             (5.2,  5.0),
    "Gedung E":          (8.2,  5.0),
    "Rima":              (11.5, 5.0),
    "Labtek OZT":        (2.5,  3.8),
    "BDR GKU 2":         (6.8,  3.5),
    "BDR GKU 1":         (3.8,  2.5),
    "Gerbang Barat":     (1.0,  2.0),
    "Gedung F":          (6.0,  2.0),
    "Labtek 4":          (8.5,  2.0),
    "GSG":               (10.5, 3.5),
    "BDR F":             (4.8,  1.0),
    "Kebun Raya":        (2.5,  0.5),
}

#  WARNA TERMINAL

C = {
    "title":    Fore.CYAN  + Style.BRIGHT,
    "header":   Fore.BLUE  + Style.BRIGHT,
    "success":  Fore.GREEN + Style.BRIGHT,
    "warning":  Fore.YELLOW,
    "error":    Fore.RED   + Style.BRIGHT,
    "info":     Fore.WHITE,
    "muted":    Fore.WHITE + Style.DIM,
    "node":     Fore.CYAN,
    "path":     Fore.YELLOW + Style.BRIGHT,
    "number":   Fore.MAGENTA + Style.BRIGHT,
    "teal":     Fore.CYAN  + Style.BRIGHT,
    "reset":    Style.RESET_ALL,
}

#  HELPER: TERMINAL

def hr(char="─", width=65, color=Fore.BLUE):
    print(color + char * width + Style.RESET_ALL)

def banner():
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_node_list(nodes):
    """Print daftar node dalam format grid 3 kolom."""
    sorted_nodes = sorted(nodes)
    per_col = (len(sorted_nodes) + 2) // 3
    cols = [sorted_nodes[i:i+per_col] for i in range(0, len(sorted_nodes), per_col)]
    max_rows = max(len(c) for c in cols)
    hr()
    print(C["header"] + f"  {'No':<4} {'Nama Lokasi':<25}  {'No':<4} {'Nama Lokasi':<25}  {'No':<4} {'Nama Lokasi':<25}")
    hr()
    for r in range(max_rows):
        row = ""
        for ci, col in enumerate(cols):
            if r < len(col):
                idx = ci * per_col + r + 1
                row += C["number"] + f"  {idx:<4}" + C["node"] + f"{col[r]:<25}  "
            else:
                row += " " * 32
        print(row)
    hr()


#  GRAPH BUILDER

def build_graph(edges):
    """Bangun adjacency list dari daftar edge."""
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
    return graph


#  BFS ALGORITHM

def bfs(graph, start, goal):
    """
    BFS dari start ke goal.
    Returns: (path, visited_order, steps, parent)
    - path         : list node dari start → goal
    - visited_order: urutan node dikunjungi
    - steps        : list dict untuk tabel langkah
    - parent       : dict parent setiap node
    """
    visited     = set()
    parent      = {start: None}
    queue       = deque([start])
    visited.add(start)
    visited_order = [start]
    steps         = []
    step_num      = 1
    found         = False

    while queue:
        current = queue.popleft()

        neighbors_added = []
        for neighbor, _ in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                visited_order.append(neighbor)
                neighbors_added.append(neighbor)

        steps.append({
            "step":      step_num,
            "current":   current,
            "neighbors": neighbors_added,
            "queue":     list(queue),
            "visited":   list(visited),
            "is_goal":   current == goal,
        })
        step_num += 1

        if current == goal:
            found = True
            break

    if not found:
        return None, visited_order, steps, parent

    # Rekonstruksi jalur
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, visited_order, steps, parent


def calc_path_distance(path, graph):
    """Hitung total jarak jalur dalam meter."""
    total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        for nb, w in graph[u]:
            if nb == v:
                total += w
                break
    return total


def get_edge_weight(u, v, graph):
    """Dapatkan bobot edge u-v."""
    for nb, w in graph.get(u, []):
        if nb == v:
            return w
    return 0

#  OUTPUT: TABEL LANGKAH BFS

def print_bfs_steps(steps, goal):
    print()
    hr("═", 65, C["header"])
    print(C["header"] + "    TABEL LANGKAH-LANGKAH BFS")
    hr("═", 65, C["header"])
    print()

    # Header tabel
    print(
        C["muted"] + f"  {'Step':>4}  " +
        C["header"] + f"{'Node Diproses':<20}" +
        C["info"]   + f"{'Tetangga Ditemukan':<35}" +
        C["muted"]  + f"{'Antrian (Queue)':>0}"
    )
    hr("─", 65)

    for s in steps:
        is_goal = s["is_goal"]
        cur_color = C["success"] if is_goal else C["path"]

        # Current node
        line = C["number"] + f"  {s['step']:>4}  " + cur_color + f"{s['current']:<20}"

        # Tetangga
        if s["neighbors"]:
            nb_str = ", ".join(s["neighbors"])
            if len(nb_str) > 33:
                nb_str = nb_str[:30] + "..."
        else:
            nb_str = Fore.WHITE + Style.DIM + "(tidak ada baru)"

        line += C["node"] + f"{nb_str:<35}"

        # Queue
        if s["queue"]:
            q_str = " → ".join(s["queue"])
            if len(q_str) > 35:
                q_str = q_str[:32] + "..."
            line += C["muted"] + f"[{q_str}]"
        else:
            line += C["muted"] + "[kosong]"

        print(line)

        if is_goal:
            print(C["success"] + "  " + "─" * 63)
            print(C["success"] + f"    TUJUAN '{goal}' DITEMUKAN pada langkah ke-{s['step']}!")
            print(C["success"] + "  " + "─" * 63)
            break

    print()

#  OUTPUT: POHON BFS

def print_bfs_tree(parent, start, path):
    """Tampilkan pohon BFS sebagai struktur teks berlevel."""
    print()
    hr("═", 65, C["header"])
    print(C["header"] + "    POHON BFS (BFS TREE)")
    hr("═", 65, C["header"])
    print()

    # Bangun children map dari parent
    children = {}
    for node, par in parent.items():
        if par is not None:
            children.setdefault(par, []).append(node)

    path_set = set(path)

    def print_subtree(node, prefix="", is_last=True, depth=0):
        connector = "└── " if is_last else "├── "
        on_path   = node in path_set

        if depth == 0:
            # Root node
            print(C["success"] + Style.BRIGHT + f"   {node}  ← ASAL")
        else:
            color = C["path"] if on_path else C["node"]
            marker = " ◀ JALUR" if on_path else ""
            print("  " + C["muted"] + prefix + connector + color + node + C["success"] + marker)

        kids = children.get(node, [])
        for i, child in enumerate(sorted(kids)):
            is_last_child = (i == len(kids) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_subtree(child, new_prefix, is_last_child, depth + 1)

    print_subtree(start)
    print()
    print(C["muted"] + "  Keterangan:")
    print(C["path"]  + "  ◀ JALUR  " + C["muted"] + "= node pada rute yang ditemukan")
    print(C["node"]  + "  (node)   " + C["muted"] + "= node yang dikunjungi BFS")
    print()

#  OUTPUT: HASIL RUTE

def print_route_result(path, graph, start, goal):
    print()
    hr("═", 65, C["success"])
    print(C["success"] + "  ️   RUTE DITEMUKAN")
    hr("═", 65, C["success"])
    print()

    # Jalur → panah
    route_str = ""
    for i, node in enumerate(path):
        if i == 0:
            route_str += C["success"] + Style.BRIGHT + f"[{node}]"
        elif i == len(path) - 1:
            route_str += C["path"] + f" ──▶ " + C["success"] + Style.BRIGHT + f"[{node}]"
        else:
            route_str += C["path"] + f" ──▶ " + C["node"] + f"[{node}]"
    print("  " + route_str)
    print()

    # Tabel segmen
    hr("─", 65)
    print(C["header"] + f"  {'No':>3}  {'Dari':<22}  {'Ke':<22}  {'Jarak':>8}")
    hr("─", 65)

    total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        w = get_edge_weight(u, v, graph)
        total += w
        print(
            C["number"] + f"  {i+1:>3}  " +
            C["node"]   + f"{u:<22}  " +
            C["node"]   + f"{v:<22}  " +
            C["path"]   + f"{w:>6} m"
        )

    hr("─", 65)
    print(C["success"] + Style.BRIGHT + f"  {'TOTAL':>28}{'':22}  {total:>6} m")
    hr("─", 65)

    print()
    print(C["success"] + f"   Titik Awal   : " + C["path"] + start)
    print(C["success"] + f"   Titik Tujuan : " + C["path"] + goal)
    print(C["success"] + f"   Total Jarak  : " + C["number"] + f"{total:,} meter")
    print(C["success"] + f"   Jumlah Simpul: " + C["number"] + f"{len(path)} node")
    print(C["info"]    + f"   BFS menemukan rute dengan jumlah simpul minimum (hop terpendek).")
    print()

#  VISUALISASI GRAF (matplotlib)

def visualize_graph(path, graph, start, goal, visited_order, parent):
    """Tampilkan 3 subplot: Graf Utama, Pohon BFS, dan Info."""

    path_set   = set(path)
    path_edges = set()
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        path_edges.add((u, v))
        path_edges.add((v, u))

    all_nodes = list(NODE_POS.keys())
    pos = NODE_POS

    fig = plt.figure(figsize=(20, 12), facecolor="#0B1F45")
    fig.suptitle(
        f"BFS Navigasi Kampus ITERA  —  {start}  →  {goal}",
        fontsize=16, fontweight="bold", color="white",
        y=0.98
    )

    # ── Subplot 1: Graf Utama ──
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_facecolor("#0F2550")
    ax1.set_title("Visualisasi Graf Kampus ITERA", color="white", fontsize=12, pad=10)

    G = nx.Graph()
    G.add_nodes_from(all_nodes)
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)

    # Warna node
    node_colors = []
    node_sizes  = []
    for n in G.nodes():
        if n == start:
            node_colors.append("#00E676")  # hijau terang
            node_sizes.append(800)
        elif n == goal:
            node_colors.append("#FF5252")  # merah
            node_sizes.append(800)
        elif n in path_set:
            node_colors.append("#FFD740")  # kuning — jalur
            node_sizes.append(600)
        elif n in set(visited_order):
            node_colors.append("#448AFF")  # biru — dikunjungi
            node_sizes.append(400)
        else:
            node_colors.append("#546E7A")  # abu — tidak dikunjungi
            node_sizes.append(350)

    # Warna edge
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if (u, v) in path_edges or (v, u) in path_edges:
            edge_colors.append("#FFD740")
            edge_widths.append(3.5)
        else:
            edge_colors.append("#1E3A5F")
            edge_widths.append(1.0)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax1)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax1, alpha=0.9)

    # Label node (ukuran font adaptif)
    for node, (x, y) in pos.items():
        color = "white"
        if node == start or node == goal:
            color = "#0B1F45"
        fontsize = 6.5
        ax1.text(x, y, node, ha="center", va="center",
                 fontsize=fontsize, fontweight="bold", color=color,
                 bbox=dict(boxstyle="round,pad=0.15", facecolor="none",
                           edgecolor="none", alpha=0))

    # Label bobot pada jalur
    for u, v, w in EDGES:
        if (u, v) in path_edges:
            mx = (pos[u][0] + pos[v][0]) / 2
            my = (pos[u][1] + pos[v][1]) / 2
            ax1.text(mx, my, f"{w}m", fontsize=6, color="#FFD740",
                     ha="center", va="center",
                     bbox=dict(boxstyle="round,pad=0.1", facecolor="#0F2550",
                               edgecolor="#FFD740", linewidth=0.5, alpha=0.85))

    # Legenda
    legend_items = [
        mpatches.Patch(color="#00E676", label=f"Start: {start}"),
        mpatches.Patch(color="#FF5252", label=f"Goal: {goal}"),
        mpatches.Patch(color="#FFD740", label="Jalur BFS"),
        mpatches.Patch(color="#448AFF", label="Node dikunjungi"),
        mpatches.Patch(color="#546E7A", label="Node lain"),
    ]
    ax1.legend(handles=legend_items, loc="lower left", fontsize=7.5,
               facecolor="#0B2040", edgecolor="#1E3A5F", labelcolor="white")

    ax1.axis("off")

    # ── Subplot 2: Pohon BFS ──
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor("#0F2550")
    ax2.set_title("Pohon BFS (BFS Tree)", color="white", fontsize=12, pad=10)

    # Bangun tree graph dari parent map
    T = nx.DiGraph()
    for node, visited_nodes in parent.items():
        pass

    # Bangun tree dari parent dict
    tree_nodes = list(parent.keys())
    T.add_nodes_from(tree_nodes)
    for node, par in parent.items():
        if par is not None:
            T.add_edge(par, node)

    # Hitung posisi tree dengan layout hierarki
    def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0,
                      xcenter=0.5, pos=None, parent=None, parsed=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        if parsed is None:
            parsed = []
        children = [n for n in G.neighbors(root) if n not in parsed]
        if children:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                    vert_loc=vert_loc - vert_gap,
                                    xcenter=nextx, pos=pos,
                                    parent=root, parsed=parsed + [root])
        return pos

    if T.nodes():
        try:
            tree_pos = hierarchy_pos(T, start, width=2.0, vert_gap=0.18)
        except Exception:
            tree_pos = nx.spring_layout(T, seed=42)

        # Warna node pohon
        t_node_colors = []
        t_node_sizes  = []
        for n in T.nodes():
            if n == start:
                t_node_colors.append("#00E676")
                t_node_sizes.append(700)
            elif n == goal:
                t_node_colors.append("#FF5252")
                t_node_sizes.append(700)
            elif n in path_set:
                t_node_colors.append("#FFD740")
                t_node_sizes.append(500)
            else:
                t_node_colors.append("#448AFF")
                t_node_sizes.append(350)

        # Warna edge pohon
        t_edge_colors = []
        t_edge_widths = []
        for u, v in T.edges():
            if u in path_set and v in path_set:
                t_edge_colors.append("#FFD740")
                t_edge_widths.append(2.5)
            else:
                t_edge_colors.append("#2E5090")
                t_edge_widths.append(1.0)

        nx.draw_networkx_nodes(T, tree_pos, node_color=t_node_colors,
                               node_size=t_node_sizes, ax=ax2)
        nx.draw_networkx_edges(T, tree_pos, edge_color=t_edge_colors,
                               width=t_edge_widths, ax=ax2, arrows=True,
                               arrowsize=10, arrowstyle="-|>",
                               connectionstyle="arc3,rad=0.0")

        # Label
        for node, (x, y) in tree_pos.items():
            short = node if len(node) <= 12 else node[:10] + ".."
            ax2.text(x, y, short, ha="center", va="center",
                     fontsize=6, fontweight="bold",
                     color="#0B1F45" if node in {start, goal} else "white")

        # Level labels
        levels = {}
        for node in T.nodes():
            d = nx.shortest_path_length(T, start, node) if nx.has_path(T, start, node) else 0
            levels.setdefault(d, []).append(node)

        for lvl, nodes_in_lvl in levels.items():
            sample_y = tree_pos[nodes_in_lvl[0]][1]
            ax2.text(-1.1, sample_y, f"L{lvl}", fontsize=7, color="#546E7A",
                     va="center", ha="right")

    ax2.axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Simpan gambar
    out_path = "bfs_itera_output.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(C["success"] + f"\n   Visualisasi disimpan ke: " + C["path"] + out_path)

    # Coba tampilkan jika ada display
    try:
        plt.show()
    except Exception:
        pass

    plt.close()

#  INPUT HANDLER

def get_node_input(prompt_text, nodes_sorted, label):
    """Minta input node dari pengguna dengan validasi."""
    while True:
        print(C["header"] + f"\n  {prompt_text}")
        print(C["muted"] + "  (ketik nama lengkap atau nomor dari daftar di atas)\n")
        raw = input(C["teal"] + f"    {label}: " + Style.RESET_ALL).strip()

        # Coba parse nomor
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(nodes_sorted):
                chosen = nodes_sorted[idx]
                print(C["success"] + f"    Dipilih: {chosen}")
                return chosen
            else:
                print(C["error"] + f"    Nomor {raw} tidak valid. Pilih antara 1–{len(nodes_sorted)}.")
                continue

        # Coba exact match (case-insensitive)
        match = next((n for n in nodes_sorted if n.lower() == raw.lower()), None)
        if match:
            print(C["success"] + f"    Dipilih: {match}")
            return match

        # Coba partial match
        matches = [n for n in nodes_sorted if raw.lower() in n.lower()]
        if len(matches) == 1:
            print(C["success"] + f"    Ditemukan: {matches[0]}")
            return matches[0]
        elif len(matches) > 1:
            print(C["warning"] + f"  ⚠  Beberapa cocok: {', '.join(matches)}")
            print(C["muted"] + "     Ketik lebih spesifik atau gunakan nomor.")
        else:
            print(C["error"] + f"    '{raw}' tidak ditemukan. Coba lagi.")


#  EKSPOR HALAMAN WEB (index.html)

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>BFS Navigasi Kampus ITERA</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background: #071936;
            color: white;
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #0b1f45, #102d61);
            padding: 50px 20px;
            text-align: center;
            border-bottom: 1px solid #284d83;
        }

        header h1 {
            font-size: 36px;
            margin-bottom: 12px;
        }

        header p {
            color: #b8c7df;
            font-size: 16px;
        }

        .container {
            width: 90%;
            max-width: 1100px;
            margin: 35px auto;
        }

        .card {
            background: #0d2349;
            border: 1px solid #244878;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }

        .card h2 {
            margin-bottom: 18px;
            color: #ffffff;
        }

        .description {
            color: #c8d4e8;
            line-height: 1.7;
        }

        .algorithm {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .algorithm div {
            background: #102b58;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #2b5389;
        }

        .algorithm strong {
            display: block;
            margin-bottom: 8px;
            color: #ffd740;
        }

        .form-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #cbd8eb;
        }

        select {
            width: 100%;
            padding: 13px;
            border-radius: 8px;
            border: 1px solid #40679c;
            background: #071936;
            color: white;
            font-size: 15px;
        }

        button {
            width: 100%;
            margin-top: 20px;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #1976d2;
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #2196f3;
        }

        .result {
            display: none;
        }

        .result-box {
            background: #071936;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }

        .route {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
        }

        .node {
            background: #ffd740;
            color: #071936;
            padding: 9px 13px;
            border-radius: 7px;
            font-weight: bold;
        }

        .arrow {
            color: #ffd740;
            font-weight: bold;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .stat {
            background: #102b58;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
        }

        .stat span {
            display: block;
            font-size: 24px;
            font-weight: bold;
            color: #00e676;
            margin-top: 8px;
        }

        .steps {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #294d7e;
            text-align: left;
        }

        th {
            color: #ffd740;
            background: #102b58;
        }

        .visited {
            color: #64b5f6;
        }

        .goal {
            color: #00e676;
            font-weight: bold;
        }

        footer {
            text-align: center;
            padding: 30px;
            color: #8fa6c5;
            border-top: 1px solid #244878;
            margin-top: 40px;
        }

        @media (max-width: 700px) {
            .algorithm,
            .form-group,
            .stats {
                grid-template-columns: 1fr;
            }

            header h1 {
                font-size: 27px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>🧭 BFS Navigasi Kampus ITERA</h1>
    <p>Pencarian Jalur Antar Lokasi ITERA Menggunakan Algoritma Breadth-First Search</p>
</header>


<div class="container">

    <!-- ABOUT -->
    <section class="card">
        <h2>📌 Tentang Proyek</h2>

        <p class="description">
            Proyek ini mengimplementasikan algoritma
            <strong>Breadth-First Search (BFS)</strong>
            untuk mencari jalur antar lokasi di lingkungan Kampus ITERA.
            Setiap lokasi direpresentasikan sebagai node pada graph,
            sedangkan hubungan antar lokasi direpresentasikan sebagai edge
            dengan bobot jarak dalam meter.
        </p>

        <div class="algorithm">

            <div>
                <strong>Algoritma</strong>
                Breadth-First Search
            </div>

            <div>
                <strong>Struktur Data</strong>
                Graph & Queue
            </div>

            <div>
                <strong>Bahasa</strong>
                Python & JavaScript
            </div>

        </div>
    </section>


    <!-- INPUT -->
    <section class="card">

        <h2>🔎 Cari Rute</h2>

        <div class="form-group">

            <div>
                <label for="start">Titik Awal</label>

                <select id="start">
                    <option value="">-- Pilih lokasi --</option>
                </select>
            </div>

            <div>
                <label for="goal">Titik Tujuan</label>

                <select id="goal">
                    <option value="">-- Pilih lokasi --</option>
                </select>
            </div>

        </div>

        <button onclick="runBFS()">
            🚀 Jalankan BFS
        </button>

    </section>


    <!-- RESULT -->
    <section class="card result" id="result">

        <h2>📍 Hasil Pencarian</h2>

        <div class="result-box">

            <p>
                <strong>Titik Awal:</strong>
                <span id="resultStart"></span>
            </p>

            <p style="margin-top: 8px;">
                <strong>Titik Tujuan:</strong>
                <span id="resultGoal"></span>
            </p>

            <h3 style="margin-top: 20px;">
                Jalur BFS
            </h3>

            <div class="route" id="route"></div>

        </div>


        <div class="stats">

            <div class="stat">
                Jumlah Node
                <span id="nodeCount">0</span>
            </div>

            <div class="stat">
                Jumlah Hop
                <span id="hopCount">0</span>
            </div>

            <div class="stat">
                Total Jarak
                <span id="distance">0 m</span>
            </div>

        </div>

    </section>


    <!-- BFS STEPS -->
    <section class="card result" id="stepsCard">

        <h2>📊 Langkah-Langkah BFS</h2>

        <div class="steps">

            <table>

                <thead>
                    <tr>
                        <th>Step</th>
                        <th>Node Diproses</th>
                        <th>Tetangga Ditemukan</th>
                        <th>Queue</th>
                    </tr>
                </thead>

                <tbody id="stepsBody"></tbody>

            </table>

        </div>

    </section>


    <!-- INFORMATION -->
    <section class="card">

        <h2>💡 Cara Kerja</h2>

        <p class="description">

            1. Pengguna memilih lokasi awal dan lokasi tujuan.

            <br><br>

            2. Sistem membentuk graph berdasarkan hubungan antar lokasi ITERA.

            <br><br>

            3. Algoritma BFS melakukan pencarian menggunakan struktur data
            <i>queue</i>.

            <br><br>

            4. Node yang telah dikunjungi dicatat dan setiap node menyimpan
            parent untuk membentuk kembali jalur.

            <br><br>

            5. Setelah tujuan ditemukan, sistem menampilkan jalur BFS,
            jumlah hop, dan total jarak berdasarkan bobot edge.

        </p>

    </section>

</div>


<footer>

    <p>
        Pencarian Jarak Antar Lokasi ITERA
        dengan Algoritma BFS
    </p>

    <p style="margin-top: 8px;">
        Data Science Project
    </p>

</footer>


<script>

/* =====================================================
   DATA GRAF ITERA
===================================================== */

__EDGES_JS_PLACEHOLDER__


/* =====================================================
   BUILD GRAPH
===================================================== */

function buildGraph(edges) {

    const graph = {};

    edges.forEach(([u, v, w]) => {

        if (!graph[u])
            graph[u] = [];

        if (!graph[v])
            graph[v] = [];

        graph[u].push({
            node: v,
            weight: w
        });

        graph[v].push({
            node: u,
            weight: w
        });

    });

    return graph;
}


const graph = buildGraph(EDGES);

const nodes = Object.keys(graph).sort();


/* =====================================================
   MASUKKAN LOKASI KE SELECT
===================================================== */

const startSelect = document.getElementById("start");
const goalSelect = document.getElementById("goal");


nodes.forEach(node => {

    const option1 = document.createElement("option");
    option1.value = node;
    option1.textContent = node;

    const option2 = document.createElement("option");
    option2.value = node;
    option2.textContent = node;

    startSelect.appendChild(option1);
    goalSelect.appendChild(option2);

});


/* =====================================================
   BFS
===================================================== */

function bfs(start, goal) {

    const queue = [start];

    const visited = new Set();

    const parent = {};

    const steps = [];

    visited.add(start);

    parent[start] = null;


    while (queue.length > 0) {

        const current = queue.shift();

        const neighborsAdded = [];


        graph[current].forEach(edge => {

            const neighbor = edge.node;

            if (!visited.has(neighbor)) {

                visited.add(neighbor);

                parent[neighbor] = current;

                queue.push(neighbor);

                neighborsAdded.push(neighbor);

            }

        });


        steps.push({

            current: current,

            neighbors: neighborsAdded,

            queue: [...queue],

            goal: current === goal

        });


        if (current === goal)
            break;

    }


    if (!visited.has(goal)) {

        return null;

    }


    /* Rekonstruksi jalur */

    const path = [];

    let current = goal;


    while (current !== null) {

        path.push(current);

        current = parent[current];

    }


    path.reverse();


    return {
        path: path,
        steps: steps,
        visited: [...visited],
        parent: parent
    };

}


/* =====================================================
   HITUNG JARAK
===================================================== */

function calculateDistance(path) {

    let total = 0;


    for (let i = 0; i < path.length - 1; i++) {

        const current = path[i];

        const next = path[i + 1];


        const edge = graph[current].find(
            item => item.node === next
        );


        if (edge) {

            total += edge.weight;

        }

    }


    return total;

}


/* =====================================================
   JALANKAN BFS
===================================================== */

function runBFS() {

    const start = startSelect.value;
    const goal = goalSelect.value;


    if (!start || !goal) {

        alert("Silakan pilih titik awal dan titik tujuan.");

        return;

    }


    if (start === goal) {

        alert("Titik awal dan tujuan tidak boleh sama.");

        return;

    }


    const result = bfs(start, goal);


    if (!result) {

        alert("Tidak ditemukan jalur.");

        return;

    }


    const path = result.path;

    const distance = calculateDistance(path);


    /* Tampilkan result */

    document.getElementById("result").style.display = "block";

    document.getElementById("stepsCard").style.display = "block";


    document.getElementById("resultStart").textContent = start;

    document.getElementById("resultGoal").textContent = goal;


    /* Route */

    const routeContainer = document.getElementById("route");

    routeContainer.innerHTML = "";


    path.forEach((node, index) => {

        const nodeElement = document.createElement("span");

        nodeElement.className = "node";

        nodeElement.textContent = node;

        routeContainer.appendChild(nodeElement);


        if (index < path.length - 1) {

            const arrow = document.createElement("span");

            arrow.className = "arrow";

            arrow.textContent = "→";

            routeContainer.appendChild(arrow);

        }

    });


    /* Statistik */

    document.getElementById("nodeCount").textContent =
        path.length;

    document.getElementById("hopCount").textContent =
        path.length - 1;

    document.getElementById("distance").textContent =
        distance.toLocaleString("id-ID") + " m";


    /* =================================================
       TABEL LANGKAH BFS
    ================================================= */

    const tableBody = document.getElementById("stepsBody");

    tableBody.innerHTML = "";


    result.steps.forEach((step, index) => {

        const row = document.createElement("tr");


        const neighbors =
            step.neighbors.length > 0
            ? step.neighbors.join(", ")
            : "-";


        const queue =
            step.queue.length > 0
            ? step.queue.join(" → ")
            : "Kosong";


        row.innerHTML = `

            <td>${index + 1}</td>

            <td class="${step.goal ? "goal" : "visited"}">
                ${step.current}
            </td>

            <td>${neighbors}</td>

            <td>${queue}</td>

        `;


        tableBody.appendChild(row);

    });


    /* Scroll ke hasil */

    document.getElementById("result")
        .scrollIntoView({
            behavior: "smooth"
        });

}

</script>

</body>
</html>'''


def _edges_to_js(edges):
    """Ubah daftar EDGES Python menjadi literal array JavaScript."""
    lines = ["const EDGES = ["]
    for u, v, w in edges:
        u_js = u.replace("\\", "\\\\").replace('"', '\\"')
        v_js = v.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'    ["{u_js}", "{v_js}", {w}],')
    lines.append("];")
    return "\n".join(lines)


def generate_index_html(edges, out_path="index.html"):
    """
    Buat file index.html (versi web interaktif dari BFS Navigasi ITERA)
    menggunakan data EDGES yang sama persis dengan versi terminal,
    sehingga kedua versi selalu konsisten.
    """
    js_edges = _edges_to_js(edges)
    html_content = HTML_TEMPLATE.replace("__EDGES_JS_PLACEHOLDER__", js_edges)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return out_path


#  MAIN

def main():
    clear_screen()
    banner()

    graph       = build_graph(EDGES)
    nodes_sorted = sorted(graph.keys())

    # Ekspor versi web (index.html) agar program menghasilkan output tambahan
    # berupa halaman HTML interaktif, selain output terminal & PNG.
    html_path = generate_index_html(EDGES)
    print(C["success"] + f"  Versi web berhasil dibuat: " + C["path"] + html_path)
    print(C["muted"]   + "  Buka file tersebut di browser untuk mencoba versi interaktifnya.\n")

    while True:
        # Tampilkan daftar node
        print(C["header"] + "    DAFTAR LOKASI DI KAMPUS ITERA\n")
        print_node_list(nodes_sorted)

        # Input asal
        start = get_node_input(
            "Masukkan TITIK AWAL (asal):",
            nodes_sorted, "Titik Awal"
        )

        # Input tujuan
        goal = get_node_input(
            "Masukkan TITIK TUJUAN:",
            nodes_sorted, "Titik Tujuan"
        )

        if start == goal:
            print(C["warning"] + "\n  ⚠  Titik awal dan tujuan sama! Pilih lokasi berbeda.\n")
            continue

        # ── Jalankan BFS ──
        print()
        print(C["info"] + "  Menjalankan BFS...")
        path, visited_order, steps, parent = bfs(graph, start, goal)

        if path is None:
            print(C["error"] + f"\n    Tidak ada jalur dari '{start}' ke '{goal}'.\n")
        else:
            # ① Hasil rute
            print_route_result(path, graph, start, goal)

            # ② Tabel langkah BFS
            print_bfs_steps(steps, goal)

            # ③ Pohon BFS teks
            print_bfs_tree(parent, start, path)

            # ④ Visualisasi graf
            print(C["header"] + "    Membuat visualisasi graf...")
            visualize_graph(path, graph, start, goal, visited_order, parent)

        # Tanya ulangi
        print()
        hr()
        again = input(C["teal"] + "\n  Cari rute lain? (y/n): " + Style.RESET_ALL).strip().lower()
        if again not in ("y", "ya", "yes"):
            print()
            print(C["success"] + "  Terima kasih telah menggunakan BFS Navigasi ITERA! ")
            print()
            break

        clear_screen()
        banner()


if __name__ == "__main__":
    main()
