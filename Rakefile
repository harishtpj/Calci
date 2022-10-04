PY="python"
SRC="calci.py"

task :default => [:run]

desc "Runs Calci Interpreter"
task :run do
    puts "---> Running Interpreter"
    sh "#{PY} #{SRC} #{ENV['ARGS']}",  verbose: false
end

desc "Cleans Working Directory by deleting files"
task :clean do
    rm_rf "__pycache__", verbose: false
    rm_rf "calci\\__pycache__", verbose: false
    puts "---> Cleaned Directory by deleting files"
end