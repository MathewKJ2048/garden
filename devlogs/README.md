# garden
A garden-simulator using cellular automata, written in python.

Try it online [here!](https://mathewkj2048.github.io/garden/)

## Controls:

`S` - sand  
`I` - ice  
`W` - water  
`R` - rock  
`F` - fire  
`A` - acid  
`O` - oil  
`E` - embers  
`L` - lava  
`M` - seeds  
`Q` - wood

`V` - inert material  
`C` - nothing  
`B` - erase    
`P` - pause/play  
`G` - flip gravity  

`0-9` - controls size of input  

`/` - stats (only with a console)

## Interactions:

- seeds must be added on top of sand and watered to germinate
- seeds die if they fall on anything other than sand or are covered by anything other than water
- sand makes piles
- rocks hold their shape given support
- fire melts ice, rock and ignites flammable elements
- inert material is unaffected by everything
- acid eats through everything (excpet inert material)
- oil floats on water and poisons plants
- germinating seeds kill immediate neighbours
- ice freezes water
- water turns lava back into rock


## Dependencies:

- [pygame](https://www.pygame.org/download.shtml)
- [pygbag](https://pypi.org/project/pygbag/) (to build as a web-app)

## To Run:

```
python ./src/main.py
```