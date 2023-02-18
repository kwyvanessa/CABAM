def get_avg_weight():

    import pandas as pd
    from pathlib import Path
    cwd = Path.cwd()
    file = cwd / 'weight_of_vegetables.csv'

    df = pd.read_csv(file)

    return df
