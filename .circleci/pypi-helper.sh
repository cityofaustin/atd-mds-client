#!/usr/bin/env bash

CIRCLE_BRANCH="powpowpow";

if [[ "${CIRCLE_BRANCH}" = "master" ]]; then
    export BUILD_ENV="master";
else
    export BUILD_ENV="dev";
fi;


#
# A helper function that prints a message in the build logs that is easy to identify.
#
function print_header {
    echo "---------------------------------------------------------------------";
    echo ">> $1";
    echo "---------------------------------------------------------------------";
    echo "";
}



#
# Prints a line for logging
#
function print_log {
    ENABLE_LOGGING="true"
    if [[ "${ENABLE_LOGGING}" = "true" ]]; then
        echo -e "$1";
    fi;
}



#
# Patches the setup.py file in order to deploy a specific package environment
#
function mds_patch_package_name {
    print_header "mds_patch_package_name() Patching package. Environment: ${BUILD_ENV}";

    # Only add postfix if not on master
    if [[ "${BUILD_ENV}" != "master" ]]; then
        sed -i '7s/atd-mds-client/atd-mds-client-dev/g' setup.py;
    fi;
}


#
# Build & Publish a single package.
# It assumes 'setup.py' is in the current working directory.
#
function mds_build_package {
    print_header "mds_build_package() building package ...";
    python3 setup.py sdist bdist_wheel;
}


#
# Deploys a built package into pypi.
# It assumes the 'dist' folder is in the current working directory.
#
function mds_deploy_package {
    print_header "mds_deploy_package() deploying package...";
    print_log "mds_deploy_package() twine upload --repository-url https://upload.pypi.org/legacy/ dist/*;"
    #twine upload --repository-url https://upload.pypi.org/legacy/ dist/*;
}
