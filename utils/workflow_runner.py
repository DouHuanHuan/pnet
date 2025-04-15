# workflow_runner.py
import pnet


def run_pnet_workflow(config: dict, paths: dict, output_dir: str):
    return pnet.workflow(
        dir_pnet_result=output_dir,
        dataType=config["dataType"],
        dataFormat=config["dataFormat"],
        file_Brain_Template=paths["template"],
        file_scan=paths["scan"],
        file_subject_ID=None,
        file_subject_folder=None,
        file_gFN=paths["gfn"],
        K=config["K"],
        Combine_Scan=False,
        method=config["method"],
        init=config.get("init", "random"),
        sampleSize=config["sampleSize"],
        nBS=config["nBS"],
        nTPoints=config["nTPoints"],
        Computation_Mode=config.get("Computation_Mode", "CPU_Torch")
    )
