import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



G_values = [0.70, 1.00, 1.30]
dt = 0.01
num_steps = 5000




def get_initial_bodies():
    
    #initial conditions for celestial bodies in the system
    return np.array([
        [1000.0, 0.0, 0.0, 0.0, 0.0],
        [1.0, 5.0, 0.0, 0.0, 14.14],
        [0.1, 0.0, 10.0, -9.5, 0.0]
    ])



sim_data = {G: {'x': [[] for _ in range(3)], 'y': [[] for _ in range(3)]} for G in G_values}


for G in G_values:
    
    
    bodies = get_initial_bodies()
    num_bodies = len(bodies)

    for step in range(num_steps):
        forces = np.zeros((num_bodies, 2))

       
        for i in range(num_bodies):
            
            
            for j in range(num_bodies):
                if i == j: continue
                
                
                
                dx = bodies[j, 1] - bodies[i, 1]
                dy = bodies[j, 2] - bodies[i, 2]
                
                
                dist = np.sqrt(dx ** 2 + dy ** 2) + 0.1 

                f_mag = (G * bodies[i, 0] * bodies[j, 0]) / (dist ** 2)
                
                
                forces[i, 0] += f_mag * (dx / dist)
                forces[i, 1] += f_mag * (dy / dist)

        
        
        
        
        for i in range(num_bodies):
            
            
            ax = forces[i, 0] / bodies[i, 0]
            ay = forces[i, 1] / bodies[i, 0]
            
            
            
            
            bodies[i, 3] += ax * dt
            bodies[i, 4] += ay * dt
            bodies[i, 1] += bodies[i, 3] * dt
            bodies[i, 2] += bodies[i, 4] * dt

            sim_data[G]['x'][i].append(bodies[i, 1])
            sim_data[G]['y'][i].append(bodies[i, 2])



fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)


colors = ['gold', 'royalblue', 'crimson']
labels = ['Star', 'inner Planet', 'outer Planet']


plots_dict = {}



for ax, G in zip(axes, G_values):
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.set_title(f"Gravity Constant G = {G}")

    plots_dict[G] = {
        'lines': [ax.plot([], [], color=colors[i], alpha=0.3, lw=1)[0] for i in range(3)],
        'scatters': [ax.plot([], [], 'o', color=colors[i], ms=8 if i == 0 else 5)[0] for i in range(3)]
    }



def animate(frame):
    artists = []
    
    
    for G in G_values:
        for i in range(3):
            
            
            x_path = sim_data[G]['x'][i][:frame]
            y_path = sim_data[G]['y'][i][:frame]

            
            plots_dict[G]['lines'][i].set_data(x_path, y_path)

           
            if len(x_path) > 0:
                plots_dict[G]['scatters'][i].set_data([x_path[-1]], [y_path[-1]])

            artists.append(plots_dict[G]['lines'][i])
            
            
            artists.append(plots_dict[G]['scatters'][i])
    return artists


ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=10, blit=True)
plt.tight_layout()
plt.show()
