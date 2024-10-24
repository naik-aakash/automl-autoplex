import os 

from jobflow import run_locally, Flow
from jobflow import Response, job
from autoplex.data.rss.jobs import RandomizedStructure, do_rss
from autoplex.data.common.jobs import sampling, VASP_collect_data, Data_preprocessing
from autoplex.data.common.flows import DFTStaticMaker
from autoplex.fitting.common.flows import MLIPFitMaker
from typing import List, Optional, Dict, Any
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor
from pathlib import Path


@job
def mock_RSS(input_dir: str = None,
             selection_method: str = 'cur',
             num_of_selection: int = 3,
             bcur_params: Optional[str] = None,
             random_seed: int = None,
             e0_spin: bool = False,
             isolated_atom: bool = True,
             dimer: bool = True,
             dimer_range: list = None,
             dimer_num: int = None,
             custom_set: Optional[str] = None,
             vasp_ref_file: str = 'vasp_ref.extxyz',
             rss_group: str = 'initial',
             test_ratio: float = 0.1,
             regularization: bool = True,
             distillation: bool = True,
             f_max: float = 200,
             pre_database_dir: Optional[str] = None,
             mlip_type: str = 'GAP',
             ref_energy_name: str = "REF_energy",
             ref_force_name: str = "REF_forces",
             ref_virial_name: str = "REF_virial",
             num_processes_fit: int = None,
             kt: float = None,
             **fit_kwargs,):
    
    job2 = sampling(selection_method=selection_method,
                    num_of_selection=num_of_selection,
                    bcur_params=bcur_params,
                    dir=input_dir,
                    random_seed=random_seed)
    job3 = DFTStaticMaker(e0_spin=e0_spin, 
                       isolated_atom=isolated_atom, 
                       dimer=dimer,
                       dimer_range=dimer_range,
                       dimer_num=dimer_num,
                       custom_set=custom_set, 
                       ).make(structures=job2.output)
    job4 = VASP_collect_data(vasp_ref_file=vasp_ref_file, 
                             rss_group=rss_group, 
                             vasp_dirs=job3.output)
    job5 = Data_preprocessing(test_ratio=test_ratio, 
                              regularization=regularization, 
                              distillation=distillation, 
                              f_max=f_max, 
                              vasp_ref_dir=job4.output['vasp_ref_dir'], pre_database_dir=pre_database_dir)
    job6 = MLIPFitMaker(mlip_type=mlip_type, 
                        ref_energy_name=ref_energy_name,
                        ref_force_name=ref_force_name,
                        ref_virial_name=ref_virial_name,
                        ).make(database_dir=job5.output, 
                               isol_es=job4.output['isol_es'],
                               num_processes_fit=num_processes_fit,
                               preprocessing_data=False,
                               **fit_kwargs)
    job_list = [job2, job3, job4, job5, job6]

    return Response(
        replace=Flow(job_list),
        output={
            'test_error': job6.output['test_error'],
            'pre_database_dir': job5.output,
            'mlip_path': job6.output['mlip_path'],
            'isol_es': job4.output['isol_es'],
            'current_iter': 0,
            'kt': kt
        },
    )


