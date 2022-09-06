import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np
import os
from scipy.stats.mstats import mquantiles
from astropy.table import Table


def plot_y_given_x_relation(result_dir):
    """
    Use to plot the conditional relationship of Y given X.
    \nINPUTS:
        result_dir : Directory generated by the fitting function.
            Example: result_dir = '~/mrexo_working/trial_result'

    EXAMPLE:

        # Sample script to plot M-R data and fit.
        from mrexo import plot_mr_relation
        import os

        pwd = '~/mrexo_working/'
        result_dir = os.path.join(pwd,'Results_deg_12')

        _ = plot_y_given_x_relation(result_dir)

    """

    input_location = os.path.join(result_dir, 'input')
    output_location = os.path.join(result_dir, 'output')
    aux_output_location = os.path.join(output_location, 'other_data_products')

    with open(os.path.join(aux_output_location, 'AxesLabels.txt'), 'r') as f:
        LabelDictionary = eval(f.read())

    t = Table.read(os.path.join(input_location, 'XY_inputs.csv'))
    Y = t[LabelDictionary['Y_char']]
    Y_sigma = t[LabelDictionary['Y_char']+'_sigma']
    X = t[LabelDictionary['X_char']]
    X_sigma = t[LabelDictionary['X_char']+'_sigma']

    Y_min, Y_max = np.loadtxt(os.path.join(input_location, 'Y_bounds.txt'))
    X_min, X_max = np.loadtxt(os.path.join(input_location, 'X_bounds.txt'))

    X_points = np.loadtxt(os.path.join(output_location, 'X_points.txt'))
    Y_cond_X = np.loadtxt(os.path.join(output_location, 'Y_cond_X.txt'))
    Y_cond_X_upper = np.loadtxt(os.path.join(output_location, 'Y_cond_X_upper.txt'))
    Y_cond_X_lower = np.loadtxt(os.path.join(output_location, 'Y_cond_X_lower.txt'))

    weights_boot = np.loadtxt(os.path.join(output_location, 'weights_boot.txt'))
    Y_cond_X_boot = np.loadtxt(os.path.join(output_location, 'Y_cond_X_boot.txt'))

    n_boot = np.shape(weights_boot)[0]
    deg_choose = int(np.sqrt(np.shape(weights_boot[1])))

    yx_lower_boot, yx_upper_boot = mquantiles(Y_cond_X_boot, prob=[0.16, 0.84], axis = 0, alphap=1, betap=1).data

    fig = plt.figure(figsize=(8.5,7))
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
    ax1 = fig.add_subplot(1,1,1)

    ax1.errorbar(x=X, y=Y, xerr=X_sigma, yerr=Y_sigma,fmt='k.',markersize=3, elinewidth=0.3)
    ax1.plot(10**X_points, 10**Y_cond_X,  color='maroon', lw=2) # Full dataset run
    ax1.fill_between(10**X_points, 10**Y_cond_X_upper, 10**Y_cond_X_lower,alpha=0.3, color='lightsalmon') # Full dataset run
    ax1.fill_between(10**X_points, 10**yx_lower_boot, 10**yx_upper_boot,alpha=0.3, color='r') # Bootstrap result

    yx_median_line = Line2D([0], [0], color='maroon', lw=2,
        label='Median of f({}$|${}) from full dataset run'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))
    yx_full = mpatches.Patch(color='lightsalmon', alpha=0.3,
        label=r'Quantiles of f({}$|${}) from full dataset run'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))
    yx_boot = mpatches.Patch(color='r', alpha=0.3,
        label=r'Quantiles of the median of the f({}$|${}) from bootstrap'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))

    handles = [yx_median_line, yx_full, yx_boot]


    ax1.set_xlabel(LabelDictionary['X_label'])
    ax1.set_ylabel(LabelDictionary['Y_label'])
    ax1.set_title('f({}$|${}) with degree {}, and {} bootstraps'.format(LabelDictionary['Y_char'], LabelDictionary['X_char'], deg_choose, n_boot), pad=5)
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    plt.show(block=False)
    plt.ylim(10**Y_min, 10**Y_max)
    plt.xlim(10**X_min, 10**X_max)
    import matplotlib
    matplotlib.rc('text', usetex=True) #use latex for text
    plt.legend(handles = handles, prop={'size': 15})
    plt.tight_layout()


    return fig, ax1, handles


