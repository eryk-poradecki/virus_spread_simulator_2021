from model import Grid

import yaml

import argparse


def innitiate_simulation():
    '''
    allows the user to enter values used in simulation and creates a list with unique agents
    there are 3 ways of entering the data
    '''

    '''
    1st way: argparse
    user runs the program in the terminal and gives the parameters using arguments (-h displays the help explaining how to give parameters)
    '''
    parser = argparse.ArgumentParser(description='enter the parameters')
    parser.add_argument('-po','--population', type=int, metavar='', help='enter the population')
    parser.add_argument('-m','--mortality_rate', type=int, metavar='', help='enter the mortality rate')
    parser.add_argument('-i','--pre_immunity', type=int, metavar='', help='enter the %% of people with preliminary immunity')
    parser.add_argument('-i0','--ill_at_t0', type=int, metavar='', help='enter the number of ill people at the beggining of the simulation')
    parser.add_argument('-g','--grid_size', type=int, metavar='', help='enter the size of the grid (at least population/10 is recommended')
    parser.add_argument('-v','--V_param', type=int, metavar='', help='enter the movement parameter (should be greater than 1, unless operating on a very small grid')
    parser.add_argument('-p','--inf_probability', metavar='', type=int, help='enter the population probability of infecting a susceptible agent(in %%)')
    parser.add_argument('-t1','--inc_time', metavar='', type=int, help='enter the incubation time')
    parser.add_argument('-t2','--sick_time', metavar='', type=int, help='enter the duration of illness')
    parser.add_argument('-d','--inf_distance', metavar='', type=int, help='enter the infective distance')
    parser.add_argument('-md','--mask_day', metavar='', type=str, help='enter on wich day people are order to wear masks(if you dont want them to wear masks, enter "")')
    args = parser.parse_args()
    if args.population == None:
        '''
        2nd way: command line questions
        user is being ask to enter parameters by the program
        '''
        choice = input("how would you like to enter parameters:\nmanually or using yaml file (m,y): ")
        if choice == 'm':
            population = int(input("enter the population: "))
            mortality_rate = int(input("enter mortality rate: "))
            pre_immunity = int(input("enter the % of population with preliminary immunity: "))
            ill_at_t0 = int(input("enter the number of ill people at t0: "))
            grid_size = int(input("enter the size of the grid: "))
            V = int(input("enter the maximum mobility parameter(should be greater than 1, unless operating on a very small grid): "))
            p = int(input("enter the probability of infecting a susceptible agent(in %): "))
            t1 = int(input("enter the incubation time: "))
            t2 = int(input("enter the duration of illness: "))
            d = int(input("enter the infective distance: "))
            mask_day = input("enter on wich day people are order to wear masks(if you don't want them to wear masks, press enter): ")

            grid = Grid(mortality_rate, population, pre_immunity, ill_at_t0, grid_size, V, p, t1, t2, d, mask_day)
            return grid
        elif choice == 'y':
            '''
            3rd way: .yaml file
            user can specify their parameters using a yaml file (an example is given in sim.yaml)
            '''
            path = str(input('enter the path to the .yaml file: '))
            with open(path) as file:
                p = yaml.load(file, Loader=yaml.FullLoader) # p – parameters
            grid = Grid(p['mortality_rate'], p['population'], p['pre_immunity'], p['ill_at_t0'], p['grid_size'],p['V'],p['p'],p['t1'],p['t2'],p['d'],p['mask_day'])
            return grid
    else:
        grid = Grid(args.mortality_rate, args.population, args.pre_immunity, args.ill_at_t0, args.grid_size, args.V_param, args.inf_probability, args.inc_time, args.sick_time, args.inf_distance, args.mask_day)
        return grid

