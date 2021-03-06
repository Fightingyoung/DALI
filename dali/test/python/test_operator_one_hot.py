# Copyright (c) 2017-2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nvidia.dali.pipeline import Pipeline
import nvidia.dali.ops as ops
import nvidia.dali.types as types

import numpy as np

sample_size = 20

class OneHotPipeline(Pipeline):
    def __init__(self, num_classes, input, num_threads=1):
        super(OneHotPipeline, self).__init__(sample_size,
                                             num_threads,
                                             0)
        self.ext_src = ops.ExternalSource(source=[input], cycle=True)
        self.one_hot = ops.OneHot(num_classes=num_classes, dtype=types.INT32, device="cpu")

    def define_graph(self):
        self.data = self.ext_src()
        return self.one_hot(self.data)

def one_hot(input):
    outp = np.zeros([sample_size, sample_size], dtype=np.int32)
    for i in range(sample_size):
        outp[i, int(input[i])] = 1
    return outp

def check_one_hot_operator(premade_batch):
    pipeline = OneHotPipeline(num_classes=sample_size, input=premade_batch)
    pipeline.build()
    outputs = pipeline.run()
    reference = one_hot(premade_batch)
    outputs = outputs[0].as_array()
    assert(np.array_equal(outputs, reference))

def test_one_hot_operator():
    np.random.seed(42);
    for i in range(10):
        premade_batch = [np.array([np.random.randint(0, sample_size)], dtype=np.int32) for x in range(sample_size)]
        yield check_one_hot_operator, premade_batch
