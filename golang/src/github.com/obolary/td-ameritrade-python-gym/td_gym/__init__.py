
from gym.envs.registration import register

register(
    id='td-gym-test-v0',
    entry_point='td_gym.envs:TDGymEnvTest',
)

register(
    id='td-gym-v0',
    entry_point='td_gym.envs:TDGymEnvMock',
)

register(
    id='td-gym-v1',
    entry_point='td_gym.envs:TDGymEnvV1',
)
