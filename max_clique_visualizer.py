import pygame
import sys
import math
import random
import numpy as np

# --- Modern Configuration (Dribbble Style) ---
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

# Palette
BG_COLOR = (15, 23, 42)       # Deep Dark Blue/Slate
SIDEBAR_COLOR = (30, 41, 59)  # Lighter Slate
PANEL_COLOR = (23, 32, 50)    # Darker Panel
ACCENT_CYAN = (6, 182, 212)   # Cyan
ACCENT_PURPLE = (139, 92, 246)# Violet
ACCENT_GREEN = (16, 185, 129) # Emerald
ACCENT_RED = (239, 68, 68)    # Red
ACCENT_YELLOW = (234, 179, 8) # Yellow/Amber
TEXT_WHITE = (248, 250, 252)
TEXT_GRAY = (148, 163, 184)
HIGHLIGHT_BG = (51, 65, 85)   # For pseudocode highlight

# Node Colors
NODE_DEFAULT = (203, 213, 225)
NODE_R = ACCENT_RED     # Current Clique
NODE_P = ACCENT_CYAN    # Candidates
NODE_X = (100, 116, 139)# Excluded
NODE_RESULT = ACCENT_GREEN

# Fonts
pygame.init()
pygame.mixer.init()

def get_font(size, bold=False):
    return pygame.font.SysFont("Segoe UI", size, bold=bold)

font_title = get_font(28, bold=True)
font_header = get_font(20, bold=True)
font_body = get_font(16)
font_code = get_font(15) # Monospace-ish if possible, but Segoe UI is fine
font_small = get_font(14)

# --- Helper Functions ---
def draw_rounded_rect(surface, color, rect, radius=10):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def generate_beep(frequency=440, duration=0.1):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sound_array = (wave * 32767).astype(np.int16)
    stereo_array = np.column_stack((sound_array, sound_array))
    return pygame.sndarray.make_sound(stereo_array)

sound_step = generate_beep(440, 0.05)
sound_found = generate_beep(880, 0.15)
sound_finish = generate_beep(1200, 0.3)