@job
def mock_do_RSS_iterations(input: Dict[str, Optional[Any]] = {'test_error': None,
                                                         'pre_database_dir': None,
                                                         'mlip_path': None,
                                                         'isol_es': None,
                                                         'current_iter': None,
                                                         'kt': 0.6},
                      input_dir: str = None,
                      selection_method1: str = 'cur',
                      selection_method2: str = 'bcur',
                      num_of_selection1: int = 3,
                      num_of_selection2: int = 5,
                      bcur_params: Optional[str] = None,
                      random_seed: int = None,
                      e0_spin: bool = False,
                      isolated_atom: bool = True,
                      dimer: bool = True,
                      dimer_range: list = None,
                      dimer_num: int = None,
                      custom_set: Optional[str] = None,
                      vasp_ref_file: str = 'vasp_ref.extxyz',
                      rss_group: str = 'initial',
                      test_ratio: float = 0.1,
                      regularization: bool = True,
                      distillation: bool = True,
                      f_max: float = 200,
                      pre_database_dir: Optional[str] = None,
                      mlip_type: str = 'GAP',
                      ref_energy_name: str = "REF_energy",
                      ref_force_name: str = "REF_forces",
                      ref_virial_name: str = "REF_virial",
                      num_processes_fit: int = None,
                      scalar_pressure_method: str ='exp',
                      scalar_exp_pressure: float = 100,
                      scalar_pressure_exponential_width: float = 0.2,
                      scalar_pressure_low: float = 0,
                      scalar_pressure_high: float = 50,
                      max_steps: int = 10,
                      force_tol: float = 0.1,
                      stress_tol: float = 0.1,
                      Hookean_repul: bool = False,
                      write_traj: bool = True,
                      num_processes_rss: int = 4,
                      device: str = "cpu",
                      stop_criterion: float = 0.01,
                      max_iteration_number: int = 9,
                      **fit_kwargs,):

    if input['test_error'] is not None and input['test_error'] > stop_criterion and input['current_iter'] < max_iteration_number:
        if input['kt'] > 0.15:
            kt = input['kt'] - 0.1
        else:
            kt = 0.1
        print('kt:', kt)
        current_iter = input['current_iter'] + 1
        print('Current iter index:', current_iter)
        print(f'The error of {current_iter}th iteration:', input['test_error'])

        bcur_params['kT'] = kt

        job2 = sampling(selection_method=selection_method1,
                        num_of_selection=num_of_selection1,
                        bcur_params=bcur_params,
                        dir=input_dir,
                        random_seed=random_seed)
        job3 = do_rss(mlip_type=mlip_type, 
                      iteration_index=f'{current_iter}th', 
                      mlip_path=input['mlip_path'], 
                      structure=job2.output,
                      scalar_pressure_method=scalar_pressure_method,
                      scalar_exp_pressure=scalar_exp_pressure,
                      scalar_pressure_exponential_width=scalar_pressure_exponential_width,
                      scalar_pressure_low=scalar_pressure_low,
                      scalar_pressure_high=scalar_pressure_high,
                      max_steps=max_steps,
                      force_tol=force_tol,
                      stress_tol=stress_tol,
                      Hookean_repul=Hookean_repul,
                      write_traj=write_traj,
                      num_processes_rss=num_processes_rss,
                      device=device)
        job4 = sampling(selection_method=selection_method2,
                        num_of_selection=num_of_selection2,
                        bcur_params=bcur_params,
                        traj_info=job3.output,
                        random_seed=random_seed,
                        isol_es=input["isol_es"])
        
        job_list = [job2, job3, job4]

        return Response(detour=job_list, output=job4.output)
    

