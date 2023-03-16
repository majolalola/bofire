import numpy as np
import pytest
import torch
from botorch.utils.objective import soft_eval_constraint

from bofire.data_models.objectives.api import (
    MaximizeSigmoidObjective,
    MinimizeSigmoidObjective,
    TargetObjective,
)


@pytest.mark.parametrize(
    "objective",
    [
        (MaximizeSigmoidObjective(w=1, tp=15, steepness=0.5)),
        (MinimizeSigmoidObjective(w=1, tp=15, steepness=0.5)),
        (TargetObjective(w=1, target_value=15, steepness=2, tolerance=5)),
    ],
)
def test_maximize_sigmoid_objective_to_constraints(objective):
    cs, etas = objective.to_constraints(idx=0)

    x = torch.from_numpy(np.linspace(0, 30, 500)).unsqueeze(-1)
    y = torch.ones([500])

    for c, eta in zip(cs, etas):
        xtt = c(x)
        y *= soft_eval_constraint(xtt, eta)

    assert np.allclose(objective.__call__(np.linspace(0, 30, 500)), y.numpy().ravel())