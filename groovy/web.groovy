def yarn_build(){
    sh 'nrm use taobao && yarn --cwd ${PROJECT_ROOT}/${PROJECT_MODULE} install && yarn --cwd ${PROJECT_ROOT}/${PROJECT_MODULE} --ignore-engines build'
}

return this;