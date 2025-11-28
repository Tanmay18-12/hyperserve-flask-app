pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'hyperserve-svc'
        IMAGE_TAG = '3'
        CONTAINER_NAME = 'hyperserve-container'
        HOST_PORT = '12208'
        CONTAINER_PORT = '12208'
    }
    
    stages {
        stage('Pre-check Docker') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 1: Pre-check Docker'
                    echo '========================================='
                    
                    try {
                        // Check if Docker is installed and running
                        bat 'docker --version'
                        bat 'docker info'
                        echo '✓ Docker is available and running'
                    } catch (Exception e) {
                        error('❌ Docker is not available! Please ensure Docker Desktop is installed and running.')
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                echo '========================================='
                echo 'Stage 2: Checkout Source Code'
                echo '========================================='
                checkout scm
                echo '✓ Source code checked out successfully'
            }
        }
        
        stage('Cleanup Old Container') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 3: Cleanup Old Container'
                    echo '========================================='
                    
                    // Stop and remove old container if exists
                    bat """
                        docker stop ${CONTAINER_NAME} 2>nul || echo Container not running
                        docker rm ${CONTAINER_NAME} 2>nul || echo Container not found
                    """
                    echo '✓ Old container cleaned up'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 4: Build Docker Image'
                    echo '========================================='
                    echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    
                    bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                    
                    // Verify image was created
                    bat "docker images ${IMAGE_NAME}:${IMAGE_TAG}"
                    echo '✓ Docker image built successfully'
                }
            }
        }
        
        stage('Run Container') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 5: Run Docker Container'
                    echo '========================================='
                    echo "Starting container on port ${HOST_PORT}"
                    
                    bat """
                        docker run -d ^
                        -p ${HOST_PORT}:${CONTAINER_PORT} ^
                        --name ${CONTAINER_NAME} ^
                        ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                    
                    // Wait for container to start
                    echo 'Waiting for container to start...'
                    sleep 5
                    
                    // Verify container is running
                    bat "docker ps -f name=${CONTAINER_NAME}"
                    echo '✓ Container started successfully'
                }
            }
        }
        
        stage('Verify Service') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 6: Verify Service is Running'
                    echo '========================================='
                    
                    // Check if port is listening
                    bat "netstat -an | findstr :${HOST_PORT}"
                    
                    // Try to access the service
                    echo 'Testing service endpoint...'
                    sleep 2
                    bat "curl -f http://localhost:${HOST_PORT}/ || echo Service check completed"
                    
                    echo '✓ Service is listening on port ' + HOST_PORT
                }
            }
        }
        
        stage('Display Container Info') {
            steps {
                script {
                    echo '========================================='
                    echo 'Stage 7: Container Information'
                    echo '========================================='
                    
                    bat "docker ps -f name=${CONTAINER_NAME}"
                    bat "docker logs ${CONTAINER_NAME}"
                    
                    echo ''
                    echo '╔════════════════════════════════════════╗'
                    echo '║   HyperServe Service Deployed!         ║'
                    echo '╚════════════════════════════════════════╝'
                    echo "Service URL: http://localhost:${HOST_PORT}"
                    echo "Container: ${CONTAINER_NAME}"
                    echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
    
    post {
        success {
            echo ''
            echo '========================================='
            echo '✓ PIPELINE SUCCESS'
            echo '========================================='
            echo 'HyperServe service is online for CIE set 207'
            echo "Access the service at: http://localhost:${HOST_PORT}"
        }
        failure {
            echo ''
            echo '========================================='
            echo '❌ PIPELINE FAILED'
            echo '========================================='
            echo 'Check the console output above for errors'
            
            // Cleanup on failure
            bat """
                docker stop ${CONTAINER_NAME} 2>nul || echo No container to stop
                docker rm ${CONTAINER_NAME} 2>nul || echo No container to remove
            """
        }
        always {
            echo ''
            echo 'Pipeline execution completed'
        }
    }
}