import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fpath', help='File path')
parser.add_argument(
    'xindex',
    type=int,
    help='Index of the column containing continuous x-values to plot '
)
parser.add_argument(
    'yindex',
    type=int,
    help='Index of the column containing continuous y-values to plot '
)
parser.add_argument(
    '--gindex',
    '-g',
    default=None,
    type=int,
    help='Index of the column containing categorical series values on which to stratify (optional: if not specified, plot all x- and y-values as one series)'
)
parser.add_argument(
    '--output',
    default='output-scatter.png',
    help=' Path to the output file(default `output-scatter.png`)'
)

parser.add_argument(
    '--xlabel'
)
parser.add_argument(
    '--ylabel'
)

args = parser.parse_args()


def load_data(fpath, x, y, z=None):
    '''Load Data'''
    f = open(fpath, 'r')
    cols = next(f).split('\t')
    xs = []
    ys = []
    zs = []
    for line in f:
        ds = line.split('\t')
        xs.append(float(ds[x]))
        ys.append(float(ds[y]))
        if z is not None:
            zs.append(ds[z])

    f.close()
    zheader = None if z is None else cols[z]
    return {
        'data': [xs, ys, zs],
        'columns': [cols[x], cols[y], zheader]
    }



def draw(data, output, xlabel=None, ylabel=None):
    '''Draw scatter'''
    if xlabel is None:
        xlabel = data['columns'][0]
    if ylabel is None:
        ylabel = data['columns'][1]
    series = {}
    if len(data['data'][2]) > 0:
        groups = set(data['data'][2])
        for i in range(len(data['data'][0])):
            x = data['data'][0][i]
            y = data['data'][1][i]
            z = data['data'][2][i].lower().strip()
            if z not in series:
                series[z] = []
                series[z].append([])
                series[z].append([])
            series[z][0].append(x)
            series[z][1].append(y)
    else:
        series['default'] = data['data'][:2]
    scatters = []
    names = []
    for name, ser in series.items():
        sct = plt.scatter(ser[0], ser[1])
        scatters.append(sct)
        names.append(name)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if len(series) > 1:
        plt.legend(scatters, names)
    plt.savefig(output)
    


if __name__ == '__main__':
    data = load_data(args.fpath, args.xindex, args.yindex, args.gindex)
    draw(data, args.output, args.xlabel, args.ylabel)
