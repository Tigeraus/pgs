# pgsearch
Parallel grid search.

Usage:

To use [pgsearch](https://pypi.org/project/pgsearch/), you need to wrap your model in a specific class (with whatever name you like) with a `run` method which receives only one argument, i.e., the process id. Keep everything you need in the initialization of the model and pass all arguments through a dict.

You can use a dict of parameters lists to generate all possible combinations of parameters:

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

Or use a list of parameters dict directly:

~~~python



class Model:
    def __init__(self, args):
        self.args = args
        pass

    def run(self, x):
        z = self.args['pa']+self.args['pb']+np.sum(self.args['pe'])
        return x+z # include everything you need here from one trial.

parameters = [{'pa': [i],'pb': [i+1],'pd': [i*2],'pe':[np.array([1,2,3])]}  for i in range(300)]

gs = GridSearcher(Model, parameters, processes=13, verbose=True, interval=0.1, preprocess=False)
res = gs.search(save=False)
print(res[0])
~~~