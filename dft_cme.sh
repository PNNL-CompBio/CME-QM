
### # Clean files to avoid snakemake locking problem.
#rm -rf .snakemake results/* logs/*

DATA_PATH="data/test.csv"

# # Create molecule config file.
python src/create_mol_config.py $DATA_PATH

 # Run cme pipeline!
snakemake --printshellcmds --cores 6 \
          --stats logs/final_pipeline_execution.json \
          --snakefile final_pipeline.smk \
          --configfile config.yaml \
          --latency-wait 300 > logs/$(date -u +'%Y-%m-%dT%H:%M:%SZ')_snakemake_cmd.out

# # Copy Snakmake log in logs/
cp -p $(find `pwd` -name `ls -Art .snakemake/log/ | tail -1`) logs/

# # Cascade
#LEAPRC_GAFF=/home/scicons/cascade/apps/python/3.7/dat/leap/cmd/leaprc.gaff
#LEAPRC_FF14SB=/home/scicons/cascade/apps/python/3.7/dat/leap/cmd/oldff/leaprc.ff14SB
