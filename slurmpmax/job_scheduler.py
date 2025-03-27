from datetime import datetime
import subprpocess



class SlurmJob:
    def __init__(self, **kwargs):
        self.opts = self.fetch_opts(kwargs)
        self.slurm = self.fetch_slurmjob()

    def fetch_slurmjob(self)
        template = self.opts.get("template")
        templates = {
            "default": f"""#!/bin/bash -l
#SBATCH -A {self.opts.get("project_code")}
#SBATCH -p {self.opts.get("partition")}
#SBATCH -n {self.opts.get("n_tasks")}
#SBATCH -t {self.opts.get("time_limit")}
#SBATCH -J {self.opts.get("job_name")}
#SBATCH --output={self.opts.get("log_file")}
#SBATCH --error={self.opts.get("error_file")}
""",
            "dummy-template": "don't use this"
        }
        # TODO
        # create possibility to read in templates from a file
        t = templates[template]
        if "constraint" in self.opts and self.opts.get("constraint") is not None:
            t = t + f"""#SBATCH --{self.opts.get("constraint")}\n"""
        t = t + f'source /sw/apps/conda/latest/rackham_stage/etc/profile.d/conda.sh\nconda activate {self.opts.get("conda_env")}\n\n'
        e = self.opts.get("executable")
        if "exargs" in self.opts and self.opts.get("exargs") is not None:
            e = e + " " + self.opts.get("exargs")
        t = t + "\n" + e + "\n"


        return t


    def fetch_opts(self, kwargs):
        opts =  {
            "project_code": "uppmax2025-2-274",
            "partition": "core",
            "n_tasks": 1,
            "time_limit": "12:00:00",
            "job_name": "default",
            "conda_env": "topics",
            "log_file": f'{datetime.now().strftime("%Y%m%d-%H%M%S")}_default.log',
            "error_file":f'{datetime.now().strftime("%Y%m%d-%H%M%S")}_default.err'
        }
        opts.update(kwargs)
        return opts

    def run(self):
        print(f"Running {self.opts.get('job_name')}")
        return subprocess.run(["sbatch"], input=self.slurm, text=True, capture_output=True)
