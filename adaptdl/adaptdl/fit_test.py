# Copyright 2020 Petuum, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import adaptdl.goodput as goodput
import numpy as np


def test_fit_1():
    # Tests goodput.fit's ability to fit to data generated
    # by its own model class with arbitrary parameters, without
    # gradient accumulation. Serves as a sanity check
    # that the goodput.model fitting works in the most
    # optimistic case.
    size = (1000,)
    nodes = np.random.randint(low=1, high=11, size=size)
    replicas = np.random.randint(low=1, high=nodes + 1, size=size)
    local_bsz = np.random.randint(32, 1024, size=size)
    params = goodput.PerfParams(0.1, 0.01, 0.5, 1.0, 1e-6, 1e-6, 1.2)
    accum_step_time = goodput._predict_accum_time(
        params, local_bsz
    ) + np.maximum(np.random.normal(0, 0.001, size=size), 0.0)
    network_time = goodput._predict_network_time(
        params, nodes, replicas
    ) + np.maximum(np.random.normal(0, 0.001, size=size), 0.0)
    gamma = params.gamma
    optim_step_time = (accum_step_time**gamma + network_time**gamma) ** (
        1 / gamma
    )
    result = goodput.fit_perf_params(
        nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    loss_result = goodput._obj_fn(
        result, nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    loss_true = goodput._obj_fn(
        params, nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    assert (
        abs(loss_result - loss_true) < 0.1 * loss_true
        or loss_result < loss_true
    ), (
        "goodput.fit failed to fit model from data generated by",
        "goodput.PerfParams(0.1, 0.01, 0.5, 1.0, 1e-6, 1e-6, 1.2)",
        "parameters: {}".format(result),
    )


def test_fit_2():
    # Tests goodput.fit's ability to fit to data generated
    # by its own model class with arbitrary parameters, with
    # gradient accumulation. Serves as a sanity check
    # that the goodput.model fitting works in the most
    # optimistic case.
    size = (1000,)
    nodes = np.random.randint(low=1, high=11, size=size)
    replicas = np.random.randint(low=1, high=nodes + 1, size=size)
    local_bsz = np.random.randint(32, 1024, size=size)
    params = goodput.PerfParams(0.1, 0.01, 0.5, 1.0, 1e-6, 1e-6, 1.2)
    accum_step_time = goodput._predict_accum_time(
        params, local_bsz
    ) + np.maximum(np.random.normal(0, 0.01, size=size), 0.0)
    network_time = goodput._predict_network_time(
        params, nodes, replicas
    ) + np.maximum(np.random.normal(0, 0.01, size=size), 0.0)
    gamma = params.gamma
    optim_step_time = (accum_step_time**gamma + network_time**gamma) ** (
        1 / gamma
    )
    result = goodput.fit_perf_params(
        nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    loss_result = goodput._obj_fn(
        result, nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    loss_true = goodput._obj_fn(
        params, nodes, replicas, local_bsz, accum_step_time, optim_step_time
    )
    assert (
        abs(loss_result - loss_true) < 0.1 * loss_true
        or loss_result < loss_true
    ), (
        "goodput.fit failed to fit model from data generated by",
        "goodput.PerfParams(0.1, 0.01, 0.5, 1.0, 1e-6, 1e-6, 1.2)",
        "parameters: {}".format(result),
    )