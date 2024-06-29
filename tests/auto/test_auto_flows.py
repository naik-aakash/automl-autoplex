from __future__ import annotations
import os
import pytest
from monty.serialization import loadfn
from atomate2.common.schemas.phonons import PhononBSDOSDoc
from pymatgen.core.structure import Structure
from autoplex.auto.phonons.flows import CompleteDFTvsMLBenchmarkWorkflow

os.environ["OMP_NUM_THREADS"] = "4"  # export OMP_NUM_THREADS=4
os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=1


@pytest.fixture(scope="class")
def ref_paths():
    return {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 1": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 2": "dft_ml_data_generation/tight_relax_2/",
        "static": "dft_ml_data_generation/static/",
        "Cl-statisoatom": "Cl_iso_atoms/Cl-statisoatom/",
        "Li-statisoatom": "Li_iso_atoms/Li-statisoatom/",
        "dft phonon static 1/2": "dft_ml_data_generation/phonon_static_1/",
        "dft phonon static 2/2": "dft_ml_data_generation/phonon_static_2/",
        "dft rattle static 1/12": "dft_ml_data_generation/rand_static_1/",
        "dft rattle static 2/12": "dft_ml_data_generation/rand_static_2/",
        "dft rattle static 3/12": "dft_ml_data_generation/rand_static_3/",
        "dft rattle static 4/12": "dft_ml_data_generation/rand_static_4/",
        "dft rattle static 5/12": "dft_ml_data_generation/rand_static_5/",
        "dft rattle static 6/12": "dft_ml_data_generation/rand_static_6/",
        "dft rattle static 7/12": "dft_ml_data_generation/rand_static_7/",
        "dft rattle static 8/12": "dft_ml_data_generation/rand_static_8/",
        "dft rattle static 9/12": "dft_ml_data_generation/rand_static_9/",
        "dft rattle static 10/12": "dft_ml_data_generation/rand_static_10/",
        "dft rattle static 11/12": "dft_ml_data_generation/rand_static_11/",
        "dft rattle static 12/12": "dft_ml_data_generation/rand_static_12/",
    }


@pytest.fixture(scope="class")
def fake_run_vasp_kwargs():
    return {
        "tight relax": {"incar_settings": ["NSW"]},
        "tight relax 1": {"incar_settings": ["NSW"]},
        "tight relax 2": {"incar_settings": ["NSW"]},
        "dft phonon static 1/2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft phonon static 2/2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft rattle static 1/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 2/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 3/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 4/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 5/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 6/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 7/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 8/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 9/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 10/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 11/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 12/12": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }


@pytest.fixture(scope="class")
def ref_paths4():
    return {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 1": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 2": "dft_ml_data_generation/tight_relax_2/",
        "static": "dft_ml_data_generation/static/",
        "Cl-statisoatom": "Cl_iso_atoms/Cl-statisoatom/",
        "Li-statisoatom": "Li_iso_atoms/Li-statisoatom/",
        "dft phonon static 1/2": "dft_ml_data_generation/phonon_static_1/",
        "dft phonon static 2/2": "dft_ml_data_generation/phonon_static_2/",
        "dft rattle static 1/4": "dft_ml_data_generation/rand_static_1/",
        "dft rattle static 2/4": "dft_ml_data_generation/rand_static_4/",
        "dft rattle static 3/4": "dft_ml_data_generation/rand_static_7/",
        "dft rattle static 4/4": "dft_ml_data_generation/rand_static_10/",
    }