# --- Classes ---

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.radius = 22
        self.target_radius = 22
        self.color = NODE_DEFAULT
        self.target_color = NODE_DEFAULT
        
    def update(self):
        self.radius += (self.target_radius - self.radius) * 0.2
        
    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,0, 50), (self.x+2, self.y+2), self.radius)
        pygame.draw.circle(surface, self.color, (self.x, self.y), int(self.radius))
        text = font_small.render(str(self.id), True, BG_COLOR)
        rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, rect)

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = set()
        self.next_id = 1
        self.max_clique = []
        self.recursion_stack = []

    def add_node(self, x, y):
        for node in self.nodes:
            if math.hypot(node.x - x, node.y - y) < 50: return
        self.nodes.append(Node(self.next_id, x, y))
        self.next_id += 1

    def remove_node(self, node):
        if node in self.nodes:
            self.edges = {(u, v) for u, v in self.edges if u != node.id and v != node.id}
            self.nodes.remove(node)
            self.reset_visuals()

    def add_edge(self, n1, n2):
        if n1.id == n2.id: return
        u, v = sorted((n1.id, n2.id))
        if (u, v) in self.edges: self.edges.remove((u, v))
        else: self.edges.add((u, v))
        self.reset_visuals()

    def get_node_at(self, x, y):
        for node in self.nodes:
            if math.hypot(node.x - x, node.y - y) <= node.radius: return node
        return None

    def get_neighbors(self, node_id):
        neighbors = set()
        for u, v in self.edges:
            if u == node_id: neighbors.add(v)
            elif v == node_id: neighbors.add(u)
        return neighbors

    def reset_visuals(self):
        self.max_clique = []
        self.recursion_stack = []
        for node in self.nodes:
            node.color = NODE_DEFAULT
            node.target_radius = 22

    def run_instant(self):
        self.reset_visuals()
        all_nodes = {node.id for node in self.nodes}
        results = []
        def bk(R, P, X):
            if not P and not X:
                results.append(R)
                return
            for v in list(P):
                neighbors = self.get_neighbors(v)
                bk(R.union({v}), P.intersection(neighbors), X.intersection(neighbors))
                P.remove(v)
                X.add(v)
        bk(set(), all_nodes, set())
        if results:
            max_c = max(results, key=len)
            self.max_clique = list(max_c)
            for node in self.nodes:
                if node.id in self.max_clique:
                    node.color = NODE_RESULT
        return len(self.max_clique)

    def run_step_by_step(self):
        """Generator Bron-Kerbosch with Educational Info"""
        self.reset_visuals()
        all_nodes = {node.id for node in self.nodes}
        
        # Pseudocode Lines
        # 1: BronKerbosch(R, P, X):
        # 2:   if P and X are both empty:
        # 3:     Report R as a maximal clique
        # 4:   for each vertex v in P:
        # 5:     BronKerbosch(R U {v}, P ^ N(v), X ^ N(v))
        # 6:     P := P \ {v}
        # 7:     X := X U {v}
        
        def bk_gen(R, P, X, depth=0):
            # Update Stack
            stack_info = f"Depth {depth}: R={list(R)}, P={list(P)}"
            if len(self.recursion_stack) <= depth: self.recursion_stack.append(stack_info)
            else: self.recursion_stack[depth] = stack_info
            self.recursion_stack = self.recursion_stack[:depth+1]

            yield {
                'R': R, 'P': P, 'X': X, 'depth': depth, 
                'line': 1, 
                'narrative': f"Memanggil fungsi BronKerbosch pada kedalaman {depth}. R={list(R)}, P={list(P)}, X={list(X)}"
            }

            yield {
                'R': R, 'P': P, 'X': X, 'depth': depth, 
                'line': 2, 
                'narrative': "Mengecek apakah P (Kandidat) dan X (Excluded) kosong?"
            }

            if not P and not X:
                yield {
                    'R': R, 'P': P, 'X': X, 'depth': depth, 
                    'line': 3, 
                    'narrative': f"P dan X kosong! Ditemukan Maximal Clique: {list(R)}"
                }
                
                if len(R) > len(self.max_clique):
                    self.max_clique = list(R)
                    yield {
                        'R': R, 'P': P, 'X': X, 'depth': depth, 'found': True, 
                        'line': 3, 
                        'narrative': f"Clique ini ({list(R)}) adalah yang TERBESAR sejauh ini!"
                    }
                return

            P_copy = list(P)
            yield {
                'R': R, 'P': P, 'X': X, 'depth': depth, 
                'line': 4, 
                'narrative': f"Melakukan iterasi untuk setiap node v di P: {P_copy}"
            }

            for v in P_copy:
                yield {
                    'R': R, 'P': P, 'X': X, 'depth': depth, 'curr': v, 
                    'line': 4, 
                    'narrative': f"Memilih node {v} dari P untuk diproses."
                }
                
                neighbors = self.get_neighbors(v)
                yield {
                    'R': R, 'P': P, 'X': X, 'depth': depth, 'curr': v, 
                    'line': 5, 
                    'narrative': f"Rekursi: Menambahkan {v} ke R. Filter P dan X hanya tetangga dari {v} ({list(neighbors)})."
                }

                yield from bk_gen(
                    R.union({v}),
                    P.intersection(neighbors),
                    X.intersection(neighbors),
                    depth + 1
                )
                
                P.remove(v)
                X.add(v)
                yield {
                    'R': R, 'P': P, 'X': X, 'depth': depth, 'curr': v, 
                    'line': 6, 
                    'narrative': f"Kembali dari rekursi. Pindahkan {v} dari P ke X (sudah diproses)."
                }

        yield from bk_gen(set(), all_nodes, set())
        yield {'finished': True, 'line': -1, 'narrative': "Algoritma Selesai. Hasil Maximum Clique ditampilkan."}

    def generate_random(self):
        self.nodes = []
        self.edges = set()
        self.next_id = 1
        count = random.randint(6, 10)
        for _ in range(count):
            for _ in range(50):
                x = random.randint(50, SCREEN_WIDTH - 450) # Adjusted for wider sidebar
                y = random.randint(80, SCREEN_HEIGHT - 200) # Adjusted for bottom panel
                if all(math.hypot(n.x-x, n.y-y) > 60 for n in self.nodes):
                    self.nodes.append(Node(self.next_id, x, y))
                    self.next_id += 1
                    break
        ids = [n.id for n in self.nodes]
        for i in range(len(ids)):
            for j in range(i+1, len(ids)):
                if random.random() < 0.35:
                    self.add_edge(self.nodes[i], self.nodes[j])

