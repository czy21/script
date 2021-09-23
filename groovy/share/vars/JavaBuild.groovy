#!/usr/bin/env groovy

def call(Map map) {
    pipeline {
       agent any
       stages{
         stage('build'){
            steps{
                sh 'echo hello docker'
            }
         }
       }
    }
}

