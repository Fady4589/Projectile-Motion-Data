from vpython import *
#Web VPython 3.2
from vpython import *

# Setting up the canvas
scene = canvas(center=vector(1, 1, 0), background=color.black)

# Environment setup
ground = box(pos=vec(0, -0.02, 0), size=vec(30, 0.02, 0.4), color=color.green)  # Green line on floor
running = False  # Initial running state is set to False
environments = {"Earth": 9.81, "Mars": 3.72, "Venus": 8.87, "Jupiter": 24.5}
current_env = "Earth"
g = environments[current_env]

# Environment selector function
def change_environment(env):
    global g, current_env
    current_env = env.selected
    g = environments[current_env]
    print(f"Environment changed to {current_env} with gravity {g} m/s^2")

# Adding a dropdown menu for selecting the environment
menu(choices=["Earth", "Mars", "Venus", "Jupiter"], bind=change_environment)

# Toggle running state
def Run(b):
    global running, dt
    running = not running
    if running:
        b.text = "Pause"
        dt = remember_dt
    else:
        b.text = "Run"
        dt = 0

# Reset simulation
def Reset():
    global t, running, dt
    t = 0
    ball.pos = vec(x0, y0, 0)
    ball.v = vConstant * vec(cos(theta), sin(theta), 0)
    ball.mo = ball.mass * ball.v  # Reset momentum
    ball.clear_trail()  # Clear the trail of the ball
    ball_2.pos = vec(x0, y0, 0)
    ball_2.clear_trail()  # Clear the trail of the second ball
    b_speed.delete()  # Clear the graph data
    running = False
    run_button.text = "Run"
    print("Simulation reset.")

# Buttons to control the simulation
run_button = button(text="Run", bind=Run)  # Run/Pause button
button(text="Reset", bind=Reset)  # Reset button

# Parameters
vConstant = 6.1  # Constant velocity of ball
x0 = -1.4  # Set ball's initial position
y0 = 0.0001  # Starting height of the ball (small positive value to avoid division by zero)
theta = 50 * pi / 180  # Angle of launch
t = 0  # Starting time
dt = 0.004  # Timestep (intervals of time)
remember_dt = dt
starttime = clock()  # System clock
realtime = clock() - starttime

# Wind resistance coefficient
wind_resistance = 0.01

# Objects
ball = sphere(pos=vec(x0, y0, 0), mass=5, angle=theta,
              v=vConstant * vec(cos(theta), sin(theta), 0),
              radius=0.02, color=color.red, make_trail=True)

ball_2 = sphere(pos=vec(x0, y0, 0), radius=0.07, color=color.blue,
                make_trail=True, trail_type="points")  # Dotted line

hole = box(pos=vec(1.5, -0.06, 0), size=vec(0.5, 0.5, 0), color=color.white)

ball.mo = ball.mass * ball.v  # Ball momentum
speed_graph = graph(title='Motion through time', xtitle='Time (s)', ytitle='Velocity (m/s)')  # Graph of ball

b_speed = gcurve(graph=speed_graph, color=color.red)  # Track ball speed on graph

# Main simulation loop
while True:
    rate(500)  # Simulation speed
    
    if running and ball.pos.y >= 0:  # Continue simulation while ball is above ground and running
        # Calculate forces
        FEnet = vector(0, ball.mass * -g, 0)  # Gravitational force
        Fwind = -wind_resistance * ball.v.mag2 * norm(ball.v)  # Wind resistance
        Fnet = FEnet + Fwind
        
        # Update momentum and velocity
        ball.mo += Fnet * dt
        ball.v = ball.mo / ball.mass
        ball.pos += ball.v * dt
        ball_2.pos = vec(x0 + vConstant * cos(theta) * t, 
                         y0 + vConstant * sin(theta) * t - g / 2 * t ** 2, 0)
        
        # Plotting ball speed over time
        b_speed.plot(pos=(t, mag(ball.v)))
        
        # Update time
        t += dt
        
        # Display information
        d = hole.pos.x - ball.pos.x
        print(f"Position of the ball: {ball.pos}")
        print(f"Velocity of the ball: {ball.v}")
        print(f"Distance from target: {d} meters")

    # Stop the simulation if the ball reaches the ground
    if ball.pos.y < 0 and running:
        impact_force = mag(Fnet)  # Impact force based on net force
        print(f"Impact force on {current_env}: {impact_force:.2f} Newtons")
        running = False
        run_button.text = "Run"

realtime = clock() - starttime
print(f"In-simulation time: {t} seconds")
print(f"Real-world time: {realtime} seconds")
