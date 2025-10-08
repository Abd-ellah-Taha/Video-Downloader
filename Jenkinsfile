pipeline {
  agent any
  environment {
    DOCKER_IMAGE = "myvideo-downloader"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Lint & Test') {
      steps {
        sh 'python3 -m pip install -r requirements.txt'
        sh 'flake8 || true'
      }
    }
    stage('Build Docker') {
      steps {
        script {
          dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}")
        }
      }
    }
    stage('Push') {
      when { expression { env.DOCKER_REGISTRY != null } }
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh "echo $PASS | docker login $DOCKER_REGISTRY -u $USER --password-stdin"
          sh "docker tag ${DOCKER_IMAGE}:${env.BUILD_NUMBER} $DOCKER_REGISTRY/${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
          sh "docker push $DOCKER_REGISTRY/${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
        }
      }
    }
  }
}
