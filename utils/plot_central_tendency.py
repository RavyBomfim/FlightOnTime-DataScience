import pandas as pd
import matplotlib.pyplot as plt

def plot_central_tendency(
        column: pd.Series,
        axis: int = 0,
        linewidth: int = 1,
        colors: list[str] = ['red', 'yellow', 'blue']
) -> None:
    """
    Plots vertical lines for mean, median, and mode of a numeric column on an existing histogram or plot.

    Parameters
    ----------
    column : pd.Series
        The column to analyze.
    axis : int, optional
        Axis for the lines:  
        0 = vertical (x-axis)  
        1 = horizontal (y-axis).  
        Default is 0.
    linewidth : int, optional
        Width of the plotted lines.  
        Default is 1.
    colors : list[str], optional
        List of 3 colors for mean, median, and mode lines respectively.  
        Default is ['red', 'yellow', 'blue'].

    Raises
    ------
    TypeError or ValueError if inputs are invalid.

    Returns
    -------
    None
    """
    # Validate input parameters
    if not isinstance(column, pd.Series):
        raise TypeError('column must be a pandas Series')
    if not pd.api.types.is_numeric_dtype(column):
        raise TypeError(f"column must be numeric")
    
    # Validate axis, linewidth and colors
    if not isinstance(axis, int) or axis not in [0, 1]:
        axis = 0
    if not isinstance(linewidth, int) or linewidth < 1:
        linewidth = 1
    if isinstance(colors, tuple) and len(colors) == 3 and all(isinstance(c, str) for c in colors): # Tolerates a tuple
        colors = list(colors)
    if not isinstance(colors, list) or len(colors) != 3 or not all(isinstance(c, str) for c in colors):
        colors = ['red', 'yellow', 'blue']


    # Calculate the mean, median, and mode
    mean = column.mean()
    median = column.median()
    mode = column.mode().values[0]
    
    # Create a dictionary for colors
    colors_dict = {
        'mean': colors[0],
        'median': colors[1],
        'mode': colors[2]
    }

    # Plot the lines
    if axis == 0:
        plt.axvline(mean, color=colors_dict['mean'], linestyle='dashed', linewidth=linewidth, label=f'Mean: {mean:,.2f}')
        plt.axvline(median, color=colors_dict['median'], linestyle='dashed', linewidth=linewidth, label=f'Median: {median:,.2f}')
        plt.axvline(mode, color=colors_dict['mode'], linestyle='dashed', linewidth=linewidth, label=f'Mode: {mode:,.2f}')
    elif axis == 1:
        plt.axhline(mean, color=colors_dict['mean'], linestyle='dashed', linewidth=linewidth, label=f'Mean: {mean:,.2f}')
        plt.axhline(median, color=colors_dict['median'], linestyle='dashed', linewidth=linewidth, label=f'Median: {median:,.2f}')
        plt.axhline(mode, color=colors_dict['mode'], linestyle='dashed', linewidth=linewidth, label=f'Mode: {mode:,.2f}')
    
    plt.legend()