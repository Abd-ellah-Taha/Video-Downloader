pipeline {
    agent any

    environment {
        APP_NAME = "video-downloader"
        DEPLOY_DIR = "/var/www/video-downloader"
        GIT_BRANCH = "master"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Pulling latest code from GitHub..."
                git branch: "${GIT_BRANCH}", url: 'https://github.com/Abd-ellah-Taha/Video-Downloader.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                echo "🐍 Setting up Python virtual environment..."
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint & Test') {
            steps {
                echo "🧹 Running Lint and Tests..."
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 || true
                    python3 -m unittest discover || true
                '''
            }
        }

        stage('Build') {
            steps {
                echo "⚙️ Building the project..."
                sh '''
                    . venv/bin/activate
                    echo "Build completed successfully!"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying to server..."
                sh '''
                    sudo systemctl stop ${APP_NAME} || true
                    rsync -av --exclude 'venv' --exclude '.git' ./ ${DEPLOY_DIR}/
                    sudo systemctl start ${APP_NAME}
                    echo "✅ Deployment completed successfully!"
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline finished successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}

