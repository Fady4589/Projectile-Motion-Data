from vpython import *
#Web VPython 3.2
#environment setup
canvas(center=vector(1,1,0), 
     background=color.black)
     ##align='right')

ground = box (pos = vec(0,-0.02,0),
            size = vec(30,0.02,0.4),
            color = color.green ) #green line on floor
            
running = True 
def Run(b): # b = button
    global running, remember_dt, dt
    running = not running
    if running:
        b.text = "Pause"
        dt = remember_dt
    else: 
        b.text = "Run"
        remember_dt = dt
        dt = 0
    return

button(text="Pause", bind=Run) #button to start and stop picks up where it left off despite dent seen

#parameters
vConstant = 6.1 #constant velocity of ball 
#gravity (m/s^2) mars:3.7 venus:8.87 Jupiter:24.5
ePull = 9.81 
vPull = 8.87
mPull = 3.72 
jPull = 27.2
y0 = 0.0000000000000000000000000000000001 #starting height
x0 = -1.4   #set ball's intial position
theta = 50 * pi/180 #angle of launch 

t = 0 #starting time
dt = 0.004 #timestep (intervals of time)
starttime = clock() #sysclock 
realtime = clock() - starttime

#objects
ball = sphere (pos = vec(x0,y0,0), 
                mass = 5, #details of ball
                angle = theta, 
                v = vConstant*vec(cos(theta),sin(theta),0), #this is saying the velocity is = to intial velocity*xpos
                radius = 0.02,
                color = color.red, make_trail = True )

ball_2 = sphere (pos = vec(x0,y0,0 ), #ball being shot
                radius = 0.07, 
                color = color.blue, make_trail=True,
                trail_type ="points")#dotted line

hole = box(pos = vec(1.5,-0.06,0), #position of hole
                size = vec(0.5,0.5,0), #size of hole 
                color = color.white)

print()

ball.mo = ball.mass*ball.v #the ball position depends on mass*velocity
speed_graph = graph(title ='Motion through time', 
                    xtitle ='Time', 
                    ytitle ='velocity') #graph of ball

b_speed = gcurve(graph = speed_graph, 
                color = color.red) #track ball in red graph(data) 

while (ball.pos.y > 0): #while the position of the ball is greater than 
    rate(500)#basically fps (slow down and speed up ball (insimulation time))
    
    #all of these are directly intertwined **DO NOT TOUCH**
    FEnet = vector(0,ball.mass*-ePull,0)# force of ball same as = ball.mass*vec(0,-9.81,0) change accel here
    ball.mo += FEnet * dt #momentum going through timestamp #only works with Fnet vector :(
    ball.v = ball.mo/ball.mass ##parameter for .pos to know info about ball 
    ball.pos += ball.v * dt #u
    #update sphere position based on velocity and timestep (goes to next position)
    ball.accel = (ball.v) / t #update ball's velocity based on acceleration
    
    b_speed.plot(pos = (t,mag(ball.v)))# actually tracking the speed of the ball
    ball_2.pos = vec(x0 + vConstant*cos(theta)*t, y0 + vConstant*sin(theta)*t-ePull/2*t**2,0) ##projectile motion along with ball
    
    t += dt #time update
    d = hole.pos.x - ball.pos.x #Final distance between ball and hole whether or not it hits target
    
    print("Position of the ball:", ball.pos)
    print("velocity of the ball:", ball.accel)  
    print("Distance from target:" , d, "meters")
    print()
    

FE = -FEnet/2.25 
FJ = 60.1
FV = 19.7
FM = 8.3 

realtime = clock() - starttime
print("In-simulation time:",t,"seconds")
print("Real-world time:",realtime,"seconds")
print()
print("Impact force:", FE, "Newtons on Earth")
print("Impact force:", FJ, "Newtons on Jupiter")
print("Impact force:", FV, "Newtons on Venus")
print("Impact force:", FM, "Newtons on Mars")

##to change length of line, go to ground and change sizevec(x,0,0)
#to change the position of box, go to hole  posvec(x,0,0)
##to change acceleration, change g= 
#the blue trail goes based on earth gravitational pull
##try to incorporate **IMPACT FORCE**
##try to incorporate **WIND RESISTANCE**