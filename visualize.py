from src.benchmark_function import BenchmarkFunction
from src.functions import rastrigin_function
from src.execution_options import ExecutionOptions
from src.algorithm import WOARun
import matplotlib.pyplot as plt

func = BenchmarkFunction(
    name='Rastrigin Function',
    hof=lambda: lambda *xs: rastrigin_function(xs),
    hyperparams=[],
    hyperparameter_defaults={},
    dimension=2,
    constraints=[{'min': -5.12, 'max': 5.12} for _ in range(2)],
)
execution_options = ExecutionOptions(func)
execution_options.execution_params = {
    'iterations_count': 20
}
woa_run = WOARun(execution_options)

results = woa_run.run()

print(
    "Results are: ",
    f"Best value: {results.best_value}",
    f"Best params: {results.best_params}",
    sep='\n',
)

figure = plt.figure()
for insert in woa_run.history:
    plt.title(insert['id'])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.xlim((-5.12, 5.12))
    plt.ylim((-5.12, 5.12))

    params = [x['params'] for x in insert['population']]
    plt.scatter(
        [x[0] for x in params],
        [x[1] for x in params],
    )
    best_params = insert['best']['params']
    plt.scatter(
        best_params[0],
        best_params[1],
    )

    figure.savefig(f"plots/{insert['id']}.jpg")
    figure.clear()