def test_mock_workflow(test_dir, mock_vasp, memory_jobstore, clean_dir):
    test_files_dir = test_dir / "data/rss.extxyz"
    # atoms = read(test_files_dir, index=':')
    # structures = [AseAtomsAdaptor.get_structure(atom) for atom in atoms]

    ref_paths = {
        **{f"static_bulk_{i}": f"rss/Si_bulk_{i+1}/" for i in range(18)},
        "static_isolated_0": "rss/Si_isolated_1/",
        "static_dimer_0": "rss/Si_dimer_1/",
        "static_dimer_1": "rss/Si_dimer_2/",
        "static_dimer_2": "rss/Si_dimer_3/",
    }

    fake_run_vasp_kwargs = {
        "static_isolated_0": {"incar_settings": {"ISPIN": 2, "KSPACINGS": 2.0}}, 
        "static_dimer_0": {"incar_settings": {"ISPIN": 2, "KSPACINGS": 2.0}}, 
        "static_dimer_1": {"incar_settings": {"ISPIN": 2, "KSPACINGS": 2.0}}, 
        "static_dimer_2": {"incar_settings": {"ISPIN": 2, "KSPACINGS": 2.0}}, 
    }

    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    job1=mock_RSS(input_dir=test_files_dir,
                  selection_method='cur',
                  num_of_selection=18,
                  bcur_params={'soap_paras': {'l_max': 3,
                                    'n_max': 3,
                                    'atom_sigma': 0.5,
                                    'cutoff': 4.0,
                                    'cutoff_transition_width': 1.0,
                                    'zeta': 4.0,
                                    'average': True,
                                    'species': True,
                                    },
                 },
                 random_seed=42,
                 e0_spin=True,
                 isolated_atom=True,
                 dimer=True,
                 dimer_range=[1.5, 2.0],
                 dimer_num=3,
                 custom_set={
                        "ADDGRID": None, 
                        "ENCUT": 200,
                        "EDIFF": 1E-04,
                        "ISMEAR": 0,
                        "SIGMA": 0.05,
                        "PREC": "Normal",
                        "ISYM": None,
                        "KSPACING": 0.3,
                        "NPAR": 8,
                        "LWAVE": "False",
                        "LCHARG": "False",
                        "ENAUG": None,
                        "GGA": None,
                        "ISPIN": None,
                        "LAECHG": None,
                        "LELF": None,
                        "LORBIT": None,
                        "LVTOT": None,
                        "NSW": None,
                        "SYMPREC": None,
                        "NELM": 50,
                        "LMAXMIX": None,
                        "LASPH": None,
                        "AMIN": None,
                    },
                 vasp_ref_file='vasp_ref.extxyz',
                 gap_rss_group='initial',
                 test_ratio=0.1,
                 regularization=True,
                 distillation=True,
                 f_max=0.7,
                 pre_database_dir=None,
                 mlip_type='GAP',
                 ref_energy_name="REF_energy",
                 ref_force_name="REF_forces",
                 ref_virial_name="REF_virial",
                 num_processes_fit=4,
                 kt=0.6
                )

    job2 = mock_do_RSS_iterations(input=job1.output,
                      input_dir=test_files_dir,
                      selection_method1='cur',
                      selection_method2='bcur',
                      num_of_selection1=5,
                      num_of_selection2=3,
                      bcur_params={'soap_paras': {'l_max': 3,
                                   'n_max': 3,
                                   'atom_sigma': 0.5,
                                   'cutoff': 4.0,
                                   'cutoff_transition_width': 1.0,
                                   'zeta': 4.0,
                                   'average': True,
                                   'species': True,
                                   },
                                   'frac_of_bcur': 0.8,
                                   'bolt_max_num': 3000,
                                   'kernel_exp': 4, 
                                   'energy_label': 'energy'},
                      random_seed=None,
                      e0_spin=False,
                      isolated_atom=True,
                      dimer=True,
                      dimer_range=None,
                      dimer_num=None,
                      custom_set=None,
                      vasp_ref_file='vasp_ref.extxyz',
                      rss_group='initial',
                      test_ratio=0.1,
                      regularization=True,
                      distillation=True,
                      f_max=200,
                      pre_database_dir=None,
                      mlip_type='GAP',
                      ref_energy_name="REF_energy",
                      ref_force_name="REF_forces",
                      ref_virial_name="REF_virial",
                      num_processes_fit=None,
                      scalar_pressure_method='exp',
                      scalar_exp_pressure=100,
                      scalar_pressure_exponential_width=0.2,
                      scalar_pressure_low=0,
                      scalar_pressure_high=50,
                      max_steps=100,
                      force_tol=0.6,
                      stress_tol=0.6,
                      Hookean_repul=False,
                      write_traj=True,
                      num_processes_rss=4,
                      device="cpu",
                      stop_criterion=0.01,
                      max_iteration_number=9
                      )

    response = run_locally(
        Flow([job1, job2]),
        create_folders=True,
        ensure_success=True,
        store=memory_jobstore
    ) 

    assert Path(job1.output["mlip_path"].resolve(memory_jobstore)).exists()

    selected_atoms = job2.output.resolve(memory_jobstore)

    assert len(selected_atoms) == 3


