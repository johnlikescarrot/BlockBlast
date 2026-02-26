import sys

with open('src/scripts/scenes/MainScene.js', 'r') as f:
    content = f.read()

# Target 1: InsertPiece powerup handling
glow_logic_insert = """                        this.idleboard[j+x][i+y].setTexture(this.powerUpsList[piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1]).setTint(0xffffff).visible = true
                        if (this.idleboard[j+x][i+y].preFX) {
                            this.idleboard[j+x][i+y].preFX.clear();
                            let glowColor = piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j) == 1 ? 0xff4444 : 0x44ffff;
                            this.idleboard[j+x][i+y].preFX.addGlow(glowColor, 4, 0, False);
                        }"""

# Target 2: CreatePiece powerup handling
glow_logic_create = """                        let s1 = this.add.image((size*j)-(size*2),(size*i)-(size*2) , this.powerUpsList[piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1])
                        if (s1.preFX) {
                            s1.preFX.clear();
                            let glowColor = piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j) == 1 ? 0xff4444 : 0x44ffff;
                            s1.preFX.addGlow(glowColor, 4, 0, False);
                        }"""

# Target 3: ChangePointer powerup handling
glow_logic_pointer = """                        this.pointer[j][i].setTexture(this.powerUpsList[this.piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1])
                        if (this.pointer[j][i].preFX) {
                            this.pointer[j][i].preFX.clear();
                            let glowColor = this.piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j) == 1 ? 0xff4444 : 0x44ffff;
                            this.pointer[j][i].preFX.addGlow(glowColor, 4, 0, False);
                        }"""

# Simple replacements
content = content.replace("this.idleboard[j+x][i+y].setTexture(this.powerUpsList[piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1]).setTint(0xffffff).visible = true", glow_logic_insert)
content = content.replace("let s1 = this.add.image((size*j)-(size*2),(size*i)-(size*2) , this.powerUpsList[piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1])", glow_logic_create)
content = content.replace("this.pointer[j][i].setTexture(this.powerUpsList[this.piece.shape.charAt((JUICE_CONFIG.PIECE_DIMENSION * i)+j)-1])", glow_logic_pointer)

# Fixed case for Javascript 'false'
content = content.replace("False)", "false)")

with open('src/scripts/scenes/MainScene.js', 'w') as f:
    f.write(content)
