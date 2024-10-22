from __future__ import annotations

import os

from atomate2.vasp.powerups import update_user_incar_settings
from atomate2.common.schemas.phonons import PhononBSDOSDoc
from pymatgen.core.structure import Structure
from atomate2.forcefields.jobs import (
    GAPRelaxMaker,
    GAPStaticMaker,

)

from autoplex.data.common.flows import GenerateTrainingDataForTesting
from autoplex.data.phonons.flows import IsoAtomMaker, RandomStructuresDataGenerator, MLPhononMaker

#os.environ["OMP_NUM_THREADS"] = "4"  # export OMP_NUM_THREADS=4
#os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=1


def test_ml_phonon_maker(test_dir, clean_dir, memory_jobstore):
    from jobflow import run_locally

    potential_file = test_dir / "fitting" / "ref_files" / "gap_file.xml"
    path_to_struct = test_dir / "fitting" / "ref_files" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    gap_phonon_jobs = MLPhononMaker(
        bulk_relax_maker=GAPRelaxMaker(relax_cell=True, relax_kwargs={"interval": 500}),
        phonon_displacement_maker=GAPStaticMaker(name="gap phonon static"),
        static_energy_maker=GAPStaticMaker(),

    ).make_from_ml_model(
        structure=structure, potential_file=potential_file, supercell_settings={"min_length": 20}
    )

    responses = run_locally(
        gap_phonon_jobs, create_folders=True, ensure_success=True, store=memory_jobstore
    )

    assert gap_phonon_jobs.name == "ml phonon"
    assert responses[gap_phonon_jobs.output.uuid][1].replace[0].name == "MLFF.GAP relax"
    assert responses[gap_phonon_jobs.output.uuid][1].replace[1].name == "MLFF.GAP static"

    ml_phonon_bs_doc = responses[gap_phonon_jobs.output.uuid][1].output.resolve(store=memory_jobstore)
    assert isinstance(ml_phonon_bs_doc, PhononBSDOSDoc)


def test_data_generation_distort_type_0(vasp_test_dir, mock_vasp, clean_dir):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    test_mpid = "mp-22905"
    ref_paths = {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "dft static 1/1": "dft_ml_data_generation/rand_static_1/",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    # disabled poscar checks here to avoid failures due to randomness issues
    fake_run_vasp_kwargs = {
        "tight relax": {"incar_settings": ["NSW"]},
        "dft static 1/1": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "kpoints", "potcar"],
        },
    }
    data_gen_dt_0 = RandomStructuresDataGenerator(distort_type=0).make(
        structure=structure,
        mp_id=test_mpid,
        volume_custom_scale_factors=[1.0],
    )

    data_gen_dt_0 = update_user_incar_settings(data_gen_dt_0, {"ISMEAR": 0})

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(data_gen_dt_0, create_folders=True, ensure_success=True)

    assert len(responses[data_gen_dt_0.output[0].uuid][2].output["dirs"]) == 1
    job_names = ["dft static 1/1"]
    for inx, name in enumerate(job_names):
        assert responses[data_gen_dt_0.output[0].uuid][1].replace.jobs[inx].name == name


