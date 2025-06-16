import matplotlib.pyplot as plt
import networkx as nx

# BAGIAN 1: DEFINISI MASALAH (CSP)
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
domains = {
    'WA': ['red', 'green', 'blue'], 'NT': ['red', 'green', 'blue'],
    'SA': ['red', 'green', 'blue'], 'Q': ['red', 'green', 'blue'],
    'NSW': ['red', 'green', 'blue'], 'V': ['red', 'green', 'blue'],
    'T': ['red', 'green', 'blue'],
}
adjacency = {
    'WA': ['NT', 'SA'], 'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'], 'V': ['SA', 'NSW'], 'T': []
}

# BAGIAN 2: FUNGSI ALGORITMA DAN VISUALISASI
def is_consistent(variable, color, assignment, adj):
    for neighbor in adj[variable]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtracking_search(variables, domains, adj, assignment={}):
    if len(assignment) == len(variables):
        return assignment
    unassigned_vars = [v for v in variables if v not in assignment]
    if not unassigned_vars: # Tambahan untuk keamanan
        return assignment
    variable = unassigned_vars[0]
    for color in domains[variable]:
        if is_consistent(variable, color, assignment, adj):
            assignment[variable] = color
            result = backtracking_search(variables, domains, adj, assignment)
            if result is not None:
                return result
            del assignment[variable]
    return None

def draw_map_graph(solution, adj):
    """Fungsi untuk menggambar graf jaringan dengan layout manual."""
    G = nx.Graph()
    # Pastikan semua variabel dari masalah ada di graf, bahkan jika solusi tidak lengkap
    G.add_nodes_from(variables) 
    
    for node, neighbors in adj.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
            
    # Definisikan posisi (x,y) setiap node secara manual
    pos = {
        'WA': (-3, 0), 'NT': (-1, 1.5), 'SA': (0, 0), 
        'Q': (1, 1.5), 'NSW': (1.5, -1), 'V': (0.5, -2), 
        'T': (0.5, -3.5)
    }
    
    # Siapkan warna untuk setiap node, jika node tidak ada di solusi (jarang terjadi), beri warna abu-abu
    node_colors = [solution.get(node, 'gray') for node in G.nodes()]
    
    plt.figure(figsize=(10, 8)) 
    nx.draw(G, pos, 
            with_labels=True, node_color=node_colors, node_size=3000,          
            font_size=12, font_color='white', font_weight='bold',      
            width=2.5, edge_color='black')       

    plt.title('Visualisasi Graf Pewarnaan Peta Australia (Layout Manual)', fontsize=16)
    # Atur batas plot agar semua node terlihat
    plt.xlim(-4, 3)
    plt.ylim(-4, 3)
    plt.show()


# BAGIAN 3: EKSEKUSI PROGRAM
print("Mencari solusi pewarnaan Peta Australia menggunakan Backtracking Search...")
solution_from_algorithm = backtracking_search(list(variables), domains, adjacency, {})

print("\n" + "="*20 + " HASIL PENCARIAN ALGORITMA " + "="*20)
if solution_from_algorithm:
    print("Solusi ditemukan oleh algoritma!")
    for variable, color in sorted(solution_from_algorithm.items()):
        print(f"  -> Wilayah {variable}: {color.capitalize()}")
    
    # Panggil fungsi untuk menggambar graf
    print("\nMenampilkan visualisasi graf...")
    draw_map_graph(solution_from_algorithm, adjacency)
else:
    print("Tidak ditemukan solusi yang valid.")