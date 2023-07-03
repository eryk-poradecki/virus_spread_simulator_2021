import random

class Agent():
  def __init__(self, mortality_rate, grid_size, V, p, t1, t2, d):
    self.initial_x = random.uniform(1,grid_size-1)
    self.initial_y = random.uniform(1,grid_size-1)
    self.current_x = self.initial_x
    self.current_y = self.initial_y

    self.state = 'susceptible'
    self.m = mortality_rate

    self.V = random.uniform(0.1,V) # mobility parameter
    self.movement = self.V

    self.d = d # infectious distance
    self.p = p # probability of getting infected (in %)

    self.infected_agents = 0

    self.t1 = t1
    self.t2 = self.t1 + t2
    self.t = 0
    

class Grid():
  def __init__(self, mortality_rate, population, pre_immunity, ill_at_t0, grid_size, V, p, t1, t2, d, mask_day):
    '''
    keeps a counter of agents with each possible states (used in scatter plots),
    '''
    self.counter = [0,0,0,0]

    self.timer = 0
    if not mask_day == "": 
      self.mask_day = int(mask_day)
    else:
      self.mask_day = None
    self.list_of_agents = {}

    self.grid_size = grid_size

    self.immune_at_t0 = int(population*pre_immunity/100)
    self.ill_at_t0 = ill_at_t0

    self.list_of_agents = list({ Agent(mortality_rate,grid_size, V, p, t1, t2, d) for i in range(population)})
    for i in range(self.immune_at_t0):
      self.list_of_agents[i].state = 'immune'
    for i in range(self.ill_at_t0):
      self.list_of_agents[self.immune_at_t0+i].state = 'ill'



  def update(self, i):
    '''
    creates lists with coordinates of agents with each state
    creates a random vector of size (0,2V) and updates the coords of each agent
    updates the legend
    increases the time
    '''
    susx = []
    susy = []
    immx = []
    immy = []
    illx = []
    illy = []
    for agent in self.list_of_agents:
      if agent.state == 'dead':
        agent.movement = 0
      else:
        v_x = (random.uniform(0,2*agent.movement**2))**0.5
        v_y = (2*agent.movement**2 - v_x**2)**0.5
        agent.current_x += random.choice((-1,1)) * v_x
        agent.current_y += random.choice((-1,1)) * v_y
        self.check_boundries(agent)
        if agent.state == 'immune':
          immx.append(agent.current_x)
          immy.append(agent.current_y)
        elif agent.state == 'ill':
          illx.append(agent.current_x)
          illy.append(agent.current_y)
        else:
          susx.append(agent.current_x)
          susy.append(agent.current_y)
    
    self.disease_spread()
    self.update_illness()

    if self.mask_day:
      self.check_mask_day()
      self.timer+=1
    

    return [susx,susy,immx,immy,illx,illy]
  
  def check_boundries(self, agent):
    '''
    checks if any agent is 'leaving' the graph and if it is, puts it back inside
    '''
    x_coords = [0,self.grid_size]
    y_coords = [0,self.grid_size]
    if agent.current_x < x_coords[0]:
      agent.current_x = x_coords[0]+abs(agent.current_x-x_coords[0])
    elif agent.current_x > x_coords[1]:
      agent.current_x = x_coords[1]-abs(agent.current_x-x_coords[1])
    if agent.current_y < y_coords[0]:
      agent.current_y = y_coords[0]+abs(agent.current_y-y_coords[0])
    elif agent.current_y > y_coords[1]:
      agent.current_y = y_coords[1]-abs(agent.current_y-y_coords[1])     
    
  def keep_track_of(self):
    '''
    each time checks how many agents of each state are there and updates the counter
    '''
    susceptible = 0
    immune = 0
    ill = 0
    dead = 0
    for agent in self.list_of_agents:
      if agent.state == 'susceptible':
        susceptible += 1
      elif agent.state == 'immune':
        immune += 1
      elif agent.state == 'ill':
        ill += 1
      elif agent.state == 'dead':
        dead += 1
    self.counter = [susceptible,immune,ill,dead]

  def disease_spread(self):
    '''
    checks the distance between each ill and susceptible agent and if they are close enough – the susceptible agent can get infected 
    '''
    ill_agents = [agent for agent in self.list_of_agents if agent.state == 'ill']
    for ill_agent in ill_agents:
      for agent in self.list_of_agents:
        if agent.state == 'susceptible':
          distance = (abs(ill_agent.current_x-agent.current_x)**2+abs(ill_agent.current_y-agent.current_y)**2)**0.5
          if distance <= ill_agent.d:
            if random.randint(0,100) <= ill_agent.p:
              agent.state = 'ill'
              if agent.state == 'ill':
                ill_agent.infected_agents += 1
  
  def update_illness(self):
    '''
    checks for how long an ill agent was ill, isolates them after the incubation and changes the state to ill or dead after the illness duration
    '''
    ill_agents = [agent for agent in self.list_of_agents if agent.state == 'ill']
    for ill_agent in ill_agents:
      if ill_agent.t == ill_agent.t1:
        ill_agent.movement = 0
      elif ill_agent.t == ill_agent.t2:
        if random.randint(0,100) <= ill_agent.m:
          ill_agent.state = 'dead'
        else:
          ill_agent.state = 'immune'
          ill_agent.movement = ill_agent.V
      ill_agent.t += 1

  def check_mask_day(self):
    '''
    checks if it's the right time to introduce masks and if it is, lowers the probability of getting infected by 65% (to make it more realistic I assumed that 4% of the population will disobey the order and won't wear masks)
    '''
    if self.timer == self.mask_day:
      for agent in self.list_of_agents:
        if random.randint(0,100) > 4:
          agent.p = 0.35*agent.p

  def calculate_R0(self):
    '''
    after the simulation is over, calculates R0 (average number of susceptible agents each ill agent can infect)
    '''
    infected = 0
    infectors = 0
    for agent in self.list_of_agents:
      infected += agent.infected_agents
      if agent.infected_agents != 0:
        infectors += 1
    R0 = infected/infectors 
    return round(R0, 2)