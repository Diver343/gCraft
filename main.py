import tkinter as tk
import random
import noise

# Constants
TILE_SIZE = 40
VISIBLE_WIDTH = 14
VISIBLE_HEIGHT = 8
CHUNK_SIZE = 10

# Perlin noise settings
SCALE = 100.0
OCTAVES = 6
PERSISTENCE = 0.5
LACUNARITY = 2.0

# Colors for different elements
COLORS = {
    'water': 'blue',
    'sand': 'yellow',
    'grass': 'green',
    'forest': 'darkgreen',
    'rock': 'gray',
    'mountain': 'white',
    'tree': 'darkgreen',
    'player': 'red'
}

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Infinite World Game")

# Create the canvas to draw the game world
canvas = tk.Canvas(root, width=VISIBLE_WIDTH * TILE_SIZE, height=VISIBLE_HEIGHT * TILE_SIZE)
canvas.pack()

# Initialize the player's position and inventory
player_pos = [0, 0]
inventory = [''] * 9  # Empty inventory with 9 slots

# Function to generate a chunk of the world with terrain features
def generate_chunk(cx, cy):
    chunk = []
    for y in range(CHUNK_SIZE):
        row = []
        for x in range(CHUNK_SIZE):
            nx = (cx * CHUNK_SIZE + x) / SCALE
            ny = (cy * CHUNK_SIZE + y) / SCALE
            noise_value = noise.pnoise2(nx, ny, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
            
            if noise_value < -0.1:
                tile_type = 'water'
            elif noise_value < 0.0:
                tile_type = 'sand'
            elif noise_value < 0.4:
                tile_type = 'grass'
            elif noise_value < 0.6:
                tile_type = 'forest'
            elif noise_value < 0.8:
                tile_type = 'rock'
            else:
                tile_type = 'mountain'

            # Add trees with a certain probability on grass and forest tiles
            if tile_type in ['grass', 'forest'] and random.random() < 0.1:  # 10% chance to add a tree
                tile_type = 'tree'
            
            row.append(tile_type)
        chunk.append(row)
    return chunk

# Function to get a tile from the world
def get_tile(x, y):
    cx, tx = divmod(x, CHUNK_SIZE)
    cy, ty = divmod(y, CHUNK_SIZE)
    if (cx, cy) not in world:
        world[(cx, cy)] = generate_chunk(cx, cy)
    return world[(cx, cy)][ty][tx]

# Function to draw the world map on the canvas
def draw_world():
    canvas.delete("all")
    px, py = player_pos
    start_x = px - VISIBLE_WIDTH // 2
    start_y = py - VISIBLE_HEIGHT // 2
    for y in range(VISIBLE_HEIGHT):
        for x in range(VISIBLE_WIDTH):
            wx = start_x + x
            wy = start_y + y
            tile = get_tile(wx, wy)
            color = COLORS.get(tile, 'white')  # Default to white if tile type is not found
            canvas.create_rectangle(
                x * TILE_SIZE, y * TILE_SIZE,
                (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE,
                fill=color, outline='black'
            )
            # Debug print for tile types
            print(f"Tile at ({wx}, {wy}) is {tile} with color {color}")

    # Draw the player
    canvas.create_rectangle(
        (VISIBLE_WIDTH // 2) * TILE_SIZE, (VISIBLE_HEIGHT // 2) * TILE_SIZE,
        (VISIBLE_WIDTH // 2 + 1) * TILE_SIZE, (VISIBLE_HEIGHT // 2 + 1) * TILE_SIZE,
        fill=COLORS['player'], outline='black'
    )

# Function to move the player
def move_player(dx, dy):
    player_pos[0] += dx
    player_pos[1] += dy
    draw_world()

# Draw the initial world
world = {}
draw_world()

# Create movement buttons
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text='Up', command=lambda: move_player(0, -1)).grid(row=0, column=1)
tk.Button(frame, text='Left', command=lambda: move_player(-1, 0)).grid(row=1, column=0)
tk.Button(frame, text='Down', command=lambda: move_player(0, 1)).grid(row=1, column=1)
tk.Button(frame, text='Right', command=lambda: move_player(1, 0)).grid(row=1, column=2)

# Function to handle inventory display
def draw_inventory():
    inv_frame.delete("all")
    for i, item in enumerate(inventory):
        x = i * TILE_SIZE  # Position items horizontally
        color = COLORS.get(item, 'white')  # Use item color or default to white
        inv_frame.create_rectangle(
            x, 0,
            x + TILE_SIZE, TILE_SIZE,
            fill=color, outline='black'
        )

# Create inventory display frame
inv_frame = tk.Canvas(root, width=9 * TILE_SIZE, height=TILE_SIZE)
inv_frame.pack()

# Draw initial inventory
draw_inventory()

# Start the Tkinter event loop
root.mainloop()
