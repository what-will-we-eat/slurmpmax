"""
start a slurm job.
"""
from slurmpmax.job_scheduler import SlurmJob
from datetime import datetime
import argparse
import os
import sys



def main(args):
    job = SlurmJob(**vars(args))
    print("Starting job:\n")
    print(job.slurm)
    result = job.run()
    print(result.stdout)
    print(result.stderr)
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-e", "--executable", required=True, help="script to run with sbatch")
    parser.add_argument("--exargs", type=str, default=None, help="arguments for the executable")
    parser.add_argument("--conda-env", type=str, default='adri')
    parser.add_argument("-C", "--constraint", type=str)
    parser.add_argument("-j", "--job-name", default="default")
    parser.add_argument("--log-file", 
                        type=str, 
                        default=None, 
                        help="If unset, will default to a datetime string and job name")
    parser.add_argument("--error-file", 
                        type=str, 
                        default=None, 
                        help="If unset, will default to a datetime string and job name")
    parser.add_argument("--log-location", default="slurm-logs")
    parser.add_argument("--partition", default="core", choices=["core", "devcore", "devel", "node"])
    parser.add_argument("-A", "--project", default="uppmax2025-2-274")
    parser.add_argument("-t", "--time-limit", default="12:00:00")
    parser.add_argument("--template", default="default")
    args = parser.parse_args()
    if args.log_file is None:
        args.log_file = f'{args.log_location}/{args.job_name}/{datetime.now().strftime("%Y%m%d-%H%M%S")}_{args.job_name}.log'
    if args.error_file is None:
        args.error_file = f'{args.log_location}/{args.job_name}/{datetime.now().strftime("%Y%m%d-%H%M%S")}_{args.job_name}.err'
    os.makedirs(f'{args.log_location}/{args.job_name}', exist_ok=True)
    main(args)
