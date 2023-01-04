class SimpleGame:

    def __init__(self) -> None:
        self.array = ['S', 'X', 'X', 'X', 'X', 'G']
        self.pointer = 0

    def move_left(self) -> None:
        if self.pointer > 0:
            # update the array
            self.array[self.pointer] = 'X'
            self.array[self.pointer - 1] = 'S'
            self.pointer -= 1
        else:
            # do nothing
            pass
        
        return None
    
    
    def move_right(self) -> None:
        if self.pointer < len(self.array) - 1:
            # update the array
            self.array[self.pointer] = 'X'
            self.array[self.pointer + 1] = 'S'
            self.pointer += 1
            return self.check_win()
        else:
            # do nothing
            pass
        
        return None

    def check_win(self) -> bool:
        return self.array[-1] == 'S'
    
    def get_array(self) -> list:
        return self.array
    
    def get_pointer(self) -> int:
        return self.pointer
    
    def print_state(self) -> None:
        for i in self.array:
            if i == "X":
                print("_", end=" ")
            else:
                print(i, end=" ")
        print()


if __name__ == "__main__":
    a = SimpleGame()
    a.print_state()
    a.move_left()
    a.print_state()
    a.move_right()
    a.print_state()
    a.move_right()
    a.print_state()
    a.move_right()
    a.print_state()
    a.move_right()
    a.print_state()
    val = a.move_right()
    a.print_state()
    if val == True:
        print("You won!")

            
