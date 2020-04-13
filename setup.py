from setuptools import setup

setup(
  name='LambdaLayerPolicyManager',
  version='1.0',
  py_modules=['layer_policy'],
  install_requires=[
    'Click',
    'boto3',
    'termcolor',
    ''
  ],
  entry_points='''
      [console_scripts]
      layer-policy-manager=layer_policy:cli
  '''
)