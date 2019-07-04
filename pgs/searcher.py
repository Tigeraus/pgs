import multiprocessing
import pickle
import itertools
import time
import sys
import copy


class GridSearcher:
    """
    To Test model performance under different parameters configurations.
    This class must be used in the top level context or it would lose effect.
    """

    def __init__(self, Model, parameter_dict, processes=None, verbose=True, interval=0.1):
        """
        Specify the model type, generate all possible combinations of
        every pair of parameters and control the processes used.
        args:
            Model: the class that is used to test.

            parameter_dict: a dict containing lists of parameters. If the model receives
            {'a':0, 'b':1}, parameter_dict can be {'a':[0,1], 'b':[1,2]}

            processes: processes used in experiment.
            
            verbose: show progress bar or not.

            interval: minimal interval for progress bar update, increase it to decrease
            the network load when using it in remote jupyterlab server.
        """
        self.verbose = verbose
        self.interval = interval
        self.md = Model
        if not processes:
            processes = multiprocessing.cpu_count() - 1
        self.pool = multiprocessing.Pool(processes=processes)
        self.conf_list = []
        kys = parameter_dict.keys()
        parameters = [parameter_dict[k] for k in kys]

        for element in itertools.product(*parameters):
            e = {}
            for k, v in zip(kys, element):
                e[k] = v

            self.conf_list.append(copy.deepcopy(e))

    def search(self, save=False, file_name=None):
        """
        Search in the grids.
        args:
            save(bool): if you want to save the running results
            file_name: file path for result storage if save is True
        
        returns:
            return_dict: the results dict for each possible parameter combinations.

        """
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        e = manager.Event()
        p = multiprocessing.Process(
            target=self._monitor_progress, args=(self.conf_list, e, return_dict, self.verbose, self.interval))
        p.start()

        for i in range(len(self.conf_list)):
            res = self.pool.apply_async(self._model_trainer, args=(
                i, e, self.md, return_dict, self.conf_list[i]))

        self.pool.close()
        self.pool.join()
        p.join()

        self.return_dict = return_dict

        if save:
            pickle.dump(return_dict, open(file_name, 'wb'))
        return return_dict

    @staticmethod
    def _model_trainer(procnum, event, Model, return_dict, args):
        """

        """
        model = Model(args)
        t0 = time.time()

        return_dict[procnum] = {
            'result': model.run(procnum),
            'parameters': args,
            'time(s)': time.time()-t0
        }
        # print(f'#{procnum} finished')

    @staticmethod
    def _monitor_progress(conf_list, event, return_dict, verbose, interval=0.1):
        """
        Show progress bar during grid search process.
        """
        toolbar_width = 60
        bar_symbol = '-'
        total_p = len(conf_list)
        current_p = len(return_dict)

        if verbose:
            sys.stdout.write("|%s|" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+1))

            while current_p < total_p:
                num = int(toolbar_width * current_p/total_p)
                sys.stdout.write(bar_symbol * num+'>')
                sys.stdout.flush()
                sys.stdout.write("\b" * (num+1))
                time.sleep(interval)
                current_p = len(return_dict)
            sys.stdout.write(bar_symbol * toolbar_width)
            sys.stdout.write("|\n")

