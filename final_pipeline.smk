configfile: "config.yaml"
CHEM_IDS= config["chemical_ids"]

DATA_PATH="data/test.csv"
RESULT_PATH="results"
LOGS_PATH="logs"

FORMATS=[".xyz", ".mol", ".mol2", ".png",".charge"]

"""
to mark a rule as local, so that it is not submitted to the cluster 
and instead executed on the host node:
"""
localrules: generate_rulegraph, generate_dag, generate_filegraph


rule all:
    """
    Used to define build-targets.
    """
    input:
         # rule csv2inchi output:
         expand("%s/{chem_id}/initial_structure/{chem_id}.inchi" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule inchiTo3D output:
         expand("%s/{chem_id}/initial_structure/{chem_id}{ext}" % RESULT_PATH, chem_id=CHEM_IDS, ext=FORMATS),
         # rule submit_MD output:
         expand("%s/{chem_id}/initial_structure/{chem_id}/RUN1/TLEAP/leap.log" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule submit_MD2 output:
         expand("%s/{chem_id}/initial_structure/{chem_id}/RUN1/EM/mdinfo" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule prepare_DFT_files output:
         expand("%s/{chem_id}/dft/{chem_id}.sbatch" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule submit_DFT output:
         expand("%s/{chem_id}/dft/{chem_id}.out" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule extract_UVspectra:
         expand("%s/{chem_id}/dft/{chem_id}_calc_prop_v2.dat" % RESULT_PATH, chem_id=CHEM_IDS),
         expand("%s/{chem_id}/dft/spectrum_0.3.dat" % RESULT_PATH, chem_id=CHEM_IDS),
          # rule plot_UVspectra output:
         expand("%s/{chem_id}/dft/{chem_id}.png" % RESULT_PATH, chem_id=CHEM_IDS),
         # rule generate_rulegraph output:
         "%s/cme_rulegraph.png" % LOGS_PATH,
         # rule generate_dag output:
         "%s/cme_dag.png" % LOGS_PATH,
         # rule generate_filegraph output:
         "%s/cme_filegraph.png" % LOGS_PATH

rule csv2inchi:
    """
    Creates necessary result directories.
    """
    input:  DATA_PATH
    output: "%s/{chem_id}/initial_structure/{chem_id}.inchi" % RESULT_PATH
    message:"Running csv2inchi...!"
    log: 'logs/{chem_id}/csv2inchi.log'
    shell:
        """
        python src/gen_inchi/csv2inchi.py {input} {output} > {log}
        """

rule inchiTo3D:
    """
    Input: "*.inchi" file
    Output: ["*.xyz", "*.mol", "*.mol2", "*.png","*.charge"] files.
    """
    input: expand("%s/{chem_id}/initial_structure/{chem_id}.inchi" % RESULT_PATH,chem_id=CHEM_IDS)
    output: multiext("%s/{chem_id}/initial_structure/{chem_id}" % RESULT_PATH, *FORMATS)
    message: "Running inchiTo3D...!"
    log: 'logs/{chem_id}/inchiTo3D.log'
    shell:
        """
        python src/gen_3Dstructure/inchiTo3D.py {input} {output} > {log}
        """

rule submit_MD:
    """
    Run Molecular dynamics
    """
    #FIXME: Downstream logic: input is just a directory not a file!
    input:  "%s/{chem_id}/initial_structure/{chem_id}.mol2" % RESULT_PATH,
            "%s/{chem_id}/initial_structure/{chem_id}.charge" % RESULT_PATH
    output: "%s/{chem_id}/initial_structure/{chem_id}/RUN1/TLEAP/leap.log" % RESULT_PATH
    message: "Running submit_MD...!"
    log: 'logs/{chem_id}/submit_MD.log'
    shell:
        """
        python src/md_simulations/md.py {input} > {log}
        """

rule submit_MD2:
    """
    Step 2 of MD
    #FIXME: Error opening File
            "..TLEAP/TUJKJAMUKRIRHC-UHFFFAOYSA-N.crd"
            "..EM/TUJKJAMUKRIRHC-UHFFFAOYSA-N_em.rst"
            is missing or unreadable
    even though they're present.
    """
    input: "%s/{chem_id}/initial_structure/{chem_id}.mol2" % RESULT_PATH
    output:"%s/{chem_id}/initial_structure/{chem_id}/RUN1/EM/mdinfo" % RESULT_PATH
    message: "Running submit_MD2...!"
    log: 'logs/{chem_id}/submit_MD2.log'
    shell:
        """
        python src/md_simulations/md2.py {input} > {log}
        """
# TODO : conformers from md to dft rule!!

rule prepare_DFT_files:
    """
    Does variable subsitution in template_dft.* files in config/
    """
    input: "%s/{chem_id}/initial_structure/{chem_id}/RUN1/EM/mdinfo" % RESULT_PATH,
           "%s/{chem_id}/initial_structure/{chem_id}.charge" % RESULT_PATH,
           "%s/{chem_id}/initial_structure/{chem_id}.xyz" % RESULT_PATH
    output:"%s/{chem_id}/dft/{chem_id}.sbatch" % RESULT_PATH,
           "%s/{chem_id}/dft/{chem_id}.nw" % RESULT_PATH
    message: "Running prepare_DFT_files...!"
    log: 'logs/{chem_id}/prepare_DFT_files.log'
    shell:
        """
        python src/solvation/create_nw_files.py {input} > {log}
        """

rule submit_DFT:
    """
    dft calculations: Run variable subsituted config/template_dft.sbatch
    Need --latency-wait 300, nwchem needs time for processing  !
    """
    input: "%s/{chem_id}/dft/{chem_id}.nw" % RESULT_PATH
    output:"%s/{chem_id}/dft/{chem_id}.out" % RESULT_PATH
    message: "Running submit_DFT...!"
    shadow: "shallow"
    log: 'logs/{chem_id}/submit_DFT.log'
    # shell:
    #     """
    #     sbatch {input}  > {log}
    #     """
    shell:
        """
        nwchem {input} > {output}
        """

rule extract_UVspectra:
    """
    Extract UV spectrum
    """
    input: "%s/{chem_id}/dft/{chem_id}.out" % RESULT_PATH
    output:
            "%s/{chem_id}/dft/{chem_id}_calc_prop_v2.dat" % RESULT_PATH,
            "%s/{chem_id}/dft/spectrum_0.3.dat" % RESULT_PATH
    message: "Running extract_DFT_properties...!"
    log: 'logs/{chem_id}/extract_UVspectra.log'
    shell:
        """
         python src/extract_chem_props/extract_properties_v2.py {input} > {log}
         python src/extract_chem_props/nw_spectrum.py -b0.3 -p5000 -wnm < {input} > {output[1]}
        """


rule plot_UVspectra:
    """
    plot UV spectrum.
    """
    input: "%s/{chem_id}/dft/spectrum_0.3.dat" % RESULT_PATH
    output: "%s/{chem_id}/dft/{chem_id}.png" % RESULT_PATH
    message: "Running plot_UVspectra...!"
    log: 'logs/{chem_id}/plot_UVspectra.log'
    shell:
        """
        python src/extract_chem_props/plot_UVspectra.py {input} > {log}
        """

rule generate_rulegraph:
    """
    Generate a the dependency graph of rules in the dot language for the workflow.
    Use this if above --dag leads to a DAG that is too large.
    """
    output:
        "%s/cme_rulegraph.png" % LOGS_PATH
    shell:
        """
        snakemake --snakefile final_pipeline.smk --configfile config.yaml --rulegraph | dot -Tpng > {output}
        """
rule generate_dag:
    """
    Generate a the dependency graph of rules in the dot language for the workflow.
    Use this if above --dag leads to a DAG that is too large.
    """
    output:
        "%s/cme_dag.png" % LOGS_PATH
    shell:
        """
        snakemake --snakefile final_pipeline.smk --configfile config.yaml --dag | dot -Tpng > {output}
        """
rule generate_filegraph:
    """
    Generate a the dependency graph of rules in the dot language for the workflow.
    Use this if above --dag leads to a DAG that is too large.
    """
    output:
        "%s/cme_filegraph.png" % LOGS_PATH
    shell:
        """
        snakemake --snakefile final_pipeline.smk --configfile config.yaml --filegraph | dot -Tpng > {output}
        """
