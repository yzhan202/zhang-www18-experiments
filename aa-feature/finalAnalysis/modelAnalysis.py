import numpy as np
from os.path import isfile, join

psl_dir = '/home/yue/Public/Java/testonPSL/output/crossValidation'

model_num = 5
models = np.zeros([5, 128])
rules = []
for i in range(model_num):
    file = 'model_'+ str(i)
    full_name = join(psl_dir, file)
    model_data = open(full_name, 'r').readlines()

    for j in range(2, 130):
        # print j
        line = model_data[j].strip()
        # print line
        start_idx = 1
        try:
            end_idx = line.index('}')
            if i == 0:
                rule_str = line[(end_idx+1):]
                rules.append(rule_str)
        except:
            continue
        weight = float(line[start_idx: end_idx])

        models[i][j-2] = weight

mean_weights = np.mean(models, axis=0)

output = './modelWeights'
out = open(output, 'w+')
for i in range(len(mean_weights)):
    weight = mean_weights[i]
    out.write('%f\t%s\n' % (weight, rules[i]))
out.close()
