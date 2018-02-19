import os
from pybuilder.core import use_plugin, init, task, depends
from pybuilder.errors import BuildFailedException

# Core Plugins
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin('pypi:pybuilder_aws_plugin')

# IDE Plugin
# Run pyb pycharm_generate to configure IDE
use_plugin('python.pycharm')

# Properties
name = "mylawn"
default_task = "publish"
version = "0.1"
lambda_name = "MyLawn"
bucket_name = "mylawn"
latest_code = "code/latest/mylawn.zip"


@init
def set_properties(project):
    # AWS Properties
    project.set_property("bucket_name", "centrospecos")
    project.set_property("bucket_prefix", "code/")
    project.set_property("coverage_break_build", False)
    project.depends_on_requirements("requirements.txt")
    project.build_depends_on_requirements("requirements-dev.txt")


@depends('clean', 'package_lambda_code', 'upload_zip_to_s3', 'lambda_release')
@task
def deploy(logger):
    pass


@task
def update_lambda(logger):
    upload_cmd = "aws lambda update-function-code --function-name %s --s3-bucket %s --s3-key %s"
    final_cmd = upload_cmd % (lambda_name,bucket_name,latest_code)

    logger.info("Updating lambda")
    logger.info(final_cmd)

    exit_code = os.system(final_cmd)
    if exit_code:
        err_msg = "Failed with exit code: %d" % exit_code
        logger.error(err_msg)
        raise BuildFailedException(message="Unable to update lamdba!")
