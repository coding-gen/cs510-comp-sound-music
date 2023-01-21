import musdb
import museval

# initiate musdb
mus = musdb.DB()

# evaluate an existing estimate folder with wav files
museval.eval_mus_dir(
    dataset=mus,  # instance of musdb
    estimates_dir=...,  # path to estimate folder
    output_dir=...,  # set a folder to write eval json files
    subsets="Test",
    parallel=True
)