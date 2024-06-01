import pandas as pd
import yaml

if __name__ == '__main__':
    d = {
        'a': 1,
        'c': {'a': 2, 'b': {'x': 5, 'y': 10, 'm': [1, 2, 3, 4]}},
        'd': [1, 2, 3]
    }

    df = pd.json_normalize(d)
    a=pd.DataFrame(df.to_dict(orient='records'))

    print()