class ModernButton:
    def __init__(self, x, y, w, h, text, color, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = color
        self.hover_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255))
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.base_color
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        draw_rounded_rect(surface, (0,0,0, 100), shadow_rect, 8)
        draw_rounded_rect(surface, color, self.rect, 8)
        txt = font_body.render(self.text, True, TEXT_WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def click(self, pos):
        return self.action if self.is_hovered else None

# --- Global State ---
graph = Graph()
selected_node = None
mode = "STEP"
algo_gen = None
algo_state = None
is_running = False
is_paused = False
last_step_time = 0
STEP_DELAY = 1000 # Slower for reading

# Buttons
btn_x = SCREEN_WIDTH - 380
btn_w = 360
btn_y = 50
buttons = [
    ModernButton(btn_x, btn_y, btn_w, 45, "RANDOM GRAPH", ACCENT_CYAN, "random"),
    ModernButton(btn_x, btn_y + 60, btn_w, 45, "QUICK RUN (Instant)", ACCENT_PURPLE, "quick"),
    ModernButton(btn_x, btn_y + 120, btn_w, 45, "STEP RUN (Auto)", ACCENT_GREEN, "step"),
    ModernButton(btn_x, btn_y + 180, btn_w, 45, "PAUSE / RESUME", ACCENT_YELLOW, "pause"),
    ModernButton(btn_x, btn_y + 240, btn_w, 45, "NEXT STEP (Manual)", (255, 100, 50), "next"),
    ModernButton(btn_x, btn_y + 300, btn_w, 45, "RESET", ACCENT_RED, "reset"),
]

pseudocode = [
    "def BronKerbosch(R, P, X):",
    "    if not P and not X:",
    "        Report R as maximal clique",
    "    for v in list(P):",
    "        BronKerbosch(R ∪ {v}, P ∩ N(v), X ∩ N(v))",
    "        P = P \ {v}",
    "        X = X ∪ {v}"
]

def handle_action(act):
    global is_running, is_paused, algo_gen, algo_state, mode, last_step_time
    
    if act == "random":
        reset_all()
        graph.generate_random()
    elif act == "quick":
        reset_all()
        mode = "NORMAL"
        graph.run_instant()
        sound_finish.play()
    elif act == "step":
        reset_all()
        mode = "STEP"
        algo_gen = graph.run_step_by_step()
        is_running = True
        is_paused = False
    elif act == "pause":
        if is_running: is_paused = not is_paused
    elif act == "next":
        if is_running and is_paused:
            step_once()
    elif act == "reset":
        reset_all()

def reset_all():
    global is_running, is_paused, algo_gen, algo_state, selected_node
    is_running = False
    is_paused = False
    algo_gen = None
    algo_state = None
    selected_node = None
    graph.reset_visuals()

def step_once():
    global algo_state, is_running, last_step_time
    try:
        algo_state = next(algo_gen)
        sound_step.play()
        if algo_state.get('found'): sound_found.play()
        if algo_state.get('finished'): 
            is_running = False
            sound_finish.play()
            for node in graph.nodes:
                if node.id in graph.max_clique:
                    node.color = NODE_RESULT
        last_step_time = pygame.time.get_ticks()
    except StopIteration:
        is_running = False

def draw_ui(surface):
    surface.fill(BG_COLOR)
    
    # Sidebar
    sidebar_rect = pygame.Rect(SCREEN_WIDTH - 400, 0, 400, SCREEN_HEIGHT)
    pygame.draw.rect(surface, SIDEBAR_COLOR, sidebar_rect)
    pygame.draw.line(surface, (50, 60, 80), (SCREEN_WIDTH - 400, 0), (SCREEN_WIDTH - 400, SCREEN_HEIGHT), 2)

    # Title
    title = font_title.render("Max Clique Visualizer", True, TEXT_WHITE)
    surface.blit(title, (20, 20))
    
    # Bottom Narrative Panel
    panel_rect = pygame.Rect(20, SCREEN_HEIGHT - 120, SCREEN_WIDTH - 440, 100)
    draw_rounded_rect(surface, PANEL_COLOR, panel_rect, 10)
    
    narrative = algo_state.get('narrative', "Siap untuk memulai...") if algo_state else "Siap untuk memulai. Klik tombol di kanan."
    # Wrap narrative text
    words = narrative.split(' ')
    lines = []
    curr_line = ""
    for word in words:
        test_line = curr_line + word + " "
        if font_header.size(test_line)[0] < panel_rect.width - 20:
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = word + " "
    lines.append(curr_line)
    
    ny = panel_rect.y + 15
    for line in lines:
        txt = font_header.render(line, True, ACCENT_CYAN)
        surface.blit(txt, (panel_rect.x + 15, ny))
        ny += 25

    # Pseudocode Panel (Sidebar)
    code_y = 400
    lbl = font_header.render("Pseudocode:", True, TEXT_WHITE)
    surface.blit(lbl, (SCREEN_WIDTH - 380, code_y))
    code_y += 30
    
    curr_line_num = algo_state.get('line', -1) if algo_state else -1
    
    for i, line in enumerate(pseudocode):
        line_num = i + 1
        rect = pygame.Rect(SCREEN_WIDTH - 390, code_y + (i*25), 380, 25)
        if line_num == curr_line_num:
            pygame.draw.rect(surface, HIGHLIGHT_BG, rect, border_radius=4)
            color = ACCENT_GREEN
        else:
            color = TEXT_GRAY
        
        txt = font_code.render(line, True, color)
        surface.blit(txt, (SCREEN_WIDTH - 380, code_y + (i*25) + 2))

    # Recursion Stack (Sidebar)
    stack_y = code_y + (len(pseudocode) * 25) + 30
    lbl = font_header.render("Recursion Stack:", True, ACCENT_PURPLE)
    surface.blit(lbl, (SCREEN_WIDTH - 380, stack_y))
    stack_y += 30
    
    if mode == "STEP" and graph.recursion_stack:
        for s in graph.recursion_stack[-6:]:
            stxt = font_small.render(s, True, (100, 100, 100))
            surface.blit(stxt, (SCREEN_WIDTH - 380, stack_y))
            stack_y += 20

    # Draw Graph
    for u_id, v_id in graph.edges:
        u = next((n for n in graph.nodes if n.id == u_id), None)
        v = next((n for n in graph.nodes if n.id == v_id), None)
        if u and v:
            color = (60, 70, 90)
            width = 2
            if algo_state:
                R = algo_state.get('R', set())
                if u.id in R and v.id in R:
                    color = ACCENT_RED
                    width = 4
            if u.color == NODE_RESULT and v.color == NODE_RESULT:
                color = ACCENT_GREEN
                width = 5
            pygame.draw.line(surface, color, (u.x, u.y), (v.x, v.y), width)

    for node in graph.nodes:
        node.update()
        if algo_state:
            R = algo_state.get('R', set())
            P = algo_state.get('P', set())
            X = algo_state.get('X', set())
            curr = algo_state.get('curr', None)
            if node.id == curr: node.color = TEXT_WHITE
            elif node.id in R: node.color = NODE_R
            elif node.id in P: node.color = NODE_P
            elif node.id in X: node.color = NODE_X
            else: node.color = NODE_DEFAULT
        elif not is_running and len(graph.max_clique) == 0:
             node.color = NODE_DEFAULT
        node.draw(surface)

    if selected_node:
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(surface, (100, 100, 100), (selected_node.x, selected_node.y), (mx, my), 1)

    for btn in buttons:
        btn.draw(surface)

    pygame.display.flip()

# --- Main Loop ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Max Clique Visualizer - Educational Mode")
clock = pygame.time.Clock()

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            for btn in buttons: btn.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = None
            for btn in buttons:
                res = btn.click(event.pos)
                if res: action = res
            
            if action:
                handle_action(action)
            elif event.pos[0] < SCREEN_WIDTH - 400:
                x, y = event.pos
                clicked = graph.get_node_at(x, y)
                if event.button == 1:
                    if clicked:
                        if selected_node:
                            graph.add_edge(selected_node, clicked)
                            selected_node = None
                        else:
                            selected_node = clicked
                    else:
                        graph.add_node(x, y)
                        selected_node = None
                elif event.button == 3:
                    if clicked: graph.remove_node(clicked)

    if is_running and not is_paused and mode == "STEP":
        if current_time - last_step_time > STEP_DELAY:
            step_once()

    draw_ui(screen)
    clock.tick(60)

pygame.quit()
sys.exit()
