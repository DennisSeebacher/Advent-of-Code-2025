from random import choice
from classes import Coordinate, Edge

class DrawCommand:

    Colors = ['red', 'green', 'blue', 'yellow', 'pink']

    def __init__(self, colour = None):
        if colour is not None:
            self.colour = colour
        else:
            self.colour = self.random_colour()

    def random_colour(self):
        return choice(DrawCommand.Colors)

class DrawCoordinates(DrawCommand):
    def __init__(self, coordinates:list[Coordinate], colour:str = None, radius:float = 1.0, draw_id:bool = False):
        super().__init__(colour)
        self.coordinates = coordinates
        self.radius = radius
        self.draw_id = draw_id

class DrawEdges(DrawCommand):
    def __init__(self, edges:list[Edge], colour:str = None, width:float = 0.5):
        super().__init__(colour)
        self.edges = edges
        self.width = width

def draw_svg(filename:str, borders:list[int], drawcommands:list[DrawCommand] = []):
    if filename is None or filename.strip() == '':
        raise ValueError('filename may not be None or empty')
    
    if len(drawcommands) == 0:
        return
    
    #creating static svg elements

    padding = 1280
    svg_head = '<?xml version="1.0" encoding="UTF-8"?>' + "\n"
    svg_head += '<svg xmlns="http://www.w3.org/2000/svg"' + "\n"
    svg_head += 'version="1.1" baseProfile="full"' + "\n"
    svg_head += f'width="1000px" height="1000px" viewBox="{borders[0]-padding} {borders[1]-padding} {borders[2]-borders[0]+2*padding} {borders[3]-borders[1]+2*padding}"' + "\n"
    svg_head += 'style="background: #eee;">' + "\n"
    svg_head += " " + "\n"

    svg_end = "</svg>"

    # creating the dynamic content

    svg_body = ''

    for drawcommand in drawcommands:
        if type(drawcommand) == DrawEdges:
            for edge in drawcommand.edges:
                svg_body += f'  <line x1="{edge.start.column}" y1="{edge.start.row}" x2="{edge.end.column}" y2="{edge.end.row}" style="stroke:{drawcommand.colour}; stroke-width:{drawcommand.width};" />' + "\n"
                svg_body += f'  <text x="{edge.center.column}" y="{edge.center.row}" fill="black" style="font-size:{drawcommand.width*drawcommand.width};">{edge.direction}</text>' + "\n"

        if type(drawcommand) == DrawCoordinates:
            for coordinate in drawcommand.coordinates:
                svg_body += f'  <circle cx="{coordinate.column}" cy="{coordinate.row}" r ="{drawcommand.radius}" fill="{drawcommand.colour}"/>' + "\n"
            if drawcommand.draw_id:
                for coordinate in drawcommand.coordinates:
                    svg_body += f'  <text x="{coordinate.column}" y="{coordinate.row}" fill="black" style="font-size:{drawcommand.radius*drawcommand.radius};">{coordinate.id}</text>' + "\n"


        svg_body += "\n"

    # finalizing

    svg_representation = svg_head + "\n" + svg_body+ "\n" + svg_end

    with open(filename, "w") as file:
        file.write(svg_representation)