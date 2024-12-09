import matplotlib.pyplot as plt

#simulates the world through an inputed number of steps and returns a register # (array) of the number of animals per step including the starting state
def simulate_and_register(steps,world):
    register = list()
    for i in range(steps):
        register.append(len(world.animals))
        world.step()
    register.append(len(world.animals))
    return register

#plots the content of multiple worlds simulated and registered population data on the same plot
def plot_registered_data(registers):
    fig, plot = plt.subplots(1, 1)
    for register in registers:
        plot.plot(list(range(len(register))), [len(x) for x in register],linewidth=4)
        plot.set_xlabel("Steps")
        plot.set_ylabel("Population")

    plt.show()
