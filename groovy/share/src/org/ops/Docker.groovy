#!/usr/bin/env groovy
package org.ops

def buildJava(){
    pipeline {
       agent any
       stages{
         stage('build'){
            steps{
                script{

                }
                sh 'echo hello docker'
            }
         }
       }
    }
}

return this