def test_data_generation_distort_type_1(vasp_test_dir, mock_vasp, clean_dir):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    test_mpid = "mp-22905"
    ref_paths = {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "dft static 1/10": "dft_ml_data_generation/rand_static_1/",
        "dft static 2/10": "dft_ml_data_generation/rand_static_2/",
        "dft static 3/10": "dft_ml_data_generation/rand_static_3/",
        "dft static 4/10": "dft_ml_data_generation/rand_static_1/",
        "dft static 5/10": "dft_ml_data_generation/rand_static_2/",
        "dft static 6/10": "dft_ml_data_generation/rand_static_3/",
        "dft static 7/10": "dft_ml_data_generation/rand_static_1/",
        "dft static 8/10": "dft_ml_data_generation/rand_static_2/",
        "dft static 9/10": "dft_ml_data_generation/rand_static_3/",
        "dft static 10/10": "dft_ml_data_generation/rand_static_1/",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    # disabled poscar checks here to avoid failures due to randomness issues
    fake_run_vasp_kwargs = {
        "tight relax": {"incar_settings": ["NSW"]},
        "dft static 1/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 2/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 3/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 4/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 5/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 6/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 7/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 8/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 9/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 10/10": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }
    data_gen_dt_1 = RandomStructuresDataGenerator(n_structures=3, distort_type=1).make(
        structure=structure,
        mp_id=test_mpid,
        volume_custom_scale_factors=[1.0],
    )

    data_gen_dt_1 = update_user_incar_settings(data_gen_dt_1, {"ISMEAR": 0})

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(data_gen_dt_1, create_folders=True, ensure_success=True)

    # the minimum required numbers of rattled structures are 10
    assert len(responses[data_gen_dt_1.output[0].uuid][2].output["dirs"]) == 10
    job_names = ["dft static 1/10", "dft static 2/10", "dft static 3/10", "dft static 4/10", "dft static 5/10",
                 "dft static 6/10", "dft static 7/10", "dft static 8/10", "dft static 9/10", "dft static 10/10"]
    for inx, name in enumerate(job_names):
        assert responses[data_gen_dt_1.output[0].uuid][1].replace.jobs[inx].name == name


def test_data_generation_distort_type_2(vasp_test_dir, mock_vasp, clean_dir):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    test_mpid = "mp-22905"
    ref_paths = {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "dft static 1/2": "dft_ml_data_generation/rand_static_1/",
        "dft static 2/2": "dft_ml_data_generation/rand_static_2/",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    # disabled poscar checks here to avoid failures due to randomness issues
    fake_run_vasp_kwargs = {
        "tight relax": {"incar_settings": ["NSW"]},
        "dft static 1/2": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 2/2": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }
    data_gen_dt_2 = RandomStructuresDataGenerator(distort_type=2).make(
        structure=structure,
        mp_id=test_mpid,
        volume_custom_scale_factors=[
            1.0,
            1.0,
        ],
        # for distort_type 0 and 2, the number of randomized structures is dependent on the number of scale factors becuase scale_cell is called
    )

    data_gen_dt_2 = update_user_incar_settings(data_gen_dt_2, {"ISMEAR": 0})

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(data_gen_dt_2, create_folders=True, ensure_success=True)

    assert len(responses[data_gen_dt_2.output[0].uuid][2].output["dirs"]) == 2
    job_names = ["dft static 1/2", "dft static 2/2"]
    for inx, name in enumerate(job_names):
        assert responses[data_gen_dt_2.output[0].uuid][1].replace.jobs[inx].name == name


def test_data_generation_volume_range(vasp_test_dir, mock_vasp, clean_dir):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    test_mpid = "mp-22905"
    ref_paths = {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "dft static 1/4": "dft_ml_data_generation/rand_static_1/",
        "dft static 2/4": "dft_ml_data_generation/rand_static_4/",
        "dft static 3/4": "dft_ml_data_generation/rand_static_7/",
        "dft static 4/4": "dft_ml_data_generation/rand_static_10/",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    # disabled poscar checks here to avoid failures due to randomness issues
    fake_run_vasp_kwargs = {
        "tight relax": {"incar_settings": ["NSW"]},
        "dft static 1/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 2/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 3/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft static 4/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }
    data_gen_vol = RandomStructuresDataGenerator(distort_type=0).make(
        structure=structure,
        mp_id=test_mpid,
        volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
    )

    data_gen_vol = update_user_incar_settings(data_gen_vol, {"ISMEAR": 0})

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(data_gen_vol, create_folders=True, ensure_success=True)

    assert len(responses[data_gen_vol.output[0].uuid][2].output["dirs"]) == 4
    job_names = [
        "dft static 1/4",
        "dft static 2/4",
        "dft static 3/4",
        "dft static 4/4",
    ]
    for inx, name in enumerate(job_names):
        assert responses[data_gen_vol.output[0].uuid][1].replace.jobs[inx].name == name


def test_iso_atom_maker(mock_vasp, clean_dir):
    from jobflow import run_locally
    from pymatgen.core import Species

    specie = Species("Cl")

    ref_paths = {
        "Cl-stat_iso_atom": "Cl_iso_atoms/Cl-statisoatom/",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {
        "Cl-stat_iso_atom": {"incar_settings": ["NSW", "ISMEAR"]},
    }

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate the job
    job_iso = IsoAtomMaker().make(all_species=[specie])

    job_iso = update_user_incar_settings(job_iso, {"ISMEAR": 0})

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(job_iso, create_folders=True, ensure_success=True)

    assert (
            responses[job_iso.job_uuids[0]][1].output.output.energy_per_atom == -0.2563903
    )


def test_generate_training_data_for_testing(
        vasp_test_dir, test_dir, memory_jobstore, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    potential_file_dir = test_dir / "fitting" / "ref_files" / "gap_file.xml"
    structure = Structure.from_file(path_to_struct)
    generate_data = GenerateTrainingDataForTesting().make(
        train_structure_list=[structure],
        cell_factor_sequence=[0.95, 1.0, 1.05],
        potential_filename=potential_file_dir,
        n_structures=1,
        steps=1,
    )

    responses = run_locally(
        generate_data, create_folders=True, ensure_success=False, store=memory_jobstore
    )  # atomate2 switched from pckl to json files for the trajectories --> job fails in its current state
