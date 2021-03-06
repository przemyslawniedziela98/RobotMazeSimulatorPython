# df_maze.py
import random
from PIL import Image, ImageDraw

class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        
    def has_all_walls(self):
        return all(self.walls.values())
    
    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

class Maze:
    def __init__(self, nx, ny, ix=0, iy=0):
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        
    def cell_at(self, x, y):
        return self.maze_map[x][y]
    
    def create_output_file(self, filename, wall_diam, line_width):
        self.wall_diam, self.line_width = wall_diam, line_width
        height, width = self.ny * self.wall_diam + 2*self.line_width, self.nx * self.wall_diam+ 2*self.line_width

        im = Image.new("RGB", (height, width), (255,255,255)) 
        draw = ImageDraw.Draw(im)
        draw.line([(self.line_width/2, self.line_width/2), (self.line_width/2,height-self.line_width )], fill =(0,0,0), width = self.line_width)
        draw.line([(self.line_width/2, self.line_width/2), (width-self.line_width- self.wall_diam, self.line_width/2)], fill =(0,0,0), width = self.line_width)
        for x in range(self.nx):
            for y in range(self.ny):
                if self.cell_at(x, y).walls['S']:
                    x1, y1, x2, y2 = x * self.wall_diam, (y + 1) * self.wall_diam, (x + 1) * self.wall_diam, (y + 1) * self.wall_diam
                    if x == 0 and y == self.ny-1:
                        continue
                    else:
                        draw.line([(x1+self.line_width, y1+self.line_width), (x2+self.line_width, y2+self.line_width)], fill =(0,0,0), width = self.line_width)
                if self.cell_at(x, y).walls['E']:
                    x1, y1, x2, y2 = (x + 1) * self.wall_diam, y * self.wall_diam, (x + 1) * self.wall_diam, (y + 1) * self.wall_diam
                    if x == 0 and y == self.ny-1:
                        continue
                    else:
                       draw.line([(x1+self.line_width, y1+self.line_width), (x2+self.line_width, y2+self.line_width)], fill =(0,0,0), width = self.line_width)
        im.save(filename, "PNG")

    def find_valid_neighbours(self, cell):
        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        nv = 1
        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)
            if not neighbours:
                current_cell = cell_stack.pop()
                continue
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1


