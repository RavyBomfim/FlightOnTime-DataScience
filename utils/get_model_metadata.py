import automlx
from typing import Any

def get_model_metadata(estimator: automlx._interface) -> dict[str, Any]: # type: ignore
    """
    Extracts metadata from a given AutoMLx estimator.

    Parameters:
    - estimator: An instance of an AutoMLx estimator.

    Returns:
    - A dictionary containing metadata about the model.
    """
    metadata = {
        'model': estimator.selected_model_,
        "model_type": type(estimator).__name__,
        'specifications': estimator.selected_model_params_,
        'features': estimator.selected_features_names_,
        'features_raw': list(set(estimator.selected_features_names_raw_)),
        "training_time": getattr(estimator, 'training_time_', None),
        "score_metric": getattr(estimator, 'score_metric_', None),
    }

    return metadata