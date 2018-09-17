import numpy as np
import pandas as pd
import orca
import copy

from urbansim_templates.settings import pipe_steps
from urbansim_templates import modelmanager as mm
from urbansim_templates.models.regression import OLSRegressionStep
from urbansim_templates.models.regression import RandomForestRegressionStep


pipe_steps['OLSRegressionStep'] = OLSRegressionStep()
pipe_steps['RandomForestRegressionStep'] = RandomForestRegressionStep()


d1 = {'oid': np.arange(1000), 
      'x': np.random.normal(size=1000),
	  'z': np.random.normal(size=1000),
      'y': np.random.normal(scale=0.01, size=1000)}

obs = pd.DataFrame(d1).set_index('oid')
obs['y'] = obs['y'] + obs['x'] +  2 * obs['z']
orca.add_table('obs', obs)

def test_observation_sampling():
    mm.initialize(path='configs')

    m = RandomForestRegressionStep()
    m.tables = 'obs'
    
    # test 1
    m.model_expression = 'y ~ x + z'
    m.fit()   
    m.name = 'ols-test1'
    d = m.to_dict()
    m.register()
    
    # test2 
    m.model_expression = 'y ~ x'
    m.fit()   
    m.name = 'ols-test2'
    d = m.to_dict()
    m.register()
    
    # get both steps
    m1 = mm.get_step('ols-test1')
    m2 = mm.get_step('ols-test2')
    
    # predict with ols-test1
    m1.run()
    t1 = orca.get_table('obs').to_frame()
    
    m2.run()
    t2 = orca.get_table('obs').to_frame()
    
    print(t1.equals(t2))
	
	
if __name__ == '__main__':

	test_observation_sampling()