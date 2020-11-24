from gym.envs.registration import register

register(
    id='fxcm-v0',
    entry_point='gym_fxcm.envs:FxcmEnv',
)

register(
    id='fxcm-v1',
    entry_point='gym_fxcm.envs:FxcmEnvV1',
)

register(
    id='fxcm-v2',
    entry_point='gym_fxcm.envs:FxcmEnvV2',
)

register(
    id='fxcm-v3',
    entry_point='gym_fxcm.envs:FxcmEnvV3',
)

register(
    id='fxcm-v4',
    entry_point='gym_fxcm.envs:FxcmEnvV4',
)

register(
    id='fxcm-v5',
    entry_point='gym_fxcm.envs:FxcmEnvV5',
)

register(
    id='coin-v0',
    entry_point='gym_fxcm.envs:CoinEnvV0',
)
