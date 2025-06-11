import nbformat
from nbclient import NotebookClient

def run_notebook(notebook_path):
    print(f"Running {notebook_path}...")

    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    client = NotebookClient(nb)
    client.execute()
    print(f"Completed {notebook_path}")


notebooks = [
    "/home/noturminesv/projects/gis-ml/src/meta/PCH_calculation.ipynb",
    "/home/noturminesv/projects/gis-ml/src/meta/combine_ht_ch_psh.ipynb",
    "/home/noturminesv/projects/gis-ml/src/meta/feature_engineering.ipynb",
    "/home/noturminesv/projects/gis-ml/main.ipynb"
]

for notebook in notebooks:
    run_notebook(notebook)