@pytest.fixture(scope="class")
def fake_run_vasp_kwargs4():
    return {
        "tight relax": {"incar_settings": ["NSW", "ISMEAR"]},
        "tight relax 1": {"incar_settings": ["NSW", "ISMEAR"]},
        "tight relax 2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft phonon static 1/2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft phonon static 2/2": {"incar_settings": ["NSW", "ISMEAR"]},

        "dft rattle static 1/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 2/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 3/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 4/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }


def test_complete_dft_vs_ml_benchmark_workflow(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                         volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                         ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow.jobs[-1].output.uuid][1].output[0][0]["benchmark_phonon_rmse"] == pytest.approx(
        2.002641337594289, abs=1.0  # it's kinda fluctuating because of the little data
    )


def test_complete_dft_vs_ml_benchmark_workflow_two_mpids(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_two_mpid = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                                  volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                                  ).make(
        structure_list=[structure, structure],
        mp_ids=["test", "test2"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_two_mpid,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_two_mpid.jobs[6].name == "complete_benchmark"
    assert responses[complete_workflow_two_mpid.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        0.7126017685370398, abs=0.5
    )


def test_complete_dft_vs_ml_benchmark_workflow_two_mpids_big_supercell(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, clean_dir
):  # this unit test checks that the phonon_displacement_maker of phonopy and rattled jobs don't override each other
    from jobflow import run_locally

    ref_paths_big_sc = {
        "tight relax": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 1": "dft_ml_data_generation/tight_relax_1/",
        "tight relax 2": "dft_ml_data_generation/tight_relax_2/",
        "static": "dft_ml_data_generation/static/",
        "Cl-statisoatom": "Cl_iso_atoms/Cl-statisoatom/",
        "Li-statisoatom": "Li_iso_atoms/Li-statisoatom/",
        "dft phonon static big supercell 1/2": "dft_ml_data_generation/phonon_static_1/",
        "dft phonon static big supercell 2/2": "dft_ml_data_generation/phonon_static_2/",
        "dft rattle static 1/4": "dft_ml_data_generation/rand_static_1/",
        "dft rattle static 2/4": "dft_ml_data_generation/rand_static_4/",
        "dft rattle static 3/4": "dft_ml_data_generation/rand_static_7/",
        "dft rattle static 4/4": "dft_ml_data_generation/rand_static_10/",
    }

    fake_run_vasp_kwargs_big_sc = {
        "tight relax": {"incar_settings": ["NSW", "ISMEAR"]},
        "tight relax 1": {"incar_settings": ["NSW", "ISMEAR"]},
        "tight relax 2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft phonon static big supercell 1/2": {"incar_settings": ["NSW", "ISMEAR"]},
        "dft phonon static big supercell 2/2": {"incar_settings": ["NSW", "ISMEAR"]},

        "dft rattle static 1/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 2/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 3/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
        "dft rattle static 4/4": {
            "incar_settings": ["NSW", "ISMEAR"],
            "check_inputs": ["incar", "potcar"],
        },
    }

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_big_sc = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=20, displacements=[0.01],
                                                                volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                                ).make(
        structure_list=[structure, structure],
        mp_ids=["test", "test2"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths_big_sc, fake_run_vasp_kwargs_big_sc)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_big_sc,
        create_folders=True,
        ensure_success=False,
        # We just want to check the correct order and anme of jobs
        # and that the phonon_displacement_maker is not overwritten.
        # Therefore, we set `ensure_success=False`
        store=memory_jobstore,
    )

    assert str(responses).count("dft rattle static") == 16
    # 8 x job name + 8 x task label
    # (4 dft rattle static for each mpid)
    assert str(responses).count("dft phonon static big supercell") == 4
    # has no task label


def test_complete_dft_vs_ml_benchmark_workflow_with_hploop(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_hploop = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                                volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                                hyper_para_loop=True,
                                                                atomwise_regularization_list=[0.01],
                                                                n_sparse_list=[3000, 5000],
                                                                soap_delta_list=[1.0],
                                                                ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_hploop,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_hploop.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow_hploop.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        2.002641337594289, abs=1.0  # it's kinda fluctuating because of the little data
    )


def test_complete_dft_vs_ml_benchmark_workflow_with_sigma_regulaization_hploop(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_sigma_hploop = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                                      volume_custom_scale_factors=[0.975, 1.0, 1.025,
                                                                                                   1.05],
                                                                      hyper_para_loop=True,
                                                                      atomwise_regularization_list=[0.01],
                                                                      n_sparse_list=[3000, 5000],
                                                                      soap_delta_list=[1.0],
                                                                      ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
        **{"regularization": True},
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_sigma_hploop,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_sigma_hploop.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow_sigma_hploop.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        1.511743561686686, abs=1.0  # it's kinda fluctuating because of the little data
    )


def test_complete_dft_vs_ml_benchmark_workflow_with_sigma_regularization(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_sigma = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                               volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                               ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
        **{"regularization": True},
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_sigma,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_sigma.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow_sigma.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        1.511743561686686, abs=0.5
    )


def test_complete_dft_vs_ml_benchmark_workflow_separated(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_sep = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                             volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                             ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
        pre_xyz_files=["vasp_ref.extxyz"],
        pre_database_dir=test_dir / "fitting" / "ref_files",
        **{"separated": True},
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_sep,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_sep.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow_sep.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        0.8709764794814768, abs=0.5
    )


def test_complete_dft_vs_ml_benchmark_workflow_separated_sigma_reg_hploop_three_mpids(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_sep_3 = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                               volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                               hyper_para_loop=True,
                                                               atomwise_regularization_list=[0.01],
                                                               n_sparse_list=[3000, 5000],
                                                               soap_delta_list=[1.0],
                                                               ).make(
        structure_list=[structure, structure, structure],
        mp_ids=["test", "test2", "test3"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
        pre_xyz_files=["vasp_ref.extxyz"],
        pre_database_dir=test_dir / "fitting" / "ref_files",
        **{"regularization": True, "separated": True},
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_sep_3,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert responses[complete_workflow_sep_3.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        0.8709764794814768, abs=0.5
    )


def test_complete_dft_vs_ml_benchmark_workflow_separated_sigma_reg_hploop(
        vasp_test_dir, mock_vasp, test_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, clean_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)

    complete_workflow_sep = CompleteDFTvsMLBenchmarkWorkflow(symprec=1e-2, min_length=8, displacements=[0.01],
                                                             volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
                                                             hyper_para_loop=True,
                                                             atomwise_regularization_list=[0.01],
                                                             n_sparse_list=[3000, 5000],
                                                             soap_delta_list=[1.0],
                                                             ).make(
        structure_list=[structure],
        mp_ids=["test"],
        benchmark_mp_ids=["mp-22905"],
        benchmark_structures=[structure],
        pre_xyz_files=["vasp_ref.extxyz"],
        pre_database_dir=test_dir / "fitting" / "ref_files",
        **{"regularization": True, "separated": True},
    )

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        complete_workflow_sep,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    assert complete_workflow_sep.jobs[4].name == "complete_benchmark"
    assert responses[complete_workflow_sep.jobs[-1].output.uuid][1].output[0][0][
               "benchmark_phonon_rmse"] == pytest.approx(
        0.8709764794814768, abs=0.5
    )


class TestCompleteDFTvsMLBenchmarkWorkflow:
    def test_add_data_to_dataset_workflow(
            self,
            vasp_test_dir,
            mock_vasp,
            test_dir,
            memory_jobstore,
            clean_dir,
            fake_run_vasp_kwargs,
            ref_paths,
    ):
        import pytest
        from jobflow import run_locally

        path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
        structure = Structure.from_file(path_to_struct)

        add_data_workflow = CompleteDFTvsMLBenchmarkWorkflow(
            n_structures=3,
            symprec=1e-2,
            min_length=8,
            displacements=[0.01],
            volume_custom_scale_factors=[0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 1.025, 1.025, 1.025, 1.05, 1.05, 1.05],
            mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
        ).make(
            structure_list=[structure],
            mp_ids=["test"],
            benchmark_mp_ids=["mp-22905"],
            benchmark_structures=[structure],
            pre_xyz_files=["vasp_ref.extxyz"],
            pre_database_dir=test_dir / "fitting" / "ref_files",
            dft_references=None,
        )

        # automatically use fake VASP and write POTCAR.spec during the test
        mock_vasp(ref_paths, fake_run_vasp_kwargs)

        # run the flow or job and ensure that it finished running successfully
        responses = run_locally(
            add_data_workflow,
            create_folders=True,
            ensure_success=True,
            store=memory_jobstore,
        )

        assert responses[add_data_workflow.jobs[-1].output.uuid][
                   1
               ].output[0][0][
                   "benchmark_phonon_rmse"] == pytest.approx(0.4841808019705598, abs=0.5)

    def test_add_data_workflow_with_dft_reference(
            self,
            vasp_test_dir,
            mock_vasp,
            test_dir,
            memory_jobstore,
            clean_dir,
            fake_run_vasp_kwargs,
            ref_paths,
    ):
        from jobflow import run_locally

        path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
        structure = Structure.from_file(path_to_struct)
        dft_data = loadfn(test_dir / "benchmark" / "PhononBSDOSDoc_LiCl.json")
        dft_reference: PhononBSDOSDoc = dft_data["output"]

        add_data_workflow_with_dft_reference = CompleteDFTvsMLBenchmarkWorkflow(
            n_structures=3,
            symprec=1e-2,
            min_length=8,
            displacements=[0.01],
            add_dft_phonon_struct=False,
            volume_custom_scale_factors=[0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 1.025, 1.025, 1.025, 1.05, 1.05, 1.05],
            mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
        ).make(
            structure_list=[structure],
            mp_ids=["test"],
            benchmark_mp_ids=["mp-22905"],
            benchmark_structures=[structure],
            pre_xyz_files=["vasp_ref.extxyz"],
            pre_database_dir=test_dir / "fitting" / "ref_files",
            dft_references=[dft_reference],
        )

        # automatically use fake VASP and write POTCAR.spec during the test
        mock_vasp(ref_paths, fake_run_vasp_kwargs)

        _ = run_locally(
            add_data_workflow_with_dft_reference,
            create_folders=True,
            ensure_success=True,
            store=memory_jobstore,
        )

        for job, uuid in add_data_workflow_with_dft_reference.iterflow():
            assert job.name != "dft_phonopy_gen_data"

        for job, uuid in add_data_workflow_with_dft_reference.iterflow():
            assert job.name != "tight relax 1"

    def test_add_data_workflow_add_phonon_false(
            self,
            vasp_test_dir,
            mock_vasp,
            test_dir,
            memory_jobstore,
            clean_dir,
            fake_run_vasp_kwargs,
            ref_paths,
    ):

        path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
        structure = Structure.from_file(path_to_struct)

        add_data_workflow_add_phonon_false = CompleteDFTvsMLBenchmarkWorkflow(
            n_structures=3,
            symprec=1e-2,
            min_length=8,
            displacements=[0.01],
            add_dft_phonon_struct=False,
            volume_custom_scale_factors=[0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 1.025, 1.025, 1.025, 1.05, 1.05, 1.05],
            mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
        ).make(
            structure_list=[structure],
            mp_ids=["test"],
            benchmark_mp_ids=["mp-22905"],
            benchmark_structures=[structure],
            pre_xyz_files=["vasp_ref.extxyz"],
            pre_database_dir=test_dir / "fitting" / "ref_files",
            dft_references=None,
        )

        for job, uuid in add_data_workflow_add_phonon_false.iterflow():
            assert job.name != "dft_phonopy_gen_data"

    def test_add_data_workflow_add_random_false(
            self,
            vasp_test_dir,
            mock_vasp,
            test_dir,
            memory_jobstore,
            clean_dir,
            fake_run_vasp_kwargs,
            ref_paths,
    ):

        path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
        structure = Structure.from_file(path_to_struct)

        add_data_workflow_add_random_false = CompleteDFTvsMLBenchmarkWorkflow(
            n_structures=3,
            symprec=1e-2,
            min_length=8,
            displacements=[0.01],
            add_dft_random_struct=False,
            volume_custom_scale_factors=[0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 1.025, 1.025, 1.025, 1.05, 1.05, 1.05],
            mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
        ).make(
            structure_list=[structure],
            mp_ids=["test"],
            benchmark_mp_ids=["mp-22905"],
            benchmark_structures=[structure],
            pre_xyz_files=["vasp_ref.extxyz"],
            pre_database_dir=test_dir / "fitting" / "ref_files",
            dft_references=None,
        )

        for job, uuid in add_data_workflow_add_random_false.iterflow():
            assert job.name != "dft_random_gen_data"

    def test_add_data_workflow_with_same_mpid(
            self,
            vasp_test_dir,
            mock_vasp,
            test_dir,
            memory_jobstore,
            clean_dir,
            fake_run_vasp_kwargs,
            ref_paths,
    ):

        path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
        structure = Structure.from_file(path_to_struct)

        add_data_workflow_with_same_mpid = CompleteDFTvsMLBenchmarkWorkflow(
            n_structures=3,
            symprec=1e-2,
            min_length=8,
            displacements=[0.01],
            volume_custom_scale_factors=[0.975, 0.975, 0.975, 1.0, 1.0, 1.0, 1.025, 1.025, 1.025, 1.05, 1.05, 1.05],
            mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
        ).make(
            structure_list=[structure],
            mp_ids=["mp-22905"],
            benchmark_mp_ids=["mp-22905"],
            benchmark_structures=[structure],
            pre_xyz_files=["vasp_ref.extxyz"],
            pre_database_dir=test_dir / "fitting" / "ref_files",
            dft_references=None,
        )

        for job, uuid in add_data_workflow_with_same_mpid.iterflow():
            assert job.name != "tight relax 1"


def test_phonon_dft_ml_data_generation_flow(
        vasp_test_dir, mock_vasp, clean_dir, memory_jobstore, ref_paths4, fake_run_vasp_kwargs4, test_dir
):
    from jobflow import run_locally

    path_to_struct = vasp_test_dir / "dft_ml_data_generation" / "POSCAR"
    structure = Structure.from_file(path_to_struct)
    structure_list = [structure]
    mp_ids = ["mp-22905"]

    flow_data_generation = CompleteDFTvsMLBenchmarkWorkflow(
        n_structures=3, min_length=10, symprec=1e-2, volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
        mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
    ).make(structure_list=structure_list,
           mp_ids=mp_ids,
           benchmark_structures=structure_list,
           benchmark_mp_ids=mp_ids,
           pre_xyz_files=["vasp_ref.extxyz"],
           pre_database_dir=test_dir / "fitting" / "ref_files",
           )

    flow_data_generation_without_rattled_structures = CompleteDFTvsMLBenchmarkWorkflow(
        n_structures=3, min_length=10, symprec=1e-2, add_dft_random_struct=False,
        volume_custom_scale_factors=[0.975, 1.0, 1.025, 1.05],
        mlip_hyper=[{"two_body": True, "three_body": False, "soap": False}],
    ).make(structure_list=structure_list,
           mp_ids=mp_ids,
           benchmark_structures=structure_list,
           benchmark_mp_ids=mp_ids,
           pre_xyz_files=["vasp_ref.extxyz"],
           pre_database_dir=test_dir / "fitting" / "ref_files",
           )
    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths4, fake_run_vasp_kwargs4)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(
        flow_data_generation,
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore,
    )

    responses_worattled = run_locally(
        flow_data_generation_without_rattled_structures,
        create_folders=True,
        ensure_success=False,  # only two phonon calcs are not enough for this to pass
        store=memory_jobstore,
    )
    counter = 0
    counter_wor = 0
    for job, uuid in flow_data_generation.iterflow():
        counter += 1
    for job, uuid in flow_data_generation_without_rattled_structures.iterflow():
        counter_wor += 1
    assert counter == 7
    assert counter_wor == 6
# TODO testing cell_factor_sequence
