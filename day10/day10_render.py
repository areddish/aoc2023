from PIL import Image, ImageDraw

def render(board, W, H, path):
    multiplier = 5
    image = Image.new("RGB", (W*multiplier, H*multiplier))
    draw = ImageDraw.Draw(image)
    for y in range(H):
        for x in range(W):
            color = "gray"
            if x in path[y]:
                color = "yellow"
            else:
                if board[y][x] == ".":
                    color = "red"
                elif board[y][x] == "I":
                    color = "green"
            x1 = x*multiplier
            y1 = y*multiplier            
            draw.rectangle([x1,y1,x1+multiplier,y1+multiplier], fill=color)
    image.show()
    image.save("day10.png")
