pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        //   cmakeBuild(
        //     installation: 'InSearchPath'
        //   )
        sh 'echo "Building..."'
        sh 'chmod +x ./installer.sh'
        sh 'bash ./installer.sh'
        // archiveArtifacts artifacts: 'Version_1/out/build/*', fingerprint: true
      }
    }
    // stage('Test') {
    //   steps {
    //     //   cmakeBuild(
    //     //     installation: 'InSearchPath'
    //     //   )
    //     sh 'echo "Running..."'
    //     sh 'chmod +x ./Version_1/run.sh'
    //     sh 'bash ./Version_1/run.sh'
    //   }
    // }
  }
}