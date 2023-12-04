# Fireworks Display

## Demo
Demo Video: <https://vimeo.com/890901226>

## GitHub Repository
GitHub Repo: <https://github.com/deankaleb/project.py>

## Description
My python program creates a firework display. This display is affected by mouse movements from the user. These fireworks are infinitely created from a random circular origin on the screen as long as the user moves their mouse.

My program contains four classes. The particle class initializes the particles size, shape, lifespan, and position. These particles are small circles that contribute to a whole firework. I chose different hues of green, purple, and blue for the colors of the firework display. The particletrail class manages a sequence of particles to create a singular firework with paramaters for the number of circles, lifespan of those circles, and the origin of the firework. The fireworksmanager class manages multiple particle trails to allow the user to create multiple firework across their screen. Lastly, the main function creates a window for the firework display to run, allows an infinite loop of fireworks until the user exits the window and for the creation of fireworks with the use of mouse movements. 

I ran into some challenges early on with programming the colors of the firework. I had to do a ton of research on pygames library and the many functions that were available to me. Researching was actually the only way I was able to complete the project. Without vast knowledge of python it's a bit difficult to create your own personal project by yourself. So if anything, I learned that the information is out there but you have to commit yourself to finding it. 