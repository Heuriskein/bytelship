import logging
import bnf


class Executor(object):
    def __init__(self, start_loc):
        self.registers = {
            'a': 0,
            'b': 0,
            'i': start_loc,
        }
        self.next_instruction = None
        self.crashed = False

    def prep_instruction(self, memory_space):
        self.next_instruction = memory_space[self.registers['i']]

    def increment_i(self):
        self.registers['i'] += 1

    def execute_instruction(self, memory_space):
        logging.warning("Executing instruction %s", self.next_instruction)
        parser = bnf.get_parser()
        parser.memory_space = memory_space
        parser.registers = self.registers
        result = parser.parse(self.next_instruction)
        if result[0] == 'noop':
            pass
        if result[0] == 'crash':
            self.crashed = True
        if result[0] == 'write':
            memory_space[result[2] % Game.MEMORY_SIZE] = result[1]
        if result[0] == 'store':
            self.registers[result[2]] = result[1]

    def check_alive(self):
        if self.crashed: 
            return False
        if self.registers['i'] >= Game.MEMORY_SIZE:
            return False
        return True
    
class Game(object):
    MEMORY_SIZE = 4096
    MAX_TURNS = 1 << 20
    def __init__(self, filename1, filename2):
        self.turn = 0
        self.memory_space = ['crash'] * Game.MEMORY_SIZE

        file1_contents = [x.strip() for x in open(filename1, 'r').readlines()]
        file1_len = len(file1_contents)
        file2_contents = [x.strip() for x in open(filename2, 'r').readlines()]
        file2_len = len(file2_contents)

        loc1, loc2 = self.select_starting_locations(file1_len, file2_len)

        self.executor1 = self.create_executor(file1_contents, loc1)
        self.executor2 = self.create_executor(file2_contents, loc2)

    @staticmethod
    def select_starting_locations(len1, len2):
        import random
        valid = False
        logging.warning("Selecting starting locations for lengths %d %d", len1, len2)
        while not valid:
            start1 = random.randint(0, Game.MEMORY_SIZE - 1)
            start2 = random.randint(0, Game.MEMORY_SIZE - 1)
            logging.warning("Attempting to choose starting locations %d %d", start1, start2)
            overlap = set(range(start1, start1 + len1)).intersection(set(range(start2, start2 + len2)))
            if (start1 + len1 <= Game.MEMORY_SIZE and
                    start2 + len2 <= Game.MEMORY_SIZE and
                    not overlap):
                valid = True
            else:
                logging.warning("failed")


        return start1, start2
    
    def create_executor(self, program, location):
        for i in range(len(program)):
            write_loc = i + location
            assert self.memory_space[write_loc] == 'crash'
            self.memory_space[write_loc] = program[i]
        return Executor(location)

    def execute_turn(self):
        self.turn += 1
        logging.warning("Beginning turn %s", self.turn)
        self.executor1.prep_instruction(self.memory_space)
        self.executor2.prep_instruction(self.memory_space)
        self.executor1.increment_i()
        self.executor2.increment_i()
        self.executor1.execute_instruction(self.memory_space)
        self.executor2.execute_instruction(self.memory_space)

        executor1_alive = self.executor1.check_alive()
        executor2_alive = self.executor2.check_alive()
        
        if not executor1_alive and not executor2_alive:
            return 'Draw'
        if not executor1_alive:
            return '2 wins'
        if not executor2_alive:
            return '1 wins'

        if self.turn > Game.MAX_TURNS:
            return 'Draw'

        return None
        
    def execute_game(self):
        result = None
        while not result:
            result = self.execute_turn()
        return result

if __name__ == '__main__':
    logging.warning("Starting")
    import sys
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    game = Game(file1, file2)
    logging.warning(game.execute_game())