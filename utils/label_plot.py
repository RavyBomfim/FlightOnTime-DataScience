import matplotlib.pyplot as plt

def label_plot(title: str = '', xlabel: str = '', ylabel: str = '', footer: str = '', fontsizes: str = 'medium') -> None:
    """
    Adds a title, axis labels, and optional footer to a Matplotlib plot.

    Parameters
    ----------
    title : str, optional
        Title of the plot.  
        Default is '' (no title).
    xlabel : str, optional
        Label for the x-axis.  
        Default is '' (no label).
    ylabel : str, optional
        Label for the y-axis.  
        Default is '' (no label).
    footer : str, optional
        Footer text to be displayed below the plot.  
        Default is '' (no footer).
    fontsizes : {'small', 'medium', 'large'}, optional
        Font size preset for the plot elements. Determines relative sizes for
        title, axis labels, and footer.  
        Default is 'medium'.

    Returns
    -------
    None
    """
    # Setup fontsizes
    fontsizes = fontsizes.strip().lower()
    if fontsizes not in ['small', 'medium', 'large']:
        fontsizes = 'medium'
    
    font_sizes = {}
    if fontsizes == 'small':
        font_sizes = {
            'title': 'large',
            'labels': 'small',
            'footer': 'medium'
        }
    elif fontsizes == 'medium':
        font_sizes = {
            'title': 'x-large',
            'labels': 'medium',
            'footer': 'large'
        }
    elif fontsizes == 'large':
        font_sizes = {
            'title': 'xx-large',
            'labels': 'large',
            'footer': 'x-large'
        }

    if title:
        plt.title(title, fontsize=font_sizes['title'])
    if xlabel:
        plt.xlabel(xlabel, fontsize=font_sizes['labels'])
    if ylabel:
        plt.ylabel(ylabel, fontsize=font_sizes['labels'])
    if footer:
        plt.text(0.5, -0.025, footer, ha='center', va='top',
                 transform=plt.gcf().transFigure, fontsize=font_sizes['footer'])
        
    # Adjust layout for cases of too much text in the plot
    if title and xlabel and ylabel:
        if footer:
            plt.tight_layout(rect=(0, 0.05, 1, 1))
        else:
            plt.tight_layout()