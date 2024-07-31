torchrun --nnodes 1 --node_rank 0 --nproc_per_node 8 --master_addr 127.0.0.1 --master_port 28327 src/launcher.py \
    --stage sft \
    --model_name_or_path models/Qwen1.5-14B  \
    --preprocessing_num_workers 16 \
    --finetuning_type full \
    --template default \
    --flash_attn auto \
    --dataset_dir data \
    --dataset raw_test \
    --cutoff_len 1024 \
    --max_samples 100000 \
    --per_device_eval_batch_size 2 \
    --predict_with_generate True \
    --max_new_tokens 1024 \
    --top_p 0.6 \
    --temperature 0.8 \
    --output_dir saves/eval_output \
    --do_predict True


