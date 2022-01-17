#!/usr/bin/env groovy
package org.ops

def build(){
    switch(env.param_code_type) {
     case "java":
        gradle_cmd = ["clean","build"].collect{t->[env.param_project_module,t].findAll{ c -> ![null, "null", ""].contains(c) }.join(":")}.join(" ")
        sh "chmod +x ${param_project_root}/gradlew && ${env.param_project_root}/gradlew --gradle-user-home ${env.param_gradle_user_home} --init-script ${env.param_gradle_init_file} --build-file ${env.param_project_root}/build.gradle ${gradle_cmd} -x test --parallel"
        break;
     case "go":
        break;
     case "python":
        break;
     case "web":
        env.NODEJS_HOME = "${tool 'node-v16.13.0'}"
        env.PATH="${NODEJS_HOME}/bin:${PATH}"
        sh 'yarn --cwd ${param_project_context} --registry ${param_npm_registry} --cache-folder ${param_yarn_cache} install && yarn --cwd ${param_project_context} --registry ${param_npm_registry} --cache-folder ${param_yarn_cache} --ignore-engines build'
        break;
     default:
        println [env.param_code_type,"not config"].join(" ");
        return;
    }
    sh 'docker login ${env.param_registry_repo} --username ${env.param_registry_username} --password ${env.param_registry_password}'
    sh 'docker build --tag ${env.param_image_name}:${env.param_release_version} --file ${env.param_docker_file} ${env.param_project_context} --no-cache --force-rm'
    sh 'docker push ${env.param_image_name}:${env.param_release_version}'
}


def prepare(){
    configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", targetLocation: 'global_env.groovy', variable: 'ENV_CONFIG')]) {
        load "global_env.groovy";
    }
    env.param_release_version = params.param_branch
    env.param_project_context = [env.param_project_root,env.param_project_module].findAll{ t -> ![null, "null", ""].contains(t) }.join("/")
    env.param_image_name      = ["${env.param_registry_repo}/${env.param_registry_dir}",[env.param_project_name,env.param_project_module].findAll{ t -> ![null, "null", ""].contains(t) }.join("-")].join("/")
    env.param_docker_file     = "${env.param_project_context}/Dockerfile"
}

return this