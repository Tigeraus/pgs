# pgsearch
Parallel grid search.

Usage:

To use pgs, you need to wrap your model in a specific class (with whatever name you like) with a `run` method which receives only one argument, i.e., the process id. Keep everything you need in the initialization of the model and pass all arguments through a dict.

~~~python
from pgsearch import GridSearcher
parameter_dict = {
    'pa': [1, 3, 3, 1, 2, 3, 3, 1, 2, 3, 3, 1, 2, 3],
    'pb': [9, 1, 1, 2, 3, 3, 1, 2, 3],
    'pd': [9, 1, 1, 2, 3, 3, 1, 2, 3],
    'pe':[np.array([1,2,3])]
}

class Model:
    def __init__(self, args):
        self.args = args
        pass

    def run(self, x):
        z = self.args['pa']+self.args['pb']+np.sum(self.args['pe'])
        return x+z # include everything you need here from one trial.

gs = GridSearcher(Model, parameter_dict, processes=13, verbose=True, interval=0.1)
res = gs.search(save=False)
print(res[0])
~~~
