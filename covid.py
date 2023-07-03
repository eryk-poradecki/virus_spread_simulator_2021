from animation import Display

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

from inp import innitiate_simulation

#from inp import innitiate_simulation

if __name__ == "__main__":
  grid = innitiate_simulation()
  
  anim = Display(grid)

  animation = FuncAnimation(anim.fig, anim.update, init_func=anim.initiate_animation, interval=700, frames=200, blit=False)
      
  plt.show()

