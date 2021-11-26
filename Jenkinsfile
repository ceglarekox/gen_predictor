pipeline {
    agent any

    stages {
        stage('clean up') {
            steps {
                echo 'clean up..'
		script{
		   try { 
	              sh 'sudo rm -rf "gen_predictor"'
		   } catch (err) {
			echo err.getMessage()
		   }
		}
            }
        }
        stage('clone repo') {
            steps {
                echo 'cloning repo..'
		sh "git clone https://github.com/ceglarekox/gen_predictor.git"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
		sh "python3 testing/unit_tests.py"
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