def plot_x_given_y_relation(result_dir):
    """
    Use to plot the conditional relationship of X given Y.
    \nINPUTS:
        result_dir : Directory generated by the fitting function.
            Example: result_dir = '~/mrexo_working/trial_result'

    EXAMPLE:

        # Sample script to plot M-R data and fit.
        from mrexo import plot_x_given_y_relation
        import os

        pwd = '~/mrexo_working/'
        result_dir = os.path.join(pwd,'Results_deg_12')

        _ = plot_x_given_y_relation(result_dir)

    """

    input_location = os.path.join(result_dir, 'input')
    output_location = os.path.join(result_dir, 'output')
    aux_output_location = os.path.join(output_location, 'other_data_products')

    with open(os.path.join(aux_output_location, 'AxesLabels.txt'), 'r') as f:
        LabelDictionary = eval(f.read())

    t = Table.read(os.path.join(input_location, 'XY_inputs.csv'))
    Y = t[LabelDictionary['Y_char']]
    Y_sigma = t[LabelDictionary['Y_char']+'_sigma']
    X = t[LabelDictionary['X_char']]
    X_sigma = t[LabelDictionary['X_char']+'_sigma']

    Y_min, Y_max = np.loadtxt(os.path.join(input_location, 'Y_bounds.txt'))
    X_min, X_max = np.loadtxt(os.path.join(input_location, 'X_bounds.txt'))

    Y_points = np.loadtxt(os.path.join(output_location, 'Y_points.txt'))
    X_cond_Y = np.loadtxt(os.path.join(output_location, 'X_cond_Y.txt'))
    X_cond_Y_upper = np.loadtxt(os.path.join(output_location, 'X_cond_Y_upper.txt'))
    X_cond_Y_lower = np.loadtxt(os.path.join(output_location, 'X_cond_Y_lower.txt'))

    weights_boot = np.loadtxt(os.path.join(output_location, 'weights_boot.txt'))
    X_cond_Y_boot = np.loadtxt(os.path.join(output_location, 'X_cond_Y_boot.txt'))

    n_boot = np.shape(weights_boot)[0]
    deg_choose = int(np.sqrt(np.shape(weights_boot[1])))

    xy_lower_boot, xy_upper_boot = mquantiles(X_cond_Y_boot, prob=[0.16, 0.84], axis = 0, alphap=1, betap=1).data

    fig = plt.figure(figsize=(8.5,7))
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
    ax1 = fig.add_subplot(1,1,1)

    ax1.errorbar(y=X, x=Y, yerr=X_sigma, xerr=Y_sigma,fmt='k.',markersize=3, elinewidth=0.3)
    ax1.plot(10**Y_points, 10**X_cond_Y,  color='midnightblue', lw=2) # Full dataset run
    ax1.fill_between(10**Y_points, 10**X_cond_Y_lower, 10**X_cond_Y_upper, alpha=0.3, color='cornflowerblue') # Full dataset run
    ax1.fill_between(10**Y_points, 10**xy_lower_boot, 10**xy_upper_boot, alpha=0.3, color='b') # Bootstrap result

    xy_median_line = Line2D([0], [0], color='midnightblue', lw=2,
            label=r'Median of f({}$|${}) from full dataset run'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    xy_full = mpatches.Patch(color='cornflowerblue', alpha=0.3,
        label=r'Quantiles of f({}$|${}) from full dataset run'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    xy_boot = mpatches.Patch(color='b', alpha=0.3,
        label=r'Quantiles of the median of the f({}$|${}) from bootstrap'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    handles = [xy_median_line, xy_full, xy_boot]

    plt.legend(handles=handles, prop={'size': 15})
    handles = [xy_median_line, xy_full, xy_boot]


    ax1.set_ylabel(LabelDictionary['X_label'])
    ax1.set_xlabel(LabelDictionary['Y_label'])
    ax1.set_title('f({}$|${}) with degree {}, and {} bootstraps'.format(LabelDictionary['X_char'], LabelDictionary['Y_char'], deg_choose, n_boot), pad=5)
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    plt.show(block=False)
    plt.xlim(10**Y_min, 10**Y_max)
    plt.ylim(10**X_min, 10**X_max)
    import matplotlib
    matplotlib.rc('text', usetex=True) #use latex for text
    plt.legend(handles = handles, prop={'size': 15})
    plt.tight_layout()

    return fig, ax1, handles


def plot_yx_and_xy(result_dir):
    """
    Use to plot the conditional relationship of radius given mass, as well as and mass given radius.
    Fig 3 (a,c) from Sangangnire S et al. 2020

    \nINPUTS:
        result_dir : Directory generated by the fitting function.
            Example: result_dir = '~/mrexo_working/trial_result'

    EXAMPLE:

        # Sample script to plot M-R data and fit.
        from mrexo import plot_yx_and_xy
        import os

        pwd = '~/mrexo_working/'
        result_dir = os.path.join(pwd,'Results_deg_12')

        _ = plot_yx_and_xy(result_dir)

    """

    input_location = os.path.join(result_dir, 'input')
    output_location = os.path.join(result_dir, 'output')
    aux_output_location = os.path.join(output_location, 'other_data_products')

    with open(os.path.join(aux_output_location, 'AxesLabels.txt'), 'r') as f:
        LabelDictionary = eval(f.read())

    t = Table.read(os.path.join(input_location, 'XY_inputs.csv'))
    Y = t[LabelDictionary['Y_char']]
    Y_sigma = t[LabelDictionary['Y_char']+'_sigma']
    X = t[LabelDictionary['X_char']]
    X_sigma = t[LabelDictionary['X_char']+'_sigma']

    Y_min, Y_max = np.loadtxt(os.path.join(input_location, 'Y_bounds.txt'))
    X_min, X_max = np.loadtxt(os.path.join(input_location, 'X_bounds.txt'))

    X_points = np.loadtxt(os.path.join(output_location, 'X_points.txt'))
    Y_points = np.loadtxt(os.path.join(output_location, 'Y_points.txt'))

    Y_cond_X = np.loadtxt(os.path.join(output_location, 'Y_cond_X.txt'))
    Y_cond_X_upper = np.loadtxt(os.path.join(output_location, 'Y_cond_X_upper.txt'))
    Y_cond_X_lower = np.loadtxt(os.path.join(output_location, 'Y_cond_X_lower.txt'))
    X_cond_Y = np.loadtxt(os.path.join(output_location, 'X_cond_Y.txt'))
    X_cond_Y_upper = np.loadtxt(os.path.join(output_location, 'X_cond_Y_upper.txt'))
    X_cond_Y_lower = np.loadtxt(os.path.join(output_location, 'X_cond_Y_lower.txt'))

    weights_boot = np.loadtxt(os.path.join(output_location, 'weights_boot.txt'))
    Y_cond_X_boot = np.loadtxt(os.path.join(output_location, 'Y_cond_X_boot.txt'))
    X_cond_Y_boot = np.loadtxt(os.path.join(output_location, 'X_cond_Y_boot.txt'))

    n_boot = np.shape(weights_boot)[0]
    deg_choose = int(np.sqrt(np.shape(weights_boot[1])))

    yx_lower_boot, yx_upper_boot = mquantiles(Y_cond_X_boot, prob=[0.16, 0.84], axis = 0, alphap=1, betap=1).data
    xy_lower_boot, xy_upper_boot = mquantiles(X_cond_Y_boot, prob=[0.16, 0.84], axis = 0, alphap=1, betap=1).data

    fig = plt.figure(figsize=(8.5,7))
    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
    ax1 = fig.add_subplot(1,1,1)

    ax1.errorbar(x=X, y=Y, xerr=X_sigma, yerr=Y_sigma,fmt='k.',markersize=3, elinewidth=0.3)
    ax1.plot(10**X_points, 10**Y_cond_X,  color='maroon', lw=2) # Full dataset run
    ax1.fill_between(10**X_points, 10**Y_cond_X_upper, 10**Y_cond_X_lower,alpha=0.3, color='lightsalmon') # Full dataset run
    ax1.fill_between(10**X_points, 10**yx_lower_boot, 10**yx_upper_boot,alpha=0.3, color='r') # Bootstrap result

    ax1.plot(10**X_cond_Y, 10**Y_points, color='midnightblue', lw=2) # Full dataset run
    ax1.fill_betweenx(10**Y_points, 10**X_cond_Y_lower, 10**X_cond_Y_upper, alpha=0.3, color='cornflowerblue') # Full dataset run
    ax1.fill_betweenx(10**Y_points, 10**xy_lower_boot, 10**xy_upper_boot, alpha=0.3, color='b') # Bootstrap result

    yx_median_line = Line2D([0], [0], color='maroon', lw=2,
        label='Median of f({}$|${}) from full dataset run'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))
    yx_full = mpatches.Patch(color='lightsalmon', alpha=0.3,
        label=r'Quantiles of f({}$|${}) from full dataset run'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))
    yx_boot = mpatches.Patch(color='r', alpha=0.3,
        label=r'Quantiles of the median of the f({}$|${}) from bootstrap'.format(LabelDictionary['Y_char'], LabelDictionary['X_char']))
    xy_median_line = Line2D([0], [0], color='midnightblue', lw=2,
        label=r'Median of f({}$|${}) from full dataset run'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    xy_full = mpatches.Patch(color='cornflowerblue', alpha=0.3,
        label=r'Quantiles of f({}$|${}) from full dataset run'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    xy_boot = mpatches.Patch(color='b', alpha=0.3,
        label=r'Quantiles of the median of the f({}$|${}) from bootstrap'.format(LabelDictionary['X_char'], LabelDictionary['Y_char']))
    handles = [yx_median_line, yx_full, yx_boot, xy_median_line, xy_full, xy_boot]


    ax1.set_xlabel(LabelDictionary['X_label'])
    ax1.set_ylabel(LabelDictionary['Y_label'])
    ax1.set_title('f({}$|${}) with degree {}, and {} bootstraps'.format(LabelDictionary['Y_char'], LabelDictionary['X_char'], deg_choose, n_boot), pad=5)
    ax1.set_yscale('log')
    ax1.set_xscale('log')

    plt.show(block=False)
    plt.ylim(10**Y_min, 10**Y_max)
    plt.xlim(10**X_min, 10**X_max)
    import matplotlib
    matplotlib.rc('text', usetex=True) #use latex for text
    plt.legend(handles = handles, prop={'size': 15})
    plt.tight_layout()

    return fig, ax1, handles


def plot_joint_xy_distribution(result_dir):
    """
    Use to plot joint distribution of mass AND radius.
    Fig 3 (b,d) from Sangangire S et al. 2020

    \nINPUTS:
        result_dir : Directory generated by the fitting function.
            Example: result_dir = '~/mrexo_working/trial_result'

    EXAMPLE:

        # Sample script to plot M-R data and fit.
        from mrexo import plot_joint_xy_distribution
        import os

        pwd = '~/mrexo_working/'
        result_dir = os.path.join(pwd,'Results_deg_12')

        _ = plot_joint_xy_distribution(result_dir)

    """

    input_location = os.path.join(result_dir, 'input')
    output_location = os.path.join(result_dir, 'output')
    aux_output_location = os.path.join(output_location, 'other_data_products')

    with open(os.path.join(aux_output_location, 'AxesLabels.txt'), 'r') as f:
        LabelDictionary = eval(f.read())

    t = Table.read(os.path.join(input_location, 'XY_inputs.csv'))
    Y = t[LabelDictionary['Y_char']]
    Y_sigma = t[LabelDictionary['Y_char']+'_sigma']
    X = t[LabelDictionary['X_char']]
    X_sigma = t[LabelDictionary['X_char']+'_sigma']

    Y_min, Y_max = np.loadtxt(os.path.join(input_location, 'Y_bounds.txt'))
    X_min, X_max = np.loadtxt(os.path.join(input_location, 'X_bounds.txt'))

    X_points = np.loadtxt(os.path.join(output_location, 'X_points.txt'))
    Y_points = np.loadtxt(os.path.join(output_location, 'Y_points.txt'))

    logY = np.log10(Y)
    logX = np.log10(X)
    logY_sigma = 0.434 * Y_sigma/Y
    logX_sigma = 0.434 * X_sigma/X

    joint = np.loadtxt(os.path.join(output_location,'joint_distribution.txt'))

    fig = plt.figure(figsize=(8.5,6.5))
    ax1 = fig.add_subplot(1,1,1)
    ax1.errorbar(x=logX, y=logY, xerr=logX_sigma, yerr=logY_sigma, fmt='k.', markersize=3, elinewidth=0.3)


    plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=20)    # fontsize of the tick labels

    ax1.tick_params(which = 'both',  labeltop = False, top = False, labelright = False, right = False, labelsize = 22)

    im = ax1.imshow(joint, cmap = 'coolwarm', extent=[X_min, X_max, Y_min, Y_max], origin = 'lower', aspect = 'auto')
    cbar = fig.colorbar(im, ticks=[np.min(joint), np.max(joint)], fraction=0.037, pad=0.04)
    cbar.ax.set_yticklabels(['Min', 'Max'])

    x_ticks = ax1.get_xticks().tolist()
    x_tick_labels = [np.round(10**i,3) for i in x_ticks]
    ax1.set_xticklabels(x_tick_labels, size = 18)

    y_ticks = ax1.get_yticks().tolist()
    y_tick_labels = [np.round(10**i,2) for i in y_ticks]
    ax1.set_yticklabels(y_tick_labels, size = 18)


    plt.ylim(Y_min, Y_max)
    plt.xlim(X_min, X_max)

    ax1.set_xlabel(LabelDictionary['X_label'])
    ax1.set_ylabel(LabelDictionary['Y_label'])

    plt.show(block=False)

    return fig, ax1



def plot_mle_weights(result_dir):
    """
    Function to plot MLE weights, similar to Fig 2 from Sangangire S et al. 2020
    \nINPUTS:
        result_dir = Directory created by fitting procedure. See ~/mrexo/mrexo/datasets/M_dwarfs_20181214 for example

    OUTPUTS:

        Displays plot. No outputs

    """
    output_location = os.path.join(result_dir, 'output')

    weights_mle = np.loadtxt(os.path.join(output_location,'weights.txt'))

    size = int(np.sqrt(len(weights_mle)))

    plt.imshow(np.reshape(weights_mle , [size, size]), extent = [0, size, 0, size], origin = 'left', cmap = 'viridis')
    plt.xticks(np.arange(0,size), *[np.arange(0,size)])
    plt.yticks(np.arange(0,size), *[np.arange(0,size)])

    plt.colorbar()
    plt.title('Polynomial weights with {} degrees'.format(size))
    plt.show()
