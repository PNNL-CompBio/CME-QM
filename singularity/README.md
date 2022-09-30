# NWChem singularity for EMSL cascade 

Singularity recipe for NWChem to use on EMSL cascade with mpich 3.2.1

## how to build on cascade
```
curl -LJO https://raw.githubusercontent.com/edoapra/nwchem-singularity/master/Singularity
singularity build --fakeroot nwchem.simg  Singularity
```
## how to run on cascade

From a Slurm script or inside an interactive Slurm session
```
module purge
module load mpich/3.2.1
mpirun  singularity exec ./nwchem.simg nwchem "input file"
```
## Using image from the Singularity Library on EMSL cascade
Instead of building on cascade, you can pull the image from the Singularity Library with two options
### option \#1
```
export https_proxy=http://proxy.emsl.pnl.gov:3128
module purge
module load mpich/3.2.1
mpirun singularity exec library://edoapra/default/nwchem701.ivybridge.mpich321.mpipr:sha256.03560327f67283ba0622594293bd35c61b4dc1e00228561b6cb5bd484ae205bc nwchem "input file"
```

### option \#2
```
singularity pull library://edoapra/default/nwchem701.ivybridge.mpich321.mpipr:latest 
```
The name of the downloaded image is `nwchem701.ivybridge.mpich321.mpipr_latest.sif`, therefore the commands to run it on cascade will change to

```
module purge
module load mpich/3.2.1
mpirun  singularity exec ./nwchem701.ivybridge.mpich321.mpipr_latest.sif nwchem "input file"
```
