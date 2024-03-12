current_dir:=$(shell pwd)
project_name:=first_dbt_project
rel_project_dir:=$(project_name)
abs_project_dir:=$(current_dir)
abs_profiles_dir:=$(current_dir)
env_file:=$(current_dir)/.env
dbt_image_version:=v1.6.0
os_docker_flag:=
ifeq ($(shell uname -s),Linux)
	os_docker_flag += --add-host host.docker.internal:host-gateway
endif
docker_dbt_shell_command:=docker run --rm $(os_docker_flag) --env-file $(env_file) --entrypoint /bin/bash --privileged -it -e NO_DOCKER=1 --network=host -v $(current_dir):/workspace -w /workspace public.ecr.aws/dataminded/dbt:$(dbt_image_version)
docker_dbt_command:=docker run --rm $(os_docker_flag) --env-file $(env_file) -it -v $(current_dir):/workspace -w /workspace public.ecr.aws/dataminded/dbt:$(dbt_image_version)

supported_args=target models select
args = $(foreach a,$(supported_args),$(if $(value $a),--$a "$($a)"))

env:
	touch $(current_dir)/.env

shell: env
	eval "$(docker_dbt_shell_command)"

deps:
	dbt deps --profiles-dir $(abs_profiles_dir) --project-dir $(abs_project_dir) $(call args,$@)

manifest: env
	eval "$(docker_dbt_command)" ls --profiles-dir ./ --project-dir ./ $(call args,$@)
	cp $(abs_project_dir)/target/manifest.json $(current_dir)/dags/manifest.json

debug:
	dbt debug --profiles-dir $(abs_profiles_dir) --project-dir $(abs_project_dir) $(call args,$@)

test:
	dbt test --profiles-dir $(abs_profiles_dir) --project-dir $(abs_project_dir) $(call args,$@)

run:
	dbt run --profiles-dir $(abs_profiles_dir) --project-dir $(abs_project_dir) $(call args,$@)

docs:
	dbt docs serve --profiles-dir $(abs_profiles_dir) --project-dir $(abs_project_dir) $(call args,$@)
