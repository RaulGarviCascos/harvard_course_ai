import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
     
        from pprint import pprint

        pprint(self.crossword.variables)
      
        print('-------')
        self.ac3()
        pprint(self.domains)
        print('-------')
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for var in self.domains:
            word_set = self.crossword.words
            for word in word_set:
                if  len(word) != var.length:
                    self.domains[var].remove(word)
     


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        x_words = self.domains[x].copy()
        y_words = self.domains[y]
        revised = False
        new_x_words = []

        if self.crossword.overlaps[x,y]:
            for x_word in x_words:
                for y_word in y_words:
                    if x_word!=y_word and self.have_same_letter(x,y,x_word,y_word):
                        new_x_words.append(x_word)
                        revised = True
                        break

        if revised:
            self.domains[x] = new_x_words.copy()                        
        
        return revised
                
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """  
        if arcs is None:
            arcs = [arc for arc in self.crossword.overlaps if self.crossword.overlaps[arc] is not None]
        
        while len(arcs)>0:
            x,y = arcs.pop()
            if self.revise(x,y):
                if len(self.domains[x]) <=0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z is not y:
                        arcs.append((z,x))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables) and all(var is not None for var in assignment.values())
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #every word is different
        if len(assignment) != len(set(assignment.values())): return False

        for var in assignment:
            #unary constraint
            if len(assignment[var]) != var.length:
                return False
            #binary constraint
            var_neighbors = self.crossword.neighbors(var)
            for neighbor in var_neighbors:
                for n_word in self.domains[neighbor]:
                    if not self.have_same_letter(var,neighbor,assignment[var],n_word):
                        return False
        return True
                   
            
    def have_same_letter(self,x,y,x_word,y_word):

        square = self.crossword.overlaps[x,y]
        if square is None : return False
        letter_var = x_word[square[0]] 
        letter_neighbor = y_word[square[1]]  
        if letter_var==letter_neighbor:
            return True 
        return False 


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        var_domain = {}
        var_neighbors = self.crossword.neighbors(var)

        for word in self.domains[var]:
            conflictos = 0
            for neighbor in var_neighbors:
                if neighbor not in assignment: 
                    for neighbor_word in self.domains[neighbor]:
                        if not self.have_same_letter(var,neighbor,word,neighbor_word):
                            conflictos+=1

            var_domain[word] = conflictos

        return sorted(var_domain,key=lambda k:var_domain[k])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var_domain = {}
        for var in self.domains:
            if var not in assignment:
                n_words= len(self.domains[var])
                n_neighbors = self.crossword.neighbors(var)
                var_domain[var] = (n_words,n_neighbors)

        list_candidates = sorted(var_domain,key=lambda k:var_domain[k],reverse=True)

        return list_candidates.pop()

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment): return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            assignment[var] = value
            if not self.consistent(assignment):
                assignment.pop(var)
                continue
            result = self.backtrack(assignment)
            if result!= None:
                return result
            assignment.pop(var)
        
        return None
        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
