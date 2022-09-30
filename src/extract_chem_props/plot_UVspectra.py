import os
import numpy as np
import matplotlib.pyplot as plt
import pylab
import numpy as np
import sys


def plot_UVspectra(input, mol_name):

    title = mol_name
    UV_03 =os.path.join( *input.split('/')[:-1], title + '_0.3.dat')
    print(UV_03)

    with open(input, 'r') as file,\
        open(UV_03, 'w') as plot_data:
        for lines in file.readlines()[15:]:
            line = lines.split()
            wave = float(line[0])
            abso = float(line[-1])
            if wave > 199.99 and wave < 600:
                plot_data.write(lines)

    data3 = np.loadtxt(UV_03)

    c = data3[:, 0]
    d = data3[:, 1]
    d = d / np.max(d)

    index = list(d).index(max(d))
    b03 = c[index]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2.5)

    plt.plot(c, d, ls='-')  # , label = '0.3')
    plt.title(title, size=12)

    # plt.legend(fontsize=18)
    plt.xlabel('Wavelength (nm)', size=16)
    plt.ylabel('Absorbance ', size=16)
    plt.axis([190, 600, 0.0, 1.3])

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    image = os.path.join(*input.split('/')[:-1], title + '.png' )
    fig.savefig(image, dpi=fig.dpi, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    ip_file = ""
    for arg in sys.argv:
        if arg.endswith((".dat")):
            ip_file = arg
    mol_name = ip_file.split('/')[-3]
    plot_UVspectra(ip_file, mol_name)