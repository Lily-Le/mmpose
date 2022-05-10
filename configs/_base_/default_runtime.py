checkpoint_config = dict(interval=10)

log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])

log_level = 'INFO'
# load_from ='/home/zlc/cll/code/peclr_cbg/data/models_res18/hybrid2-frei-cgbg-correct/66e551fefbd14447ab967161e9af9c0c/port_model/epoch=29_st.pth'# None
load_from = None
resume_from = None
dist_params = dict(backend='nccl')
workflow = [('train', 1)]

# disable opencv multithreading to avoid system being overloaded
opencv_num_threads = 0
# set multi-process start method as `fork` to speed up the training
mp_start_method = 'fork'
