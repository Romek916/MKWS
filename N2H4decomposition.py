import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

temperature = 1000
pressure = 101325

gas=ct.Solution('N2H4.yaml')
gas.X = np.zeros(11)
gas.TPX = temperature, pressure, 'N2H4: 1' #initial condition of gas
reactor=ct.ConstPressureReactor(gas) #filling reactor with gas

with open('substrates.txt', 'wt') as sub:
    print(gas.report(), file=sub)

gas.equilibrate('HP')   #calculation of thermodynamic equilibrium of mixture for simulation verification

with open('products.txt', 'wt') as pro:
    print(gas.report(), file=pro)

simulation = ct.ReactorNet([reactor]) #simulation setup

dt_max = 1.e-5
t_end = 200 * dt_max
states = ct.SolutionArray(gas, extra=['t'])

print('{:10s} {:10s} {:10s} {:14s}'.format(
    't [s]', 'T [K]', 'P [Pa]', 'u [J/kg]'))

while simulation.time < t_end:  #sperformance of simulation
    simulation.advance(simulation.time + dt_max)
    states.append(reactor.thermo.state, t=simulation.time*1e3)
    print('{:10.3e} {:10.3f} {:10.3f} {:14.6f}'.format(
            simulation.time, reactor.T, reactor.thermo.P, reactor.thermo.u))

with open('productsReactor.txt', 'wt') as proReact:
    print(gas.report(), file=proReact)

#plots generation
plt.clf()
plt.plot(states.t, states.T)
plt.xlabel('Time (ms)')
plt.ylabel('Temperature (K)')
plt.show()

plt.clf()
plt.plot(states.t, states.X[:, gas.species_index('N2H4')])
plt.xlabel('Time (ms)')
plt.ylabel('N2H4 Mole Fraction')
plt.show()

plt.clf()
plt.plot(states.t, states.X[:, gas.species_index('H2')])
plt.xlabel('Time (ms)')
plt.ylabel('H2 Mole Fraction')
plt.show()

plt.clf()
plt.plot(states.t, states.X[:, gas.species_index('N2')])
plt.xlabel('Time (ms)')
plt.ylabel('N2 Mole Fraction')
plt.show()

plt.clf()
plt.plot(states.t, states.X[:, gas.species_index('NH3')])
plt.xlabel('Time (ms)')
plt.ylabel('NH3 Mole Fraction')
plt.show()


