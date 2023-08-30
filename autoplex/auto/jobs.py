"""
Complete AutoPLEX -- Automated machine-learned Potential Landscape explorer -- jobs
"""

from pathlib import Path
from pymatgen.core.structure import Structure
from jobflow import Flow, job, Response
from atomate2.forcefields.jobs import GAPRelaxMaker, GAPStaticMaker
from atomate2.forcefields.flows.phonons import PhononMaker

@job
def PhononDFTMLBenchmarkJob(
        structure_list: list[Structure],
        ml_dir: str | Path | None = None,
):
    flows = []
    for struc_i, structure in enumerate(structure_list):
        GAPPhonons = PhononMaker(
            bulk_relax_maker=GAPRelaxMaker(potential_param_file_name=ml_dir, relax_cell=True,
                                           relax_kwargs={"interval": 500}),
            phonon_displacement_maker=GAPStaticMaker(potential_param_file_name=ml_dir),
            static_energy_maker=GAPStaticMaker(potential_param_file_name=ml_dir),
            store_force_constants=False,
            generate_frequencies_eigenvectors_kwargs={"units": "THz"}).make(
            structure=structure)
        flows.append(GAPPhonons)
        # benchmark = PhononBenchmarkMaker(name="Benchmark").make()
        # flows.append(benchmark)

        flow = Flow(flows) # output will follow
        return Response(replace=flow)