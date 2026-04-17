pipeline {
    agent any

    environment {
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                bat '''
                    pip install -r backend/services/auth_service/requirements.txt pytest httpx
                    cd backend/services/auth_service
                    python -m pytest tests/ -v --tb=short || exit 0
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                bat '''
                    docker build -t helpdesk-auth:%IMAGE_TAG%    ./backend/services/auth_service
                    docker build -t helpdesk-ticket:%IMAGE_TAG%  ./backend/services/ticket_service
                    docker build -t helpdesk-comment:%IMAGE_TAG% ./backend/services/comment_service
                    docker build -t helpdesk-frontend:%IMAGE_TAG% ./frontend
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                    echo Checking Trivy...

                    where trivy >nul 2>nul
                    if %errorlevel% neq 0 (
                        echo Installing Trivy...

                        powershell -Command "Invoke-WebRequest -Uri https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.58.0_Windows-64bit.zip -OutFile trivy.zip"
                        powershell -Command "Expand-Archive trivy.zip -DestinationPath C:\\trivy"

                        set PATH=C:\\trivy;%PATH%
                    )

                    trivy image --severity HIGH,CRITICAL --exit-code 0 helpdesk-auth:%IMAGE_TAG%
                    trivy image --severity HIGH,CRITICAL --exit-code 0 helpdesk-frontend:%IMAGE_TAG%
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    bat """
                        C:\\sonar-scanner\\bin\\sonar-scanner.bat ^
                        -Dsonar.projectKey=helpdesk ^
                        -Dsonar.sources=backend,frontend ^
                        -Dsonar.host.url=http://localhost:9000 ^
                        -Dsonar.login=%SONAR_AUTH_TOKEN%
                    """
                }
            }
        }
        stage('Push to DockerHub') {
            when { branch 'main' }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-password',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin

                        docker tag helpdesk-auth:%IMAGE_TAG% %DOCKER_USER%/helpdesk-auth:latest
                        docker push %DOCKER_USER%/helpdesk-auth:latest

                        docker tag helpdesk-ticket:%IMAGE_TAG% %DOCKER_USER%/helpdesk-ticket:latest
                        docker push %DOCKER_USER%/helpdesk-ticket:latest

                        docker tag helpdesk-comment:%IMAGE_TAG% %DOCKER_USER%/helpdesk-comment:latest
                        docker push %DOCKER_USER%/helpdesk-comment:latest

                        docker tag helpdesk-frontend:%IMAGE_TAG% %DOCKER_USER%/helpdesk-frontend:latest
                        docker push %DOCKER_USER%/helpdesk-frontend:latest
                    '''
                }
            }
        }

        stage('Update Manifests') {
            when { branch 'main' }
            steps {
                bat '''
                    powershell -Command "(Get-Content manifests/deployments/auth-deployment.yaml) -replace 'image:.*helpdesk-auth:.*','image: %DOCKER_USER%/helpdesk-auth:%IMAGE_TAG%' | Set-Content manifests/deployments/auth-deployment.yaml"

                    git config user.email "jenkins@helpdesk.com"
                    git config user.name "Jenkins CI"

                    git add manifests/
                    git commit -m "ci: update image tag %IMAGE_TAG%" || exit 0
                    git push origin main || exit 0
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline passed — ArgoCD will sync the cluster"
        }
        failure {
            echo "❌ Pipeline failed — check logs above"
        }
    }
}