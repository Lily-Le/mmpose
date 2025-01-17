#%%
import matplotlib.pyplot as plt
import json

#%%
paths={
'ori44':'/home/zlc/cll/code/mmpose/work_dirs/res18_freihand2d_224x224_ft/20220506_043806.log.json',
'cgbg29c':'/home/zlc/cll/code/mmpose/work_dirs/res18_freihand2d_224x224_ft_cgbg/20220506_070750.log_c.json',
'cgbg14':'/home/zlc/cll/code/mmpose/work_dirs/res18_freihand2d_224x224_ft_cgbg/20220506_072244.log.json',
}

labels=paths.keys()
accs=[]
iter=[]
val_accs=[]
results_all={}
for n in paths:
    jst=[]
    with open(paths[n],'r') as f:
        data=f.read().splitlines()
        for j in range(1,len(data)):
            # jsc=json.loads(data[j])
            jst.append(json.loads(data[j]))       
    f.close()
    results_all[n]=jst
    # print(data[1].keys())
#%%
import copy
import pdb
def dic_to_list(dic_list):
    keys=list(dic_list[0].keys())
    ep_keys=['AUC','EPE','PCK','epoch','iter','lr','mode']
    # keys.remove('memory')
    dic_result= dict.fromkeys(keys)
    ep_result=dict.fromkeys(ep_keys)
    for n in keys:
        dic_result[n]=[]
    for n in ep_keys:
        ep_result[n]=[]
    for d in range(len(dic_list)):   
        for n in dic_list[d].keys():
            if n in keys:
                dic_result[n].append(dic_list[d][n])
            if n in ep_keys:
                # pdb.set_trace()
                ep_result[n].append(dic_list[d][n])
    return dic_result,ep_result

def show_results(results,mode,ind):
    import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(220+1)
    i=0
    for n in results.keys():#_ep999_
        ax.plot(results[n][mode][ind],label=n)
        # break
        i+=1
        pdb.set_trace()
    # ax.plot(Accuracy_val_list, label = 'val_acc')
    ax.set_xlabel(mode)
    ax.set_ylabel(ind)
    #plt.ylim([0.5, 1])
    ax.set_title(f'{ind} vs. {mode}')
    ax.legend(loc='lower right')

        

#%%
    # for i in range(1,len(data)):

# %%
results=dict.fromkeys(labels)
for n in results:
    results[n]={'iter_result':None,'epoch_result':None}
    results[n]['iter_result'],results[n]['epoch_result']=dic_to_list(results_all[n])
# %%
show_results(results,'epoch_result','AUC')
# %%
