import copy


class TubesConfiguration:

    size_tubes = -1
    
    def __init__(self, tubes) -> None:
        self.tubes = tubes


    def ID(self):
        id=""
        for tube in self.tubes:
            for i,color in enumerate(tube):
                if color != '':
                    id+= color + '|'
            id+='-'
        
        return id
    
    def ID_to_configuration(id):
        configuration = []
        tubes = id.split('-')
        tubes.pop()
        for tube in tubes:
            configuration.append(['']*TubesConfiguration.size_tubes)

            for i, color in enumerate(tube.split('|')):
                if (i < TubesConfiguration.size_tubes):
                    configuration[-1][i] = color

        return TubesConfiguration(configuration)

    def check_validity(self):
        TubesConfiguration.size_tubes = -1

        for tube in self.tubes:
            if TubesConfiguration.size_tubes == -1:
                TubesConfiguration.size_tubes = len(tube)
            elif len(tube) != TubesConfiguration.size_tubes:
                print("The tubes does not have the same length")
                return False
        
        count_colors = {}
        
        for tube in self.tubes:
            for color in tube:
                try:
                    count_colors[color] += 1
                except KeyError:
                    count_colors[color] = 1
        
        for k in count_colors:
            #print(f"{k} {count_colors[k]}")
            if k != '' and count_colors[k] != TubesConfiguration.size_tubes:
                print("Not the right amount of ", k)
                return False
        
        return True
    
    def display(self):
        for i in range(TubesConfiguration.size_tubes -1, -1, -1):
            str = ""
            for tube in self.tubes:
                str += f"|{tube[i].ljust(2) if tube[i] != '' else '**'}"
            str +="|"
            print(str)
        
        str = ""
        for i,tube in enumerate(self.tubes):
            str +=f" {i.__str__().ljust(2)}"
        print(str)
                    
    def unfinished_tubes(self):
        unfinished_tubes = []

        for index_tube,tube in enumerate(self.tubes):
            color_reference = tube[0]

            if color_reference == '':
                unfinished_tubes.append(index_tube)
            
            for color in tube:
                if color != color_reference:
                    unfinished_tubes.append(index_tube)
                    break

        return unfinished_tubes
    
    def last_color_tube(self, id_tube):
        last_index = 0
        last_color = ''
        for index, color in enumerate(self.tubes[id_tube]):
            if color == '':
                return last_index,last_color
            last_color = color
            last_index = index
        
        return index, last_color
    
    def move(self, start_tube, end_tube):

        #if start tube empty
        if self.tubes[start_tube][0] == '':
            return None

        #last_color[0] -> last position
        #last_color[1] -> color
        last_color_end = self.last_color_tube(end_tube)

        # if end tube full
        if last_color_end[0] == TubesConfiguration.size_tubes -1:
            return None

        last_color_start = self.last_color_tube(start_tube)

        #if start and end color are differents
        if last_color_start[1] != last_color_end[1] and last_color_end[1] != '':
            return None 

        if last_color_end[1] == '':
            self.tubes[end_tube][0] = last_color_start[1]
        else:
            self.tubes[end_tube][last_color_end[0]+1] = last_color_start[1]

        self.tubes[start_tube][last_color_start[0]] = ''
        
        self.move(start_tube, end_tube)

        return self

class tubes_puzzle_solver:

    MAX_DEPTH = 20

    def __init__(self, tubes_configuration):
        self.configuration_present = []

        self.tubes_configuration = tubes_configuration
        self.Ids_Solutions = []

        ### key -> configuration_key
        ### value -> [mother configuration,depth]
        self.configurations_IDs_dict = {}

    def solve(self):
        self.configuration_present.append(self.tubes_configuration)

        solution_ID = self._solver(0)

        compt = 0
        while solution_ID in self.configurations_IDs_dict.keys():
            compt += 1
            TubesConfiguration.ID_to_configuration(solution_ID).display()
            print()
            solution_ID = self.configurations_IDs_dict[solution_ID]
        TubesConfiguration.ID_to_configuration(solution_ID).display()

        print("Solution with",compt,"steps")


    def _solver(self, depth):
        print(depth, len(self.configuration_present))

        configuration_sons = []

        if depth > tubes_puzzle_solver.MAX_DEPTH:
            return None
            
        for configuration in self.configuration_present:
            configuration_ID = configuration.ID()

            unfinished_tubes = configuration.unfinished_tubes()

            if len(unfinished_tubes) == 2:            
                return configuration_ID

            for i in unfinished_tubes:
                for j in unfinished_tubes:
                    if i!=j:
                        
                        new_configuration = TubesConfiguration( copy.deepcopy(configuration.tubes) )
                        new_configuration = new_configuration.move(i,j)

                        if new_configuration != None:
                            new_configuration_ID = new_configuration.ID()

                            if new_configuration_ID not in self.configurations_IDs_dict.keys():
                                self.configurations_IDs_dict[new_configuration_ID] = configuration_ID
                                configuration_sons.append(new_configuration)

        self.configuration_present = configuration_sons
        return self._solver(depth+1)
                


if __name__ == "__main__":
    # G  -> Green
    # Y  -> yellow
    # P  -> Pink
    # LO -> Light Orange
    # Pu -> Purple
    # Gr -> Gray
    # O  -> Orange
    # LG -> Light Green
    # LB -> Light Blue
    # B  -> Brown
    # R  -> Red 

    tubes3 = [
        ['O','B','O'],
        ['B','B','O'],
        ['','',''],
        ['','','']
    ]
    
    tubes2 = [
        ['O','R','O','B'],
        ['Y','B','Y','B'],
        ['R','G','Y','O'],
        ['G','R','O','G'],
        ['Gr','Gr','Gr','Y'],
        ['R','G','Gr','B'],
        ['','','',''],
        ['','','','']
    ]

    tubes1 = [
        ['G','Y','G','P','LO'],
        [ 'Pu','LO','Gr','LO','Y'],
        [ 'O','Pu','P','O','Gr'],
        [ 'Y','G','LB','LG','LG'],
        [ 'O','P','LO','LB','LB'],
        [ 'P','LG','O','LB','Pu'],
        [ 'Pu','Gr','Gr','Pu','G'],
        [ 'Y','LB','P','LG','Y'],
        [ 'LG','G','LO','O','Gr'],
        [ '','','','',''],
        [ '','','','','']
    ]

    configuration = TubesConfiguration(tubes3)
    if configuration.check_validity():
        configuration.display()

        solver = tubes_puzzle_solver(configuration)
        solver.solve()
