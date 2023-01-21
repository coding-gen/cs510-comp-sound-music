import musdb
import museval

output_dir = ...
estimates_dir = ...

def estimate_and_evaluate(track):
    # generate your estimates
    estimates = {
        'vocals': track.audio,
        'accompaniment': track.audio
    }

    # Evaluate using museval
    scores = museval.eval_mus_track(
        track, estimates, output_dir=output_dir
    )

    # print nicely formatted mean scores
    print(scores)

    # return estimates as usual
    return estimates

# your usual way to run musdb
musdb.DB().run()