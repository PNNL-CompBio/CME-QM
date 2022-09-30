For now the mongodb database has been setup locally.

To run the [database script](../apis/database/cme_mongo.py)

Before running database script, I assume:
1. You're running mongodb server on your machine
2. You're mounted the `MSSHARE/Anubhav/darpacme/` drive on your system and configured the `RESULT_PATH` to MSSHARE data location & `FILEPATTERN` to `CHEM_ID_calc_prop_v2.dat`(default) file in database script. 
3. Have a MongoDB GUI client, such Studio 3T or NoSQL Manager downloaded and installed to view the database queries.

Run the database script.
`python cme_mongo.py`

Example database can be found at `smb://pnl.gov/Projects/MSSHARE/Anubhav/darpacme/Oct26/test/darpe_cme.calcProp_uvSpec.json`
JSON Schema:

```
Atomic Number

INCHIKEY  index  A	B	C	mu	HOMO    LUMO    gap     ZPVE    U0       U     H       G       Cv

Geometry block with mulliken charges as ==> symbol x y z Mulliken_population_charge

Frequency

Converged SMILE

Converged InChI

------------------UNITS of properties----------------------

I.  Property  Unit         Description
--  --------  -----------  --------------
1  tag       -            "INCHIKEY"; string constant to ease extraction via grep
2  index     -            Consecutive, 1-based integer identifier of molecule
3  A         cm-1         Rotational constant A
4  B         cm-1         Rotational constant B
5  C         cm-1         Rotational constant C
6  mu        Debye        Dipole moment
7  homo      Hartree      Energy of Highest occupied molecular orbital (HOMO)
8  lumo      Hartree      Energy of Lowest occupied molecular orbital (LUMO)
9  gap       Hartree      Gap, difference between LUMO and HOMO
10  zpve     Hartree      Zero point vibrational energy
11  U0       Hartree      Internal energy at 0 K
12  U        Hartree      Internal energy at 298.15 K
13  H        Hartree      Enthalpy at 298.15 K
14  G        Hartree      Free energy at 298.15 K
15  Cv       cal/mol-K    Heat capacity at 298.15 K
```

<details><summary>Sample database document</summary>
<p>

```mongojs
{ 
    "_id" : "KSEBMYQBYZTDHS-HWKANZROSA-M", 
    "atomic_num" : NumberInt(24), 
    "INCHIKEY" : "KSEBMYQBYZTDHS-HWKANZROSA-M", 
    "index" : "KSEBMYQBYZTDHS-HWKANZROSA-M", 
    "A" : 0.050706, 
    "B" : 0.018, 
    "C" : 0.01471, 
    "mu" : 5.7437844482, 
    "HOMO" : -0.2054529, 
    "LUMO" : -0.0135485, 
    "gap" : 0.1919044, 
    "ZPVE" : 0.19638889566141512, 
    "U0" : -592.907702504817, 
    "U" : -592.700074504817, 
    "H" : -592.699131504817, 
    "G" : -592.7484801350587, 
    "Cv" : 44.502, 
    "geo_block" : [
        [
            "C", 
            2.3887962, 
            -1.61080755, 
            -0.1494748, 
            -0.16999999999999993
        ], 
        [
            "C", 
            3.35446709, 
            -0.58295536, 
            -0.19870777, 
            -0.17999999999999972
        ], 
        [
            "C", 
            1.03050204, 
            -1.32182051, 
            -0.14440963, 
            -0.23000000000000043
        ], 
        [
            "C", 
            2.98190821, 
            0.75540299, 
            -0.24768949, 
            -0.1900000000000004
        ], 
        [
            "C", 
            -0.41292119, 
            2.02944908, 
            -0.25933631, 
            -0.019999999999999574
        ], 
        [
            "C", 
            -2.29531416, 
            -0.51334009, 
            1.3241779, 
            -0.040000000000000036
        ], 
        [
            "C", 
            0.6235709, 
            0.02374632, 
            -0.17918187, 
            0.05999999999999961
        ], 
        [
            "C", 
            -0.66251935, 
            0.68095436, 
            -0.19067203, 
            0.009999999999999787
        ], 
        [
            "C", 
            1.61277367, 
            1.04233645, 
            -0.23757404, 
            0.29000000000000004
        ], 
        [
            "C", 
            -2.00250504, 
            0.02346523, 
            -0.08145639, 
            0.04999999999999982
        ], 
        [
            "N", 
            0.94959335, 
            2.25378711, 
            -0.28100364, 
            -0.6799999999999997
        ], 
        [
            "O", 
            -3.56213003, 
            -1.14494106, 
            1.3823646, 
            -0.6699999999999999
        ], 
        [
            "O", 
            -2.10315637, 
            -1.1360316, 
            -0.93004101, 
            -0.6799999999999997
        ], 
        [
            "H", 
            2.71761064, 
            -2.64592787, 
            -0.11929648, 
            0.14
        ], 
        [
            "H", 
            4.40962205, 
            -0.84208893, 
            -0.20316257, 
            0.15000000000000002
        ], 
        [
            "H", 
            0.28430283, 
            -2.10930126, 
            -0.12642897, 
            0.14
        ], 
        [
            "H", 
            3.72487533, 
            1.54745263, 
            -0.29261372, 
            0.16000000000000003
        ], 
        [
            "H", 
            -1.10893102, 
            2.85701722, 
            -0.28607341, 
            0.18999999999999995
        ], 
        [
            "H", 
            -2.31288238, 
            0.31826465, 
            2.03519347, 
            0.16000000000000003
        ], 
        [
            "H", 
            -1.48103132, 
            -1.19585666, 
            1.61670757, 
            0.14
        ], 
        [
            "H", 
            -2.79829945, 
            0.74209614, 
            -0.33570152, 
            0.14
        ], 
        [
            "H", 
            1.39014313, 
            3.15813014, 
            -0.34196153, 
            0.38
        ], 
        [
            "H", 
            -3.57423141, 
            -1.77154983, 
            0.63955221, 
            0.42000000000000004
        ], 
        [
            "H", 
            -1.83819691, 
            -0.87247309, 
            -1.82443824, 
            0.43000000000000005
        ]
    ], 
    "freq_block" : [
        -0.0, 
        -0.0, 
        0.0, 
        0.0, 
        0.0, 
        0.0, 
        61.353, 
        85.811, 
        104.807, 
        182.776, 
        203.769, 
        226.731, 
        255.782, 
        315.02, 
        348.163, 
        361.193, 
        424.376, 
        437.702, 
        457.636, 
        465.268, 
        530.578, 
        573.782, 
        588.466, 
        630.745, 
        652.505, 
        758.512, 
        769.367, 
        782.277, 
        800.02, 
        800.887, 
        864.421, 
        889.172, 
        901.764, 
        934.546, 
        976.553, 
        1040.433, 
        1043.145, 
        1072.806, 
        1090.665, 
        1099.015, 
        1121.245, 
        1164.808, 
        1192.761, 
        1203.683, 
        1247.243, 
        1277.901, 
        1301.528, 
        1319.571, 
        1356.834, 
        1367.152, 
        1390.283, 
        1403.47, 
        1422.828, 
        1456.69, 
        1462.449, 
        1499.056, 
        1529.638, 
        1540.647, 
        1606.71, 
        1633.684, 
        1678.454, 
        2992.024, 
        3009.983, 
        3111.548, 
        3179.892, 
        3190.077, 
        3204.35, 
        3220.414, 
        3263.127, 
        3668.227, 
        3722.247, 
        3755.54
    ], 
    "converg_smile" : "c1ccc2c(c1)c(c[nH]2)[C@H](CO)O", 
    "converg_inchi" : "1S/C10H11NO2/c12-6-10(13)8-5-11-9-4-2-1-3-7(8)9/h1-5,10-13H,6H2/t10-/m0/s1"
}
```

</p>
</details>
