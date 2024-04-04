import copy


class TubesConfiguration:
    
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
            configuration.append( tube.split('|'))
            configuration[-1].pop()

            for i in range(0,TubesConfiguration.size_tubes-len(tube)):
                configuration[-1].append('')

        print(configuration)

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
        for i in range(len(self.tubes[0])-1, -1, -1):
            str = ""
            for tube in self.tubes:
                str += f"|{tube[i].ljust(2) if tube[i] != '' else '**'}"
            str +="|"
            print(str)
        
        str = ""
        for i,tube in enumerate(self.tubes):
            str +=f" {i.__str__().ljust(2)}"
        print(str)
        print()
                    
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
        self.tubes_configuration = tubes_configuration
        self.Ids_Solutions = []

        ### key -> configuration_key
        ### value -> [mother configuration,depth]
        self.configurations_IDs_dict = {}

    def solve(self):
        self._solver(self.tubes_configuration, 0)

        ID_solution_min = self.Ids_Solutions[0]
        nb_play_minimum = 1000

        for solution in self.Ids_Solutions:

            ID_solution = solution
            compt = 0

            while ID_solution in self.configurations_IDs_dict.keys():
                ID_solution = self.configurations_IDs_dict[ID_solution][0]
                compt += 1

            if compt < nb_play_minimum:
                ID_solution_min = solution
                nb_play_minimum = compt

        print(nb_play_minimum," plays min found")
        
        while ID_solution_min in self.configurations_IDs_dict.keys():
            print(ID_solution_min)
            ID_solution_min = self.configurations_IDs_dict[ID_solution_min][0]
            
        TubesConfiguration.ID_to_configuration(self.Ids_Solutions[0])



    def _solver(self, configuration, depth):
        if depth > tubes_puzzle_solver.MAX_DEPTH:
            return

        unfinished_tubes = configuration.unfinished_tubes()

        if len(unfinished_tubes) == 2:            
            self.Ids_Solutions.append(configuration.ID())
            
        
        for i in unfinished_tubes:
            for j in unfinished_tubes:

                if i!=j:

                    new_configuration = TubesConfiguration( copy.deepcopy(configuration.tubes) )
                    new_configuration = new_configuration.move(i,j)

                    if new_configuration != None:
                        #print(depth,len(unfinished_tubes) ,i,j)

                        new_configuration_id = new_configuration.ID()

                        try:
                            if depth < self.configurations_IDs_dict[new_configuration_id][1]:
                                self.configurations_IDs_dict[new_configuration_id] = [configuration.ID(), depth ]

                        except KeyError:
                            self.configurations_IDs_dict[new_configuration_id] = [configuration.ID(), depth ]

                            self._solver(new_configuration, depth+1)



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
