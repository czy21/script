#!/usr/bin/env groovy
package org.ops

def build(){
    switch(env.param_code_type) {
     case "java":
        sh 'chmod +x ${param_project_root}/gradlew && ${param_project_root}/gradlew --gradle-user-home ${param_gradle_user_home} --init-script ${param_gradle_init_file} --build-file ${param_project_root}/build.gradle ${param_project_module}:clean ${param_project_module}:build -x test --parallel'
        break;
     case "web":
        env.NODEJS_HOME = "${tool 'node-v16.13.0'}"
        env.PATH="${NODEJS_HOME}/bin:${PATH}"
        sh 'npm config set registry ${param_yarn_registry} && npm install --prefix ${param_project_root}/${param_project_module} && npm run build --prefix ${param_project_root}/${param_project_module}'
        break;
     case "go":
        break;
     default:
        println [env.param_code_type,"not config"].join(" ");
        return;
    }
    sh 'docker login ${param_registry_repo} --username ${param_registry_username} --password ${param_registry_password}'
    sh 'docker build --tag ${param_image_name}:${param_release_version} --file ${param_docker_file} ${param_docker_file_context} --no-cache --force-rm'
    sh 'docker push ${param_image_name}:${param_release_version}'
}


def prepare(Map map){
    configFileProvider([configFile(fileId: "${param_global_env_file_id}", targetLocation: 'global_env.groovy', variable: 'ENV_CONFIG')]) {
        load "global_env.groovy";
    }
    env.param_release_version = params.param_branch
    env.param_image_name=[env.param_registry_repo,env.param_registry_dir,[env.param_project_name,env.param_project_module].findAll{it!=null|!it.equals("null")|it!=""}.join("-")].join("/")
    env.param_docker_file = [env.param_project_root,env.param_project_module,"Dockerfile"].findAll{it!=null|!it.equals("null")|it!=""}.join("/")
    env.param_docker_file_context = [env.param_project_root,env.param_project_module].findAll{it!=null|!it.equals("null")|it!=""}.join("/")
    def a=[env.param_registry_repo,env.param_registry_dir,[env.param_project_name,env.param_project_module].findAll{it->it!=null|it!="null"|it!=""}.join("-")].findAll{it->it!=null|!it!="null"|it!=""}.join("/")
    println a
}

return this