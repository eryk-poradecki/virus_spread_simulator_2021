from inp import innitiate_simulation

from matplotlib.gridspec import GridSpec

import numpy as np
import matplotlib.pyplot as plt


plt.style.use('ggplot')

#grid = innitiate_simulation()


class Display():
  def __init__(self, grid):
    self.pause = False
    self.grid = grid
    '''
    creates the figure and the main plot, uses GridSpec to devide the window
    '''
    self.grid_size = self.grid.grid_size
    self.fig = plt.figure(figsize=(16,8), num='COVID Simulation')
    self.gs = GridSpec(3,2, figure=self.fig, hspace=0.255)
    self.ax = plt.subplot(self.gs[0:,0],title="Simulation")
    self.ax.grid(False)

    '''
    creates scatters for each possible state, for larger population (x>1000) the scatter points are smaller for better visibility
    '''
    self.time = 0
    if len(self.grid.list_of_agents) >= 1000:
      self.susceptible = self.ax.scatter([],[],s=20,color='steelblue', label='susceptible {}'.format(self.grid.counter[0]))
      self.ill = self.ax.scatter([],[],s=20,color='crimson', label='ill {}'.format(self.grid.counter[2]))
      self.immune = self.ax.scatter([],[],s=20,color='forestgreen', label='immune {}'.format(self.grid.counter[1]))
      self.dead = self.ax.scatter([],[],s=20,color='whitesmoke', label='dead {}'.format(self.grid.counter[3]))
    else:
      self.susceptible = self.ax.scatter([],[],color='steelblue', label='susceptible {}'.format(self.grid.counter[0]))
      self.ill = self.ax.scatter([],[],color='crimson', label='ill {}'.format(self.grid.counter[2]))
      self.immune = self.ax.scatter([],[],color='forestgreen', label='immune {}'.format(self.grid.counter[1]))
      self.dead = self.ax.scatter([],[],color='whitesmoke', label='dead {}'.format(self.grid.counter[3])) 

    '''
    creates subplots – linear functions of total cases, active cases and deaths over time
    '''
    self.subtotal = plt.subplot(self.gs[0,1], title='Total cases/t')
    self.subactive = plt.subplot(self.gs[1,1], title='Active cases/t')
    self.subdead = plt.subplot(self.gs[2,1], title='Deaths/t')

    self.totalx = []
    self.totaly = []
    self.activex = []
    self.activey = []
    self.deadx = []
    self.deady = []
    
    self.total, = self.subtotal.plot([],[],'navy')
    self.active, = self.subactive.plot([],[],'crimson')
    self.deads, = self.subdead.plot([],[],'black')

    self.max_total = self.grid.counter[2]+self.grid.counter[1]-self.grid.immune_at_t0
    self.max_active = self.grid.counter[2]
    self.max_dead = self.grid.counter[3]
    '''
    creates legend, time counter, R0
    '''
    self.legend = self.ax.legend(loc='upper right')
    self.time_counter = self.ax.text( x=self.grid_size,y=self.grid_size+1,s='time: {}'.format(self.time), fontsize=20)
    self.disp_R0 = self.ax.text( x = 0, y = self.grid_size+1, s ='', fontsize=20)
    
  def initiate_animation(self):
    '''
    sets axes, the background color and the window title
    '''
    self.fig.patch.set_facecolor('mistyrose')

    self.ax.set_xlim(0, self.grid_size)
    self.ax.set_ylim(0, self.grid_size)
    return self.susceptible, self.immune, self.ill,

  def update(self, i):
    '''
    checks if the simulation is finished, if it is – displays R0
    if not – updates all the plots and the legend
    '''
    self.check_if_finished(i)
    if not self.pause:
      
      self.update_legend()
      self.update_subplots(i-1)
      self.time += 1
      self.time_counter.set_text(s='time: {}'.format(self.time))
      values = self.grid.update(i)
      self.susceptible.set_offsets(np.c_[values[0], values[1]])
      self.immune.set_offsets(np.c_[values[2], values[3]])
      self.ill.set_offsets(np.c_[values[4], values[5]])
    elif self.pause:
      R0 = self.grid.calculate_R0()
      self.disp_R0.set_text(s='R0: {}'.format(R0))
    
    return self.susceptible, self.immune, self.ill, self.dead

  def update_legend(self):
    '''
    checks the situation on the board (how many agents with each state are there) and updates the legend
    '''
    self.grid.keep_track_of()
    self.susceptible.set_label('susceptible {}'.format(self.grid.counter[0]))
    self.immune.set_label('immune {}'.format(self.grid.counter[1]))
    self.ill.set_label('ill {}'.format(self.grid.counter[2]))
    self.dead.set_label('dead {}'.format(self.grid.counter[3]))
    self.ax.legend(loc='upper right')
  
  def check_if_finished(self,i):
    '''
    checks if there are still ill people in the simulation, if not stops the simulation
    '''
    if i>0:
      if self.grid.counter[2] == 0:
        self.pause = True
  
  def update_subplots(self, i):
    '''
    updates the subplots:
    sets the limit of x axis depending on the current time,
    updates the plot depending on states of agents
    sets the limit of y axis depending on maximum cases of each state
    '''
    if i>0:
      self.subtotal.set_xlim(0,self.time)
      self.subactive.set_xlim(0,self.time)
      self.subdead.set_xlim(0,self.time)
    
    if (self.grid.counter[2]+self.grid.counter[1]+self.grid.counter[3]-self.grid.immune_at_t0) > self.max_total:
      self.max_total = self.grid.counter[2]+self.grid.counter[1]+self.grid.counter[3]-self.grid.immune_at_t0
    self.subtotal.set_ylim(0,self.max_total+0.1*self.max_total)
    self.totalx.append(self.time)
    self.totaly.append(self.grid.counter[2]+self.grid.counter[1]+self.grid.counter[3]-self.grid.immune_at_t0)
    self.total.set_data(self.totalx,self.totaly)

    if self.grid.counter[2] > self.max_active:
      self.max_active = self.grid.counter[2]
    self.subactive.set_ylim(0,self.max_active+0.1*self.max_active)
    self.activex.append(self.time)
    self.activey.append(self.grid.counter[2])
    self.active.set_data(self.activex,self.activey)

    if self.grid.counter[3] > self.max_dead:
      self.max_dead = self.grid.counter[3]
    if self.grid.counter[3] == 0:
      self.subdead.set_ylim(0,self.max_dead+1)
    else:
      self.subdead.set_ylim(0,self.max_dead+0.1*self.max_dead)
    self.deadx.append(self.time)
    self.deady.append(self.grid.counter[3])
    self.deads.set_data(self.deadx,self.deady)

    return self.total, self.active, self.deads,